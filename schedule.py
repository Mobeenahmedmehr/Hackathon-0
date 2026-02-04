"""
Scheduler for AI Employee Silver Tier
Implements basic scheduling functionality for recurring tasks.
"""

import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
import json


class Scheduler:
    """
    A basic scheduler for the AI Employee Silver Tier.
    Implements timestamp-based checks for recurring tasks like daily summaries and weekly reviews.
    """

    def __init__(self, inbox_dir="Inbox", logs_dir="Logs"):
        self.inbox_dir = Path(inbox_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories if they don't exist
        self.inbox_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Schedule configuration
        self.scheduled_tasks = {
            "daily_summary": {
                "interval_hours": 24,
                "last_run": None,
                "enabled": True
            },
            "weekly_review": {
                "interval_hours": 168,  # 7 days
                "last_run": None,
                "enabled": True
            }
        }

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] SCHEDULER: {message}\n"

        log_file = self.logs_dir / "scheduler.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    def create_daily_summary_request(self):
        """Create a task file requesting a daily summary"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_filename = f"daily_summary_request_{timestamp}.md"
        task_path = self.inbox_dir / task_filename

        task_content = f"""# Daily Summary Request

## Objective
Generate a daily summary of activities, completed tasks, and upcoming priorities for {datetime.now().strftime('%Y-%m-%d')}.

## Requirements
- Review all completed tasks from the past 24 hours
- Summarize key accomplishments
- Identify any outstanding items requiring attention
- Format as a clear, concise summary

## Expected Output
- Daily summary document in markdown format
- Key metrics and statistics
- Priorities for the upcoming day

## Timeline
Complete within 2 business hours of receipt.

## Metadata
- Priority: Normal
- Type: Daily Report
- Source: Automated Scheduler
"""

        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(task_content)

        self.log_event(f"Created daily summary request: {task_filename}")

    def create_weekly_review_request(self):
        """Create a task file requesting a weekly review"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_filename = f"weekly_review_request_{timestamp}.md"
        task_path = self.inbox_dir / task_filename

        task_content = f"""# Weekly Review Request

## Objective
Generate a weekly review of activities, completed tasks, and upcoming priorities for week ending {datetime.now().strftime('%Y-%m-%d')}.

## Requirements
- Review all completed tasks from the past 7 days
- Summarize key accomplishments and milestones
- Analyze productivity trends and patterns
- Identify areas for improvement
- Set priorities for the upcoming week

## Expected Output
- Weekly review document in markdown format
- Performance metrics and KPIs
- Strategic insights and recommendations
- Action items for the next week

## Timeline
Complete within 4 business hours of receipt.

## Metadata
- Priority: Medium
- Type: Weekly Report
- Source: Automated Scheduler
"""

        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(task_content)

        self.log_event(f"Created weekly review request: {task_filename}")

    def check_and_execute_scheduled_tasks(self):
        """Check if scheduled tasks need to be executed"""
        current_time = datetime.now()

        for task_name, config in self.scheduled_tasks.items():
            if not config["enabled"]:
                continue

            # Calculate next run time
            if config["last_run"] is None:
                # First run - execute immediately
                should_run = True
            else:
                next_run = config["last_run"] + timedelta(hours=config["interval_hours"])
                should_run = current_time >= next_run

            if should_run:
                if task_name == "daily_summary":
                    self.create_daily_summary_request()
                elif task_name == "weekly_review":
                    self.create_weekly_review_request()

                # Update last run time
                self.scheduled_tasks[task_name]["last_run"] = current_time
                self.log_event(f"Executed scheduled task: {task_name}")

    def run_scheduler(self, check_interval=3600):  # Check every hour
        """Run the scheduler in a loop"""
        self.log_event("Scheduler started")

        try:
            while True:
                self.check_and_execute_scheduled_tasks()

                # Sleep for the check interval
                time.sleep(check_interval)

        except KeyboardInterrupt:
            self.log_event("Scheduler stopped by user")
        except Exception as e:
            self.log_event(f"Unexpected error in scheduler: {str(e)}")

    def start_background_scheduler(self):
        """Start the scheduler in a background thread"""
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        return scheduler_thread


if __name__ == "__main__":
    scheduler = Scheduler()
    print("Starting AI Employee Scheduler...")
    print("Monitoring for scheduled tasks...")
    print("Press Ctrl+C to stop")
    scheduler.run_scheduler()