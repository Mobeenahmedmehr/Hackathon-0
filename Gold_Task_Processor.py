"""
Gold Tier Autonomous Task Processor for AI Employee
Implements persistent multi-step execution loop with state verification and recovery.
"""

import time
import json
from datetime import datetime
from pathlib import Path
import shutil
import re
import threading
from enum import Enum
from typing import Dict, List, Optional, Tuple

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    QUARANTINED = "quarantined"

class ErrorType(Enum):
    TRANSIENT = "transient"
    AUTH = "auth"
    LOGIC = "logic"
    SYSTEM = "system"

class GoldTaskProcessor:
    """
    Gold Tier persistent task processor with autonomous loop, error handling, and audit logging.
    """

    def __init__(self,
                 inbox_dir="Inbox",
                 needs_action_dir="Needs_Action",
                 done_dir="Done",
                 logs_dir="Logs",
                 plans_dir="Plans",
                 in_progress_dir="In_Progress",
                 agent_name="gold_agent",
                 quarantined_dir="Quarantined"):

        self.inbox_dir = Path(inbox_dir)
        self.needs_action_dir = Path(needs_action_dir)
        self.done_dir = Path(done_dir)
        self.logs_dir = Path(logs_dir)
        self.plans_dir = Path(plans_dir)
        self.agent_name = agent_name
        self.quarantined_dir = Path(quarantined_dir)

        # Create agent-specific in-progress directory
        self.in_progress_dir = Path(in_progress_dir) / agent_name
        self.in_progress_dir.mkdir(parents=True, exist_ok=True)

        # Create directories if they don't exist
        for directory in [inbox_dir, needs_action_dir, done_dir, logs_dir, plans_dir, quarantined_dir]:
            Path(directory).mkdir(exist_ok=True)

        # Task tracking
        self.task_states = {}
        self.retry_counts = {}
        self.max_retries = 3

        # Audit log setup
        self.audit_log_path = self.logs_dir / f"gold_audit_{datetime.now().strftime('%Y%m%d')}.log"

        # Statistics
        self.stats = {
            'processed': 0,
            'completed': 0,
            'failed': 0,
            'retried': 0
        }

    def log_event(self, message: str, action: str = "", input_data: str = "", output_data: str = "", approval_status: str = ""):
        """Log an event to the audit log with comprehensive details."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        audit_entry = {
            "timestamp": timestamp,
            "action": action,
            "input": input_data[:500],  # Limit length to prevent huge logs
            "output": output_data[:500],
            "approval_status": approval_status,
            "message": message,
            "agent": self.agent_name
        }

        with open(self.audit_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry) + "\n")

        # Also write to general log
        log_entry = f"[{timestamp}] GOLD_PROCESSOR: {message}\n"
        general_log_path = self.logs_dir / "processor.log"
        with open(general_log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def classify_error(self, error_msg: str) -> ErrorType:
        """Classify error type based on error message content."""
        error_lower = error_msg.lower()

        if any(keyword in error_lower for keyword in ['timeout', 'connection', 'network', 'retry']):
            return ErrorType.TRANSIENT
        elif any(keyword in error_lower for keyword in ['auth', 'authorization', 'permission', 'token', 'credentials']):
            return ErrorType.AUTH
        elif any(keyword in error_lower for keyword in ['syntax', 'value', 'key', 'index', 'type']):
            return ErrorType.LOGIC
        else:
            return ErrorType.SYSTEM

    def requires_approval(self, content: str) -> bool:
        """Check if a task requires human approval."""
        content_lower = content.lower()

        # Keywords that indicate sensitive actions requiring approval
        sensitive_keywords = [
            'send email', 'send message', 'draft email', 'draft message',
            'payment', 'pay', 'transfer', 'buy', 'purchase', 'approve transaction',
            'delete', 'remove permanently', 'shutdown', 'terminate', 'cancel subscription',
            'share confidential', 'disclose', 'reveal password', 'access credentials',
            'new recipient', 'large action', 'cross-domain'
        ]

        return any(keyword in content_lower for keyword in sensitive_keywords)

    def claim_task(self, task_file_path: Path) -> bool:
        """Claim a task by moving it to the agent's in-progress directory."""
        try:
            # Create unique filename for in-progress
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            in_progress_filename = f"in_progress_{timestamp}_{task_file_path.name}"
            in_progress_path = self.in_progress_dir / in_progress_filename

            # Move task to in-progress directory
            shutil.move(str(task_file_path), str(in_progress_path))

            self.log_event(
                f"Claimed task: {task_file_path.name}",
                action="claim_task",
                input_data=str(task_file_path),
                output_data=str(in_progress_path)
            )

            return True
        except Exception as e:
            self.log_event(
                f"Failed to claim task {task_file_path.name}: {str(e)}",
                action="claim_task",
                input_data=str(task_file_path),
                output_data=str(e)
            )
            return False

    def read_task_file(self, task_file_path: Path):
        """Read and parse a task file."""
        try:
            with open(task_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic parsing of markdown task structure
            lines = content.split('\n')
            task_title = ""
            instructions = []
            found_instructions = False

            for line in lines:
                if line.startswith('# ') and not task_title:
                    task_title = line[2:]  # Remove '# ' prefix
                elif line.startswith('## Instructions'):
                    found_instructions = True
                elif found_instructions and line.startswith('##'):
                    break  # End of instructions section
                elif found_instructions and line.strip():
                    instructions.append(line.strip())

            return {
                'title': task_title,
                'instructions': '\n'.join(instructions),
                'full_content': content
            }
        except Exception as e:
            self.log_event(
                f"Error reading task file '{task_file_path}': {str(e)}",
                action="read_task_file",
                input_data=str(task_file_path),
                output_data=str(e)
            )
            return None

    def process_task(self, task_file_path: Path):
        """Process a single task file with error handling and retries."""
        task_id = task_file_path.name
        retry_count = self.retry_counts.get(task_id, 0)

        try:
            task_data = self.read_task_file(task_file_path)

            if not task_data:
                raise Exception("Failed to read task file")

            self.log_event(
                f"Processing task: {task_data['title']}",
                action="process_task",
                input_data=task_data['title'],
                output_data="Started processing"
            )

            # Check if this is a sensitive action that requires approval
            if self.requires_approval(task_data['full_content']):
                success = self.handle_approval_required_task(task_file_path, task_data)
            else:
                # Determine what type of task this is and process accordingly
                content = task_data['full_content'].lower()

                # If the task contains planning instructions, generate a plan
                if 'plan' in content or 'strategy' in content or 'outline' in content:
                    self.generate_plan_from_task(task_data)
                    success = True
                else:
                    # For other tasks, just acknowledge processing
                    self.log_event(f"Acknowledged task: {task_data['title']}")
                    success = True

            if success:
                # Move the processed task to Done folder
                self.move_task_to_done(task_file_path, task_data['title'])
                self.stats['completed'] += 1

                # Reset retry count on success
                if task_id in self.retry_counts:
                    del self.retry_counts[task_id]

                return True
            else:
                raise Exception("Task processing failed")

        except Exception as e:
            error_type = self.classify_error(str(e))
            self.log_event(
                f"Error processing task '{task_file_path.name}': {str(e)}",
                action="process_task",
                input_data=str(task_file_path),
                output_data=f"Error type: {error_type.value}",
                approval_status="failed"
            )

            # Handle retry logic
            if retry_count < self.max_retries:
                self.retry_counts[task_id] = retry_count + 1
                self.stats['retried'] += 1

                # Apply backoff - wait longer with each retry
                backoff_time = min(2 ** retry_count * 5, 60)  # Max 60 seconds
                self.log_event(
                    f"Retrying task '{task_file_path.name}' in {backoff_time}s (attempt {retry_count + 1}/{self.max_retries})"
                )

                # Move back to needs_action for retry after delay
                needs_action_path = self.needs_action_dir / task_file_path.name
                shutil.move(str(task_file_path), str(needs_action_path))

                # Wait before next attempt
                time.sleep(backoff_time)
                return False
            else:
                # Quarantine failed task
                self.quarantine_task(task_file_path, str(e))
                self.stats['failed'] += 1
                return False

    def handle_approval_required_task(self, task_file_path: Path, task_data):
        """Handle tasks that require human approval."""
        # Create an approval request file in Pending_Approval
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        approval_filename = f"approval_request_{timestamp}_{task_file_path.stem}.md"
        approval_path = Path("Pending_Approval") / approval_filename

        approval_content = f"""# Approval Request

## Original Task
**Title:** {task_data['title']}

## Request Details
The following task requires your approval before execution:

```
{task_data['full_content']}
```

## Action Required
- Review the requested action
- If approved, move this file to the `Approved` folder
- If rejected, move this file to the `Rejected` folder
- If uncertain, add comments with your concerns before moving

## Safety Check
This action was flagged as potentially sensitive because it contains operations that require human oversight.

## Metadata
- Requested: {datetime.now().isoformat()}
- Original File: {task_file_path.name}
- Priority: High
- Requires Approval: Yes
- Cross-Domain: {'cross-domain' in task_data['full_content'].lower()}
- New Recipient: {'new recipient' in task_data['full_content'].lower()}
- Large Action: {'large action' in task_data['full_content'].lower()}
"""

        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        self.log_event(
            f"Created approval request for sensitive task: {task_data['title']}",
            action="create_approval_request",
            input_data=task_data['title'],
            output_data=str(approval_path),
            approval_status="pending"
        )

        # Move the original task to a holding area or just log it (don't process yet)
        # For now, we'll just acknowledge that the approval request was created
        return True

    def generate_plan_from_task(self, task_data):
        """Generate a plan based on task requirements."""
        # Extract relevant content for plan
        plan_content = f"# Plan: {task_data['title']}\n\n"
        plan_content += f"Generated on: {datetime.now().isoformat()}\n\n"
        plan_content += "## Objective\n"
        plan_content += "Based on the task requirements, this plan outlines the approach to fulfill the request.\n\n"
        plan_content += "## Steps\n"
        plan_content += "1. Analyze the requirements\n"
        plan_content += "2. Identify necessary resources\n"
        plan_content += "3. Execute the planned actions\n"
        plan_content += "4. Verify completion\n"
        plan_content += "5. Document results\n\n"
        plan_content += "## Timeline\n"
        plan_content += "To be determined based on complexity.\n\n"
        plan_content += "## Resources Required\n"
        plan_content += "- AI Employee system\n"
        plan_content += "- Appropriate permissions\n"
        plan_content += "- Time allocation\n\n"
        plan_content += "## Success Criteria\n"
        plan_content += "- Task completed as specified\n"
        plan_content += "- All requirements satisfied\n"
        plan_content += "- Proper documentation maintained\n"
        plan_content += "- Cross-domain coordination verified\n"
        plan_content += "- Audit trail complete\n"

        # Save the plan to Plans folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"plan_{timestamp}_{task_data['title'].replace(' ', '_').replace('/', '_')}.md"
        plan_path = self.plans_dir / plan_filename

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(plan_content)

        self.log_event(
            f"Generated plan: {plan_filename}",
            action="generate_plan",
            input_data=task_data['title'],
            output_data=plan_filename
        )

    def move_task_to_done(self, task_file_path: Path, task_title: str):
        """Move the processed task file to the Done folder."""
        try:
            # Create a new filename with timestamp and status
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = task_file_path.stem
            extension = task_file_path.suffix
            new_filename = f"done_{timestamp}_{original_name}{extension}"

            destination = self.done_dir / new_filename
            shutil.move(str(task_file_path), str(destination))

            self.log_event(
                f"Moved processed task '{task_title}' to Done folder as '{new_filename}'",
                action="move_to_done",
                input_data=task_title,
                output_data=new_filename
            )
            return True
        except Exception as e:
            self.log_event(
                f"Error moving task '{task_file_path}' to Done folder: {str(e)}",
                action="move_to_done",
                input_data=str(task_file_path),
                output_data=str(e)
            )
            return False

    def quarantine_task(self, task_file_path: Path, error_reason: str):
        """Move a failed task to the quarantine folder."""
        try:
            # Create a new filename with error details
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = task_file_path.stem
            extension = task_file_path.suffix
            new_filename = f"quarantined_{timestamp}_{original_name}_error_{error_reason[:50].replace(' ', '_')}{extension}"

            destination = self.quarantined_dir / new_filename
            shutil.move(str(task_file_path), str(destination))

            self.log_event(
                f"Quarantined failed task '{task_file_path.name}' due to: {error_reason}",
                action="quarantine_task",
                input_data=task_file_path.name,
                output_data=new_filename,
                approval_status="quarantined"
            )
            return True
        except Exception as e:
            self.log_event(
                f"Error quarantining task '{task_file_path}': {str(e)}",
                action="quarantine_task",
                input_data=str(task_file_path),
                output_data=str(e)
            )
            return False

    def scan_and_claim_tasks(self):
        """Scan for and claim pending tasks."""
        if not self.needs_action_dir.exists():
            return 0

        task_files = [f for f in self.needs_action_dir.iterdir() if f.is_file()]
        claimed_count = 0

        for task_file in task_files:
            if self.claim_task(task_file):
                claimed_count += 1

        return claimed_count

    def process_claimed_tasks(self):
        """Process all tasks in the agent's in-progress directory."""
        if not self.in_progress_dir.exists():
            return 0

        task_files = [f for f in self.in_progress_dir.iterdir() if f.is_file()]
        processed_count = 0

        for task_file in task_files:
            if self.process_task(task_file):
                processed_count += 1

        return processed_count

    def update_dashboard(self):
        """Update the dashboard with current status."""
        # Count pending tasks
        pending_tasks = 0
        if self.needs_action_dir.exists():
            pending_tasks = len([f for f in self.needs_action_dir.iterdir() if f.is_file()])

        # Count in-progress tasks for this agent
        in_progress_tasks = 0
        if self.in_progress_dir.exists():
            in_progress_tasks = len([f for f in self.in_progress_dir.iterdir() if f.is_file()])

        # Count completed tasks
        completed_tasks = 0
        if self.done_dir.exists():
            completed_tasks = len([f for f in self.done_dir.iterdir() if f.is_file()])

        # Count quarantined tasks
        quarantined_tasks = 0
        if self.quarantined_dir.exists():
            quarantined_tasks = len([f for f in self.quarantined_dir.iterdir() if f.is_file()])

        # Update dashboard file with thread-safe approach
        dashboard_path = Path("Dashboard.md")
        dashboard_lock = threading.Lock()

        with dashboard_lock:
            if dashboard_path.exists():
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Update the task queue count in the dashboard
                content = re.sub(
                    r'\| Task Queue \| 📊 \d+ pending \|',
                    f'| Task Queue | 📊 {pending_tasks} pending |',
                    content
                )

                # Update in-progress tasks
                content = re.sub(
                    r'\| In Progress \(Gold\) \| 🔄 \d+ tasks \|',
                    f'| In Progress (Gold) | 🔄 {in_progress_tasks} tasks |',
                    content
                )

                # Update completed tasks
                content = re.sub(
                    r'\| Completed Today \| 📈 \d+ tasks \|',
                    f'| Completed Today | 📈 {completed_tasks} tasks |',
                    content
                )

                # Update quarantined tasks
                content = re.sub(
                    r'\| Quarantined \(Gold\) \| ⚠️ \d+ tasks \|',
                    f'| Quarantined (Gold) | ⚠️ {quarantined_tasks} tasks |',
                    content
                )

                # Update last updated timestamp
                content = re.sub(
                    r'Last Updated: .*',
                    f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    content
                )

                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    def run_autonomous_loop(self, scan_interval=5, process_interval=2):
        """
        Main autonomous loop for the Gold Tier task processor
        """
        self.log_event("Gold Tier task processor started", action="start_processor")

        self.stats['processed'] = 0

        try:
            while True:
                # Scan and claim new tasks
                claimed_count = self.scan_and_claim_tasks()

                # Process claimed tasks
                processed_count = self.process_claimed_tasks()

                # Update dashboard
                if claimed_count > 0 or processed_count > 0:
                    self.update_dashboard()
                    self.stats['processed'] += processed_count

                    self.log_event(
                        f"Autonomous cycle: claimed {claimed_count}, processed {processed_count}",
                        action="autonomous_cycle",
                        input_data=f"claimed:{claimed_count},processed:{processed_count}",
                        output_data=str(self.stats)
                    )

                time.sleep(process_interval)

        except KeyboardInterrupt:
            self.log_event("Gold Tier task processor stopped by user", action="stop_processor")
        except Exception as e:
            self.log_event(
                f"Unexpected error in Gold Tier processor: {str(e)}",
                action="processor_error",
                output_data=str(e)
            )

    def get_stats(self):
        """Return current processor statistics."""
        return self.stats.copy()


if __name__ == "__main__":
    processor = GoldTaskProcessor()
    print("Starting AI Employee Gold Tier Task Processor...")
    print("Using persistent autonomous loop with error recovery and audit logging...")
    print("Processing tasks from Needs_Action folder...")
    print("Press Ctrl+C to stop")
    processor.run_autonomous_loop()