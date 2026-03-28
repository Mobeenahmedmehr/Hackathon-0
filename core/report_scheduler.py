import os
import schedule
import time
from datetime import datetime
import logging
from pathlib import Path

from auditor.auditor_runner import generate_weekly_report

logger = logging.getLogger(__name__)

def run_report_scheduler():
    """
    Automatically generate reports on a weekly basis.
    Runs the auditor every Sunday.
    """
    def job():
        logger.info("Starting weekly report generation job...")
        try:
            report_path = generate_weekly_report()
            logger.info(f"Successfully generated weekly report: {report_path}")
        except Exception as e:
            logger.error(f"Error generating weekly report: {str(e)}")

    # Schedule the job to run every Sunday at midnight
    schedule.every().sunday.at("00:00").do(job)

    logger.info("Report scheduler started. Waiting for scheduled time...")

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour

def is_sunday_and_midnight():
    """
    Check if today is Sunday and the time is midnight.
    Alternative to using schedule library if preferred.
    """
    now = datetime.now()
    return now.weekday() == 6 and now.hour == 0  # Sunday is 6, midnight is 0

def run_if_sunday():
    """
    Run the auditor if today is Sunday at midnight.
    """
    if is_sunday_and_midnight():
        logger.info("Today is Sunday at midnight. Running weekly report generation...")
        try:
            report_path = generate_weekly_report()
            logger.info(f"Successfully generated weekly report: {report_path}")
        except Exception as e:
            logger.error(f"Error generating weekly report: {str(e)}")

if __name__ == "__main__":
    # Run the scheduler
    run_report_scheduler()