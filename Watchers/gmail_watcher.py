"""
Gmail Watcher for AI Employee Silver Tier
Monitors Gmail inbox for new emails and creates structured task files in Needs_Action.
"""

import time
import json
from datetime import datetime
from pathlib import Path


class GmailWatcher:
    """
    A Gmail watcher for the AI Employee Silver Tier.
    Simulates monitoring a Gmail inbox and creates task files in Needs_Action when new emails are detected.
    NOTE: This is a simulation that creates sample emails to demonstrate the concept.
    In a real implementation, this would connect to Gmail API.
    """

    def __init__(self, needs_action_dir="Needs_Action", logs_dir="Logs"):
        self.needs_action_dir = Path(needs_action_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories if they don't exist
        self.needs_action_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Track emails that have already been processed
        self.processed_emails = set()
        self.load_processed_emails()

        # Simulate email data for demonstration
        self.simulated_emails = [
            {
                "id": "email_001",
                "subject": "Project Update Request",
                "sender": "manager@company.com",
                "timestamp": "2026-02-04T10:30:00Z",
                "body": "Hi, please provide an update on the quarterly project. Include budget status and timeline projections."
            },
            {
                "id": "email_002",
                "subject": "Meeting Follow-up",
                "sender": "colleague@company.com",
                "timestamp": "2026-02-04T11:15:00Z",
                "body": "Following up on our meeting yesterday. Could you please send the presentation materials and action items?"
            }
        ]

    def load_processed_emails(self):
        """Load the set of already processed emails from a tracking file"""
        tracker_file = self.logs_dir / ".processed_emails_tracker"
        if tracker_file.exists():
            with open(tracker_file, 'r') as f:
                self.processed_emails = set(line.strip() for line in f.readlines())

    def save_processed_emails(self):
        """Save the set of processed emails to a tracking file"""
        tracker_file = self.logs_dir / ".processed_emails_tracker"
        with open(tracker_file, 'w') as f:
            for email_id in self.processed_emails:
                f.write(f"{email_id}\n")

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] GMAIL_WATCHER: {message}\n"

        log_file = self.logs_dir / "gmail_watcher.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    def create_task_file(self, email_data):
        """Create a structured task file in Needs_Action based on the detected email"""
        # Create a unique task filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_filename = f"gmail_task_{timestamp}_{email_data['id']}.md"
        task_path = self.needs_action_dir / task_filename

        # Create structured task content
        task_content = f"""# Task: Process Email "{email_data['subject']}"

## Source
- Email ID: `{email_data['id']}`
- Sender: `{email_data['sender']}`
- Subject: `{email_data['subject']}`
- Received: `{email_data['timestamp']}`

## Email Content
{email_data['body']}

## Instructions
Process the following email content and take appropriate action:

```
From: {email_data['sender']}
Subject: {email_data['subject']}
Date: {email_data['timestamp']}

{email_data['body']}
```

## Expected Outcomes
- Analyze the email content
- Determine appropriate response or action
- Generate necessary documents or reports if requested
- Update dashboard with results

## Metadata
- Priority: Normal
- Type: Email Processing
- Source: Gmail Watcher
- Classification: Need to respond to email request
"""

        # Write the task file
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(task_content)

        self.log_event(f"Created task file '{task_filename}' for email '{email_data['subject']}'")
        return task_path

    def simulate_check_new_emails(self):
        """Simulate checking for new emails (in real implementation, this would use Gmail API)"""
        new_emails = []

        for email in self.simulated_emails:
            if email['id'] not in self.processed_emails:
                # Check if it's a "recent" email (for demo purposes, all are recent)
                new_emails.append(email)

        return new_emails

    def run(self, interval=30):
        """
        Main loop for the Gmail watcher
        :param interval: Time in seconds between email checks
        """
        self.log_event("Gmail watcher started")

        try:
            while True:
                new_emails = self.simulate_check_new_emails()

                for email in new_emails:
                    try:
                        self.create_task_file(email)
                        self.processed_emails.add(email['id'])
                    except Exception as e:
                        self.log_event(f"Error processing email '{email['id']}': {str(e)}")

                if new_emails:
                    self.save_processed_emails()

                time.sleep(interval)

        except KeyboardInterrupt:
            self.log_event("Gmail watcher stopped by user")
        except Exception as e:
            self.log_event(f"Unexpected error in Gmail watcher: {str(e)}")


if __name__ == "__main__":
    watcher = GmailWatcher()
    print("Starting AI Employee Gmail Watcher...")
    print("Monitoring Gmail for new emails...")
    print("(This is a simulation - in production, this would connect to Gmail API)")
    print("Press Ctrl+C to stop")
    watcher.run()