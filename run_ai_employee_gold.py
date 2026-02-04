"""
Gold Tier AI Employee System Runner
Orchestrates all Gold Tier components with enhanced autonomy and audit capabilities.
"""

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


def run_gold_processor():
    """Run the Gold Tier task processor"""
    try:
        subprocess.run([sys.executable, "Gold_Task_Processor.py"])
    except KeyboardInterrupt:
        print("Gold processor stopped by user")
    except Exception as e:
        print(f"Error in Gold processor: {e}")


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


def run_email_mcp_server():
    """Run the email MCP server"""
    try:
        subprocess.run([sys.executable, "mcp_server.py"])
    except KeyboardInterrupt:
        print("Email MCP server stopped by user")
    except Exception as e:
        print(f"Error in email MCP server: {e}")


def run_browser_mcp_server():
    """Run the browser MCP server"""
    try:
        subprocess.run([sys.executable, "Browser_MCPServer.py"])
    except KeyboardInterrupt:
        print("Browser MCP server stopped by user")
    except Exception as e:
        print(f"Error in browser MCP server: {e}")


def run_gold_auditor():
    """Run the Gold Tier auditor (periodic execution)"""
    try:
        # The auditor runs once per week to generate reports
        import subprocess
        import sys

        # Run the auditor script as a subprocess
        while True:
            subprocess.run([sys.executable, "Gold_Auditor.py"])

            # Wait 7 days before running again
            time.sleep(7 * 24 * 3600)  # Wait 7 days
    except KeyboardInterrupt:
        print("Gold auditor stopped by user")
    except Exception as e:
        print(f"Error in Gold auditor: {e}")


def main():
    """Main entry point for the AI Employee Gold Tier system"""
    print("Starting AI Employee Gold Tier System...")
    print("=========================================")

    # Initialize required directories
    dirs_to_create = [
        'Inbox', 'Needs_Action', 'Done', 'Plans', 'Logs', 'Skills', 'Watchers',
        'Docs', 'Pending_Approval', 'Approved', 'Rejected', 'Drafts',
        'In_Progress', 'Quarantined', 'Reports'
    ]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)

    print("✓ Directories initialized")
    print("✓ Starting file system watcher...")
    print("✓ Starting gmail watcher...")
    print("✓ Starting Gold Tier task processor...")
    print("✓ Starting approval monitor...")
    print("✓ Starting scheduler...")
    print("✓ Starting email MCP server...")
    print("✓ Starting browser MCP server...")
    print("✓ Starting Gold Tier auditor...")
    print("\nGold Tier system is now running. Press Ctrl+C to stop.\n")

    # Create threads for all components
    watcher_thread = threading.Thread(target=run_watcher, daemon=True)
    gmail_watcher_thread = threading.Thread(target=run_gmail_watcher, daemon=True)
    gold_processor_thread = threading.Thread(target=run_gold_processor, daemon=True)
    approval_monitor_thread = threading.Thread(target=run_approval_monitor, daemon=True)
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    email_mcp_thread = threading.Thread(target=run_email_mcp_server, daemon=True)
    browser_mcp_thread = threading.Thread(target=run_browser_mcp_server, daemon=True)
    gold_auditor_thread = threading.Thread(target=run_gold_auditor, daemon=True)

    # Start all threads
    watcher_thread.start()
    gmail_watcher_thread.start()
    gold_processor_thread.start()
    approval_monitor_thread.start()
    scheduler_thread.start()
    email_mcp_thread.start()
    browser_mcp_thread.start()
    gold_auditor_thread.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down AI Employee Gold Tier system...")
        print("All processes will terminate shortly.")
        sys.exit(0)


if __name__ == "__main__":
    main()