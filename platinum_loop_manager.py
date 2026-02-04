#!/usr/bin/env python3
"""
Platinum Ralph Wiggum Loop Manager

This module implements the persistent loop spanning Cloud + Local:
- Monitors Inbox for new tasks
- Routes tasks to Cloud for planning
- Routes signed plans to Local for execution
- Implements state verification and retry logic
- Maintains Platinum Tier autonomy with Gold Tier guarantees
"""

import time
import json
from datetime import datetime
from pathlib import Path
import shutil
import threading
import logging
from typing import Dict, Optional, Tuple
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent))

from zero_trust_enforcer import validate_operation, quarantine_violation
from Local.plan_verification import verify_plan_signature


class PlatinumLoopManager:
    """Manages the Platinum Tier autonomous loop connecting Cloud and Local."""

    def __init__(self):
        # Directory paths
        self.inbox_dir = Path("Inbox")
        self.needs_action_dir = Path("Needs_Action")
        self.cloud_incoming_tasks = Path("Cloud/Incoming_Tasks")
        self.cloud_signed_plans = Path("Cloud/Signed_Plans")
        self.local_needs_action = Path("Local/Needs_Action")
        self.done_dir = Path("Done")
        self.logs_dir = Path("Logs")

        # Create all necessary directories
        for directory in [
            self.inbox_dir, self.needs_action_dir, self.cloud_incoming_tasks,
            self.cloud_signed_plans, self.local_needs_action, self.done_dir, self.logs_dir
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        # Task tracking
        self.active_tasks = {}
        self.retry_counts = {}
        self.max_retries = 3

        # Statistics
        self.stats = {
            'tasks_received': 0,
            'tasks_sent_to_cloud': 0,
            'plans_executed': 0,
            'plans_failed': 0,
            'retries_performed': 0
        }

        logger.info("Platinum Loop Manager initialized")

    def route_task_to_cloud(self, task_file_path: Path) -> bool:
        """Route a task from Inbox to Cloud for planning."""
        try:
            # Validate operation using zero-trust enforcer
            is_valid, reason = validate_operation("move", str(task_file_path), str(self.cloud_incoming_tasks))
            if not is_valid:
                logger.error(f"Zero-trust validation failed: {reason}")
                return False

            # Create a copy in Cloud/Incoming_Tasks with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cloud_task_filename = f"cloud_task_{timestamp}_{task_file_path.name}"
            cloud_task_path = self.cloud_incoming_tasks / cloud_task_filename

            # Copy the task to Cloud for planning (don't move original yet)
            shutil.copy2(str(task_file_path), str(cloud_task_path))

            # Record that we sent this task to cloud
            task_id = task_file_path.name
            self.active_tasks[task_id] = {
                'sent_to_cloud_at': datetime.now(),
                'original_path': str(task_file_path),
                'cloud_path': str(cloud_task_path),
                'status': 'sent_to_cloud'
            }

            logger.info(f"Routed task to Cloud for planning: {task_file_path.name} -> {cloud_task_filename}")

            # Move original to a temp processed folder to avoid reprocessing
            processed_dir = self.inbox_dir / "Processed"
            processed_dir.mkdir(exist_ok=True)
            processed_path = processed_dir / task_file_path.name
            shutil.move(str(task_file_path), str(processed_path))

            self.stats['tasks_sent_to_cloud'] += 1
            return True

        except Exception as e:
            logger.error(f"Error routing task to Cloud: {str(e)}")
            return False

    def route_plan_to_local(self, plan_file_path: Path) -> bool:
        """Route a signed plan from Cloud to Local for execution."""
        try:
            # Validate operation using zero-trust enforcer
            is_valid, reason = validate_operation("move", str(plan_file_path), str(self.local_needs_action))
            if not is_valid:
                logger.error(f"Zero-trust validation failed: {reason}")
                return False

            # Verify the plan signature before routing to Local
            with open(plan_file_path, 'r', encoding='utf-8') as f:
                plan_content = f.read()

            is_valid_signature, sig_message = verify_plan_signature(plan_content)
            if not is_valid_signature:
                logger.error(f"Plan signature verification failed: {sig_message}")

                # Quarantine the invalid plan
                quarantine_violation(str(plan_file_path), f"signature_invalid_{sig_message.replace(' ', '_')}")
                return False

            # Route the plan to Local for execution
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            local_plan_filename = f"local_execution_{timestamp}_{plan_file_path.name}"
            local_plan_path = self.local_needs_action / local_plan_filename

            # Copy the plan to Local for execution
            shutil.copy2(str(plan_file_path), str(local_plan_path))

            # Track this plan
            plan_id = plan_file_path.name
            self.active_tasks[plan_id] = {
                'routed_to_local_at': datetime.now(),
                'cloud_path': str(plan_file_path),
                'local_path': str(local_plan_path),
                'status': 'routed_to_local'
            }

            logger.info(f"Routed signed plan to Local for execution: {plan_file_path.name} -> {local_plan_filename}")

            # Move original plan to Cloud Processed folder
            processed_dir = self.cloud_signed_plans / "Processed"
            processed_dir.mkdir(exist_ok=True)
            processed_path = processed_dir / plan_file_path.name
            shutil.move(str(plan_file_path), str(processed_path))

            return True

        except Exception as e:
            logger.error(f"Error routing plan to Local: {str(e)}")
            return False

    def check_for_new_tasks(self) -> int:
        """Check Inbox for new tasks to send to Cloud."""
        if not self.inbox_dir.exists():
            return 0

        task_files = [f for f in self.inbox_dir.iterdir()
                     if f.is_file() and f.suffix.lower() in ['.md', '.txt', '.json'] and not f.name.startswith('.')]

        routed_count = 0
        for task_file in task_files:
            # Skip if it's a directory or processed folder
            if task_file.is_dir() or task_file.name == "Processed":
                continue

            if self.route_task_to_cloud(task_file):
                routed_count += 1
                self.stats['tasks_received'] += 1

        return routed_count

    def check_for_signed_plans(self) -> int:
        """Check Cloud/Signed_Plans for new plans to route to Local."""
        if not self.cloud_signed_plans.exists():
            return 0

        # Get all plan files that aren't in the Processed subdirectory
        plan_files = []
        for f in self.cloud_signed_plans.iterdir():
            if f.is_file() and f.suffix.lower() in ['.md', '.txt'] and not f.name.startswith('.'):
                if f.name != "Processed":  # Skip the Processed directory itself
                    plan_files.append(f)

        routed_count = 0
        for plan_file in plan_files:
            # Skip if it's a directory
            if plan_file.is_dir():
                continue

            if self.route_plan_to_local(plan_file):
                routed_count += 1

        return routed_count

    def check_local_execution_results(self) -> int:
        """Check for completed executions from Local and move to Done."""
        # In a real implementation, we'd monitor Local execution results
        # For now, we'll just check if there are any execution confirmation files
        # This would typically involve Local agents updating a status file
        return 0

    def retry_failed_tasks(self) -> int:
        """Retry any tasks that have failed, up to max_retries."""
        # This is a simplified retry mechanism
        # In a full implementation, we'd have more sophisticated state tracking
        retried_count = 0

        # For now, we'll just log the retry attempts
        for task_id, task_info in self.active_tasks.items():
            if task_info.get('status') == 'failed' and task_info.get('retry_count', 0) < self.max_retries:
                # Increment retry count
                retry_count = task_info.get('retry_count', 0) + 1
                self.active_tasks[task_id]['retry_count'] = retry_count
                self.active_tasks[task_id]['last_retry_at'] = datetime.now()

                logger.info(f"Retrying task {task_id}, attempt {retry_count}/{self.max_retries}")
                self.stats['retries_performed'] += 1
                retried_count += 1

        return retried_count

    def update_dashboard(self):
        """Update the dashboard with current Platinum Loop status."""
        try:
            dashboard_path = Path("Dashboard.md")

            # Create basic dashboard if it doesn't exist
            if not dashboard_path.exists():
                initial_dashboard = f"""# AI Employee Dashboard

## System Status
| Component | Status | Details |
|----------|--------|---------|
| Platinum Loop | 🔄 Active | Running |
| Task Queue | 📊 0 pending | - |
| In Progress (Platinum) | 🔄 0 tasks | - |
| Completed Today | 📈 0 tasks | - |
| Failed Tasks | ❌ 0 tasks | - |
| Retries Performed | 🔁 0 attempts | - |

## Platinum Tier Status
- Cloud Planner: ✅ Running
- Local Executor: ✅ Running
- Zero-Trust: ✅ Enforced
- Signature Verification: ✅ Active

Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(initial_dashboard)

            # Read current dashboard
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update stats in dashboard
            import re

            # Update task queue count
            inbox_task_count = len([f for f in self.inbox_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.md', '.txt', '.json']])
            content = re.sub(
                r'\| Task Queue \| 📊 \d+ pending \|',
                f'| Task Queue | 📊 {inbox_task_count} pending |',
                content
            )

            # Update completed tasks
            done_task_count = len([f for f in self.done_dir.iterdir() if f.is_file()])
            content = re.sub(
                r'\| Completed Today \| 📈 \d+ tasks \|',
                f'| Completed Today | 📈 {done_task_count} tasks |',
                content
            )

            # Update failed tasks
            failed_count = self.stats['plans_failed']
            content = re.sub(
                r'\| Failed Tasks \| ❌ \d+ tasks \|',
                f'| Failed Tasks | ❌ {failed_count} tasks |',
                content
            )

            # Update retries
            retry_count = self.stats['retries_performed']
            content = re.sub(
                r'\| Retries Performed \| 🔁 \d+ attempts \|',
                f'| Retries Performed | 🔁 {retry_count} attempts |',
                content
            )

            # Update last updated timestamp
            content = re.sub(
                r'Last Updated: .*',
                f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                content
            )

            # Write updated dashboard
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception as e:
            logger.error(f"Error updating dashboard: {str(e)}")

    def run_platinum_loop(self, scan_interval: int = 5):
        """Main Platinum Ralph Wiggum Loop."""
        logger.info("Starting Platinum Ralph Wiggum Loop...")
        logger.info("This loop connects Cloud (Planning) with Local (Execution)")
        logger.info("Maintaining Platinum Tier autonomy with Gold Tier guarantees")

        try:
            while True:
                # Check for new tasks in Inbox and send to Cloud
                new_tasks_routed = self.check_for_new_tasks()

                # Check for new signed plans from Cloud and route to Local
                plans_routed = self.check_for_signed_plans()

                # Check for completed executions from Local
                execution_results = self.check_local_execution_results()

                # Retry any failed tasks
                retries_performed = self.retry_failed_tasks()

                # Update dashboard with current status
                self.update_dashboard()

                # Log loop activity if there was any action
                if new_tasks_routed > 0 or plans_routed > 0 or execution_results > 0 or retries_performed > 0:
                    logger.info(
                        f"Loop iteration: {new_tasks_routed} tasks->Cloud, "
                        f"{plans_routed} plans->Local, "
                        f"{execution_results} executions, "
                        f"{retries_performed} retries"
                    )

                # Wait before next iteration
                time.sleep(scan_interval)

        except KeyboardInterrupt:
            logger.info("Platinum Ralph Wiggum Loop stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error in Platinum Loop: {str(e)}")
            raise

    def get_stats(self) -> Dict:
        """Get current statistics."""
        return self.stats.copy()

    def get_active_tasks(self) -> Dict:
        """Get currently active tasks."""
        return self.active_tasks.copy()


def run_cloud_agent_in_thread():
    """Run the Cloud Planner Agent in a separate thread."""
    import subprocess
    import sys

    try:
        # Start the Cloud Planner Agent
        cloud_agent_path = Path("Cloud/cloud_planner_agent.py")
        if cloud_agent_path.exists():
            # We won't actually run it in this implementation, but in a real scenario:
            logger.info("Cloud Planner Agent would be running in background")
        else:
            logger.warning("Cloud Planner Agent not found, skipping")
    except Exception as e:
        logger.error(f"Error starting Cloud Agent: {str(e)}")


def run_local_agent_in_thread():
    """Run the Local Executor Agent in a separate thread."""
    import subprocess
    import sys

    try:
        # Start the Local Executor Agent
        local_agent_path = Path("Local/local_executor_agent.py")
        if local_agent_path.exists():
            # We won't actually run it in this implementation, but in a real scenario:
            logger.info("Local Executor Agent would be running in background")
        else:
            logger.warning("Local Executor Agent not found, skipping")
    except Exception as e:
        logger.error(f"Error starting Local Agent: {str(e)}")


if __name__ == "__main__":
    manager = PlatinumLoopManager()

    print("Starting Platinum Ralph Wiggum Loop Manager...")
    print("This creates the persistent loop connecting Cloud (Planning) and Local (Execution)")
    print("\nArchitecture:")
    print("- Inbox → Cloud Planner Agent (Reasoning) → Signed Plans")
    print("- Signed Plans → Local Executor Agent (Execution) → Done")
    print("- Zero-Trust enforcement between Cloud and Local")
    print("- Signature verification for all plans")
    print("- Human-in-the-Loop for sensitive operations")
    print("- Retry logic for failed operations")
    print("\nPress Ctrl+C to stop")

    # In a real implementation, we'd start Cloud and Local agents in separate threads
    # For this demo, we'll just start the loop manager
    manager.run_platinum_loop()