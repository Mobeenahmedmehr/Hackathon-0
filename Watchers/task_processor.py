import time
from datetime import datetime
from pathlib import Path
import shutil
import re

class TaskProcessor:
    """
    Processes tasks from Needs_Action folder and moves them to Done folder after processing.
    """

    def __init__(self, needs_action_dir="Needs_Action", done_dir="Done", logs_dir="Logs", plans_dir="Plans"):
        self.needs_action_dir = Path(needs_action_dir)
        self.done_dir = Path(done_dir)
        self.logs_dir = Path(logs_dir)
        self.plans_dir = Path(plans_dir)

        # Create directories if they don't exist
        self.needs_action_dir.mkdir(exist_ok=True)
        self.done_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.plans_dir.mkdir(exist_ok=True)

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        log_file = self.logs_dir / "processor.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    def read_task_file(self, task_file_path):
        """Read and parse a task file"""
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
            self.log_event(f"Error reading task file '{task_file_path}': {str(e)}")
            return None

    def process_task(self, task_file_path):
        """Process a single task file"""
        task_data = self.read_task_file(task_file_path)

        if not task_data:
            return False

        self.log_event(f"Processing task: {task_data['title']}")

        # Check if this is a sensitive action that requires approval
        if self.requires_approval(task_data['full_content']):
            return self.handle_approval_required_task(task_file_path, task_data)

        # Determine what type of task this is and process accordingly
        content = task_data['full_content'].lower()

        # If the task contains planning instructions, generate a plan
        if 'plan' in content or 'strategy' in content or 'outline' in content:
            self.generate_plan_from_task(task_data)
        else:
            # For other tasks, just acknowledge processing
            self.log_event(f"Acknowledged task: {task_data['title']}")

        # Move the processed task to Done folder
        return self.move_task_to_done(task_file_path, task_data['title'])

    def requires_approval(self, content):
        """Check if a task requires human approval"""
        content_lower = content.lower()

        # Keywords that indicate sensitive actions requiring approval
        sensitive_keywords = [
            'send email', 'send message', 'draft email', 'draft message',
            'payment', 'pay', 'transfer', 'buy', 'purchase', 'approve transaction',
            'delete', 'remove permanently', 'shutdown', 'terminate', 'cancel subscription',
            'share confidential', 'disclose', 'reveal password', 'access credentials'
        ]

        return any(keyword in content_lower for keyword in sensitive_keywords)

    def handle_approval_required_task(self, task_file_path, task_data):
        """Handle tasks that require human approval"""
        # Create an approval request file in Pending_Approval
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        approval_filename = f"approval_request_{timestamp}_{Path(task_file_path).stem}.md"
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
- Priority: Medium
"""

        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        self.log_event(f"Created approval request for sensitive task: {task_data['title']}")

        # Move the original task to a holding area or just log it (don't process yet)
        # For now, we'll just acknowledge that the approval request was created
        return True

    def generate_plan_from_task(self, task_data):
        """Generate a plan based on task requirements"""
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

        # Save the plan to Plans folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"plan_{timestamp}_{task_data['title'].replace(' ', '_').replace('/', '_')}.md"
        plan_path = self.plans_dir / plan_filename

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(plan_content)

        self.log_event(f"Generated plan: {plan_filename}")

    def move_task_to_done(self, task_file_path, task_title):
        """Move the processed task file to the Done folder"""
        try:
            # Create a new filename with timestamp and status
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = Path(task_file_path).stem
            extension = Path(task_file_path).suffix
            new_filename = f"done_{timestamp}_{original_name}{extension}"

            destination = self.done_dir / new_filename
            shutil.move(str(task_file_path), str(destination))

            self.log_event(f"Moved processed task '{task_title}' to Done folder as '{new_filename}'")
            return True
        except Exception as e:
            self.log_event(f"Error moving task '{task_file_path}' to Done folder: {str(e)}")
            return False

    def scan_and_process_tasks(self):
        """Scan for and process all pending tasks"""
        if not self.needs_action_dir.exists():
            return 0

        task_files = [f for f in self.needs_action_dir.iterdir() if f.is_file()]
        processed_count = 0

        for task_file in task_files:
            if self.process_task(task_file):
                processed_count += 1

        return processed_count

    def update_dashboard(self):
        """Update the dashboard with current status"""
        # Count pending tasks
        pending_tasks = 0
        if self.needs_action_dir.exists():
            pending_tasks = len([f for f in self.needs_action_dir.iterdir() if f.is_file()])

        # Count completed tasks
        completed_tasks = 0
        if self.done_dir.exists():
            completed_tasks = len([f for f in self.done_dir.iterdir() if f.is_file()])

        # Update dashboard file
        dashboard_path = Path("Dashboard.md")
        if dashboard_path.exists():
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update the task queue count in the dashboard
            import re
            content = re.sub(
                r'\| Task Queue \| 📊 \d+ pending \|',
                f'| Task Queue | 📊 {pending_tasks} pending |',
                content
            )

            # Update completed tasks
            content = re.sub(
                r'\| Completed Today \| 📈 \d+ tasks \|',
                f'| Completed Today | 📈 {completed_tasks} tasks |',
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

    def run(self, interval=5):
        """
        Main loop for the task processor
        :param interval: Time in seconds between scans
        """
        self.log_event("Task processor started")

        try:
            while True:
                processed_count = self.scan_and_process_tasks()

                if processed_count > 0:
                    self.log_event(f"Processed {processed_count} tasks")
                    self.update_dashboard()

                time.sleep(interval)

        except KeyboardInterrupt:
            self.log_event("Task processor stopped by user")
        except Exception as e:
            self.log_event(f"Unexpected error in processor: {str(e)}")


if __name__ == "__main__":
    processor = TaskProcessor()
    print("Starting AI Employee Task Processor...")
    print("Processing tasks from Needs_Action folder...")
    print("Press Ctrl+C to stop")
    processor.run()