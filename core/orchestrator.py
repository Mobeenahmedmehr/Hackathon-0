import os
import time
import shutil
from datetime import datetime
from pathlib import Path
import logging

from config.config_loader import load_config
from utils.paths import (
    get_needs_action_path, get_plans_path, get_pending_approval_path,
    get_approved_path, get_drafts_path, get_done_path, get_errors_path
)
from logging_setup import get_logger
from ai.reasoner import ai_reasoner
from .task_manager import TaskManager
from .plan_parser import PlanParser


class Orchestrator:
    """
    Main control loop of the AI employee.
    Monitors the system and coordinates task processing.
    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self.task_manager = TaskManager()
        self.plan_parser = PlanParser()

        # Ensure all required directories exist
        for path_func in [get_needs_action_path, get_plans_path, get_pending_approval_path,
                         get_approved_path, get_drafts_path, get_done_path, get_errors_path]:
            path = path_func()
            Path(path).mkdir(parents=True, exist_ok=True)

    def scan_new_tasks(self):
        """
        Scan Needs_Action directory.
        For each task file:
        - call ai_reasoner.generate_plan()
        - Move task to Plans/
        Return list of generated plans.
        """
        logger = self.logger
        needs_action_path = get_needs_action_path()
        plans_path = get_plans_path()

        task_files = []
        for file_path in Path(needs_action_path).iterdir():
            if file_path.is_file() and file_path.suffix == '.md':
                task_files.append(file_path)

        logger.info(f"Found {len(task_files)} new tasks to process")

        generated_plans = []
        for task_file in task_files:
            try:
                # Generate plan using AI reasoner
                plan_content = ai_reasoner.generate_plan(str(task_file))

                # Create plan file in Plans directory
                plan_filename = f"plan_{task_file.stem}_{int(time.time())}.md"
                plan_path = os.path.join(plans_path, plan_filename)

                with open(plan_path, 'w', encoding='utf-8') as f:
                    f.write(plan_content)

                # Move the original task to Plans directory as well
                moved_task_path = os.path.join(plans_path, f"task_{task_file.name}")
                shutil.move(str(task_file), moved_task_path)

                generated_plans.append(plan_path)
                logger.info(f"Generated plan for task: {task_file.name}")

            except Exception as e:
                logger.error(f"Failed to generate plan for task {task_file.name}: {str(e)}")
                # Move task to errors folder
                error_path = get_errors_path()
                error_task_path = os.path.join(error_path, f"error_{task_file.name}")
                shutil.move(str(task_file), error_task_path)

        return generated_plans

    def send_for_approval(self, plan_path):
        """
        Move plan file to Pending_Approval/
        Add approval metadata to the plan file header:
        Approval Status: Pending
        Created Time:
        Requested By: AI Employee
        """
        logger = self.logger
        pending_approval_path = get_pending_approval_path()

        # Read the current plan content
        with open(plan_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Prepare approval metadata
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        approval_metadata = f"""---
Approval Status: Pending
Created Time: {current_time}
Requested By: AI Employee
---

"""

        # Combine metadata with original content
        updated_content = approval_metadata + original_content

        # Write back to the plan file
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Move the plan file to Pending_Approval directory
        plan_filename = os.path.basename(plan_path)
        new_plan_path = os.path.join(pending_approval_path, plan_filename)
        shutil.move(plan_path, new_plan_path)

        logger.info(f"Sent plan for approval: {plan_filename}")
        return new_plan_path

    def check_approved_plans(self):
        """
        Monitor Approved directory.
        Return list of plans ready for execution.
        """
        logger = self.logger
        approved_path = get_approved_path()

        approved_plans = []
        for file_path in Path(approved_path).iterdir():
            if file_path.is_file() and file_path.suffix == '.md':
                # Check if the plan has approval metadata indicating it's approved
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for approval status in the header
                if "Approval Status: Approved" in content or "---\nApproval Status: Approved" in content:
                    approved_plans.append(str(file_path))

        logger.info(f"Found {len(approved_plans)} approved plans ready for execution")
        return approved_plans

    def execute_plan(self, plan_path):
        """
        Read plan content.
        Extract:
        - Recommended Agent
        - Tools Required
        - Steps

        Send plan to the agent executor.
        Save outputs in Drafts/ or Done/
        """
        logger = self.logger

        try:
            # Read plan content
            with open(plan_path, 'r', encoding='utf-8') as f:
                plan_content = f.read()

            # Parse the plan
            parsed_plan = self.plan_parser.parse_plan(plan_content)

            if not parsed_plan:
                logger.error(f"Could not parse plan: {plan_path}")
                return False

            logger.info(f"Executing plan: {parsed_plan.get('goal', 'Unknown')} with agent: {parsed_plan.get('recommended_agent', 'Unknown')}")

            # Extract plan components
            recommended_agent = parsed_plan.get('recommended_agent', 'default')
            tools_required = parsed_plan.get('tools_required', [])
            steps = parsed_plan.get('steps', [])

            # Execute the plan steps (this would involve calling the appropriate agents/tools)
            execution_success = True
            execution_output = []

            # In a real implementation, this would call the actual agent execution logic
            # For now, we'll simulate execution
            for step_idx, step in enumerate(steps):
                logger.info(f"Executing step {step_idx + 1}: {step[:50]}...")
                # Simulate step execution
                execution_output.append(f"Step {step_idx + 1} completed: {step}")

            # Determine output destination based on plan type
            if parsed_plan.get('task_type') == 'draft':
                output_dir = get_drafts_path()
            else:
                output_dir = get_done_path()

            # Save execution output
            plan_filename = os.path.basename(plan_path)
            output_filename = f"executed_{plan_filename}"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Execution Report\n\n")
                f.write(f"Plan executed: {plan_filename}\n")
                f.write(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Original Plan\n{plan_content}\n\n")
                f.write(f"## Execution Output\n")
                for output in execution_output:
                    f.write(f"- {output}\n")

            # Remove the plan from Approved directory after execution
            os.remove(plan_path)

            logger.info(f"Plan executed successfully, output saved to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to execute plan {plan_path}: {str(e)}")
            # Move to errors folder
            error_path = get_errors_path()
            error_plan_path = os.path.join(error_path, f"execution_error_{os.path.basename(plan_path)}")
            shutil.move(plan_path, error_plan_path)
            return False

    def orchestrator_cycle(self):
        """
        Pipeline:
        - scan new tasks
        - generate plans
        - move plans to Pending_Approval
        - check Approved plans
        - execute them
        - log results
        """
        logger = self.logger

        logger.info("Starting orchestrator cycle")

        # Scan for new tasks and generate plans
        new_plans = self.scan_new_tasks()
        logger.info(f"Generated {len(new_plans)} new plans")

        # Send new plans for approval
        for plan_path in new_plans:
            try:
                self.send_for_approval(plan_path)
            except Exception as e:
                logger.error(f"Failed to send plan for approval {plan_path}: {str(e)}")

        # Check for approved plans and execute them
        approved_plans = self.check_approved_plans()
        logger.info(f"Found {len(approved_plans)} approved plans to execute")

        executed_count = 0
        for plan_path in approved_plans:
            try:
                if self.execute_plan(plan_path):
                    executed_count += 1
            except Exception as e:
                logger.error(f"Failed to execute plan {plan_path}: {str(e)}")

        logger.info(f"Orchestrator cycle completed: {len(new_plans)} plans generated, {executed_count} plans executed")

        return {
            'new_plans_generated': len(new_plans),
            'approved_plans_executed': executed_count,
            'total_approved_plans_found': len(approved_plans)
        }

    def run_autonomous_loop(self):
        """
        Continuous system loop:
        while True:
            orchestrator_cycle()
            sleep(30)
        """
        logger = self.logger

        logger.info("Starting autonomous orchestrator loop")

        while True:
            try:
                cycle_results = self.orchestrator_cycle()
                time.sleep(30)  # Wait 30 seconds before next cycle

            except KeyboardInterrupt:
                logger.info("Orchestrator loop interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in orchestrator loop: {str(e)}")
                time.sleep(30)  # Wait before retrying


def orchestrator_cycle():
    """
    Standalone function to run a single orchestrator cycle.
    """
    orchestrator = Orchestrator()
    return orchestrator.orchestrator_cycle()


def run_autonomous_loop():
    """
    Standalone function to run the continuous orchestrator loop.
    """
    orchestrator = Orchestrator()
    orchestrator.run_autonomous_loop()


if __name__ == "__main__":
    print("Starting AI Employee Orchestrator...")
    print("Running autonomous loop...")
    run_autonomous_loop()