import time
from datetime import datetime
from pathlib import Path

class FileSystemWatcher:
    """
    A simple file system watcher for the AI Employee Bronze Tier.
    Monitors the Inbox folder and creates task files in Needs_Action when new files are detected.
    """

    def __init__(self, inbox_dir="Inbox", needs_action_dir="Needs_Action", logs_dir="Logs"):
        self.inbox_dir = Path(inbox_dir)
        self.needs_action_dir = Path(needs_action_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories if they don't exist
        self.inbox_dir.mkdir(exist_ok=True)
        self.needs_action_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Track files that have already been processed
        self.processed_files = set()
        self.load_processed_files()

    def load_processed_files(self):
        """Load the set of already processed files from a tracking file"""
        tracker_file = self.logs_dir / ".processed_files_tracker"
        if tracker_file.exists():
            with open(tracker_file, 'r') as f:
                self.processed_files = set(line.strip() for line in f.readlines())

    def save_processed_files(self):
        """Save the set of processed files to a tracking file"""
        tracker_file = self.logs_dir / ".processed_files_tracker"
        with open(tracker_file, 'w') as f:
            for filename in self.processed_files:
                f.write(f"{filename}\n")

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        log_file = self.logs_dir / "watcher.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    def create_task_file(self, source_file_path):
        """Create a structured task file in Needs_Action based on the detected file"""
        source_file = Path(source_file_path)

        # Create a unique task filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_filename = f"task_{timestamp}_{source_file.name}.md"
        task_path = self.needs_action_dir / task_filename

        # Read the source file content if it's a text file
        try:
            with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read(1000)  # Limit to first 1000 chars to prevent huge files
        except:
            file_content = f"Detected new file: {source_file.name}"

        # Create structured task content
        task_content = f"""# Task: Process File "{source_file.name}"

## Source
- File: `{source_file.name}`
- Location: `{str(source_file)}`
- Detected: `{datetime.now().isoformat()}`

## Instructions
Process the following content and take appropriate action:

```
{file_content[:500]}{'...' if len(file_content) > 500 else ''}
```

## Expected Outcomes
- Analyze the content
- Determine appropriate response
- Perform necessary actions
- Update dashboard with results

## Metadata
- Priority: Normal
- Type: File Processing
- Source: File System Watcher
"""

        # Write the task file
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(task_content)

        self.log_event(f"Created task file '{task_filename}' for source file '{source_file.name}'")
        return task_path

    def scan_inbox(self):
        """Scan the inbox directory for new files"""
        new_files = []

        if not self.inbox_dir.exists():
            self.log_event("Inbox directory does not exist")
            return new_files

        for file_path in self.inbox_dir.iterdir():
            if file_path.is_file():
                file_key = str(file_path.relative_to(self.inbox_dir))

                # Check if this file has already been processed
                if file_key not in self.processed_files:
                    new_files.append(file_path)

        return new_files

    def update_dashboard(self):
        """Update the dashboard with current status"""
        # Count pending tasks
        pending_tasks = 0
        if self.needs_action_dir.exists():
            pending_tasks = len([f for f in self.needs_action_dir.iterdir() if f.is_file()])

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
        Main loop for the file system watcher
        :param interval: Time in seconds between scans
        """
        self.log_event("File system watcher started")

        try:
            while True:
                new_files = self.scan_inbox()

                for file_path in new_files:
                    try:
                        self.create_task_file(file_path)
                        file_key = str(file_path.relative_to(self.inbox_dir))
                        self.processed_files.add(file_key)
                    except Exception as e:
                        self.log_event(f"Error processing file '{file_path}': {str(e)}")

                if new_files:
                    self.save_processed_files()
                    self.update_dashboard()

                time.sleep(interval)

        except KeyboardInterrupt:
            self.log_event("File system watcher stopped by user")
        except Exception as e:
            self.log_event(f"Unexpected error in watcher: {str(e)}")


if __name__ == "__main__":
    watcher = FileSystemWatcher()
    print("Starting AI Employee File System Watcher...")
    print("Monitoring Inbox folder for new files...")
    print("Press Ctrl+C to stop")
    watcher.run()