"""
Approval Monitor for AI Employee Silver Tier
Monitors the Pending_Approval, Approved, and Rejected folders for approval workflow.
"""

import time
from datetime import datetime
from pathlib import Path
import shutil


class ApprovalMonitor:
    """
    Monitors approval workflow folders and processes approved/rejected tasks.
    """

    def __init__(self, pending_dir="Pending_Approval", approved_dir="Approved",
                 rejected_dir="Rejected", needs_action_dir="Needs_Action",
                 done_dir="Done", logs_dir="Logs"):
        self.pending_dir = Path(pending_dir)
        self.approved_dir = Path(approved_dir)
        self.rejected_dir = Path(rejected_dir)
        self.needs_action_dir = Path(needs_action_dir)
        self.done_dir = Path(done_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories if they don't exist
        for directory in [pending_dir, approved_dir, rejected_dir, needs_action_dir, done_dir, logs_dir]:
            Path(directory).mkdir(exist_ok=True)

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] APPROVAL_MONITOR: {message}\n"

        log_file = self.logs_dir / "approval_monitor.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    def process_approved_tasks(self):
        """Process tasks that have been approved"""
        if not self.approved_dir.exists():
            return 0

        approved_files = [f for f in self.approved_dir.iterdir() if f.is_file() and f.suffix == '.md']
        processed_count = 0

        for file_path in approved_files:
            try:
                # Read the approval request file to extract original task content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract the original task content from the approval request
                # Find the content between triple backticks after "Request Details"
                import re
                pattern = r'## Request Details\nThe following task requires your approval before execution:\n\n```(?:markdown)?\n(.*?)\n```'
                match = re.search(pattern, content, re.DOTALL)

                if match:
                    original_task_content = match.group(1)

                    # Create a new task file in Needs_Action for processing
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_task_filename = f"approved_task_{timestamp}_{file_path.stem.replace('approval_request_', '')}.md"
                    new_task_path = self.needs_action_dir / new_task_filename

                    with open(new_task_path, 'w', encoding='utf-8') as f:
                        f.write(original_task_content)

                    self.log_event(f"Moved approved task to Needs_Action: {new_task_filename}")

                    # Move the approval request to Done folder
                    done_filename = f"processed_{timestamp}_{file_path.name}"
                    done_path = self.done_dir / done_filename
                    shutil.move(str(file_path), str(done_path))

                    processed_count += 1
                else:
                    self.log_event(f"Could not extract original task from approval request: {file_path.name}")

            except Exception as e:
                self.log_event(f"Error processing approved task '{file_path.name}': {str(e)}")

        return processed_count

    def process_rejected_tasks(self):
        """Process tasks that have been rejected"""
        if not self.rejected_dir.exists():
            return 0

        rejected_files = [f for f in self.rejected_dir.iterdir() if f.is_file() and f.suffix == '.md']
        processed_count = 0

        for file_path in rejected_files:
            try:
                # Move the rejection request to Done folder with rejected status
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                done_filename = f"rejected_{timestamp}_{file_path.name}"
                done_path = self.done_dir / done_filename
                shutil.move(str(file_path), str(done_path))

                self.log_event(f"Moved rejected task to Done: {done_filename}")
                processed_count += 1

            except Exception as e:
                self.log_event(f"Error processing rejected task '{file_path.name}': {str(e)}")

        return processed_count

    def run(self, interval=10):
        """
        Main loop for the approval monitor
        :param interval: Time in seconds between checks
        """
        self.log_event("Approval monitor started")

        try:
            while True:
                # Process approved tasks
                approved_count = self.process_approved_tasks()

                # Process rejected tasks
                rejected_count = self.process_rejected_tasks()

                if approved_count > 0 or rejected_count > 0:
                    self.log_event(f"Processed {approved_count} approved and {rejected_count} rejected tasks")

                time.sleep(interval)

        except KeyboardInterrupt:
            self.log_event("Approval monitor stopped by user")
        except Exception as e:
            self.log_event(f"Unexpected error in approval monitor: {str(e)}")


if __name__ == "__main__":
    monitor = ApprovalMonitor()
    print("Starting AI Employee Approval Monitor...")
    print("Monitoring Pending_Approval, Approved, and Rejected folders...")
    print("Press Ctrl+C to stop")
    monitor.run()