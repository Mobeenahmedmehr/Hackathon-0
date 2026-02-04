import subprocess
import sys
import threading
import time
from pathlib import Path


def run_watcher():
    """Run the file system watcher"""
    try:
        subprocess.run([sys.executable, "Watchers/file_watcher.py"])
    except KeyboardInterrupt:
        print("File watcher stopped by user")
    except Exception as e:
        print(f"Error in file watcher: {e}")


def run_gmail_watcher():
    """Run the gmail watcher"""
    try:
        subprocess.run([sys.executable, "Watchers/gmail_watcher.py"])
    except KeyboardInterrupt:
        print("Gmail watcher stopped by user")
    except Exception as e:
        print(f"Error in gmail watcher: {e}")


def run_processor():
    """Run the task processor"""
    try:
        subprocess.run([sys.executable, "Watchers/task_processor.py"])
    except KeyboardInterrupt:
        print("Processor stopped by user")
    except Exception as e:
        print(f"Error in processor: {e}")


def run_approval_monitor():
    """Run the approval monitor"""
    try:
        subprocess.run([sys.executable, "approval_monitor.py"])
    except KeyboardInterrupt:
        print("Approval monitor stopped by user")
    except Exception as e:
        print(f"Error in approval monitor: {e}")


def run_scheduler():
    """Run the scheduler"""
    try:
        subprocess.run([sys.executable, "schedule.py"])
    except KeyboardInterrupt:
        print("Scheduler stopped by user")
    except Exception as e:
        print(f"Error in scheduler: {e}")


def main():
    """Main entry point for the AI Employee Silver Tier system"""
    print("Starting AI Employee Silver Tier System...")
    print("===========================================")

    # Initialize required directories
    dirs_to_create = [
        'Inbox', 'Needs_Action', 'Done', 'Plans', 'Logs', 'Skills', 'Watchers',
        'Docs', 'Pending_Approval', 'Approved', 'Rejected', 'Drafts'
    ]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)

    print("✓ Directories initialized")
    print("✓ Starting file system watcher...")
    print("✓ Starting gmail watcher...")
    print("✓ Starting task processor...")
    print("✓ Starting approval monitor...")
    print("✓ Starting scheduler...")
    print("\nSilver Tier system is now running. Press Ctrl+C to stop.\n")

    # Create threads for all components
    watcher_thread = threading.Thread(target=run_watcher, daemon=True)
    gmail_watcher_thread = threading.Thread(target=run_gmail_watcher, daemon=True)
    processor_thread = threading.Thread(target=run_processor, daemon=True)
    approval_monitor_thread = threading.Thread(target=run_approval_monitor, daemon=True)
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)

    # Start all threads
    watcher_thread.start()
    gmail_watcher_thread.start()
    processor_thread.start()
    approval_monitor_thread.start()
    scheduler_thread.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down AI Employee Silver Tier system...")
        print("All processes will terminate shortly.")
        sys.exit(0)


if __name__ == "__main__":
    main()