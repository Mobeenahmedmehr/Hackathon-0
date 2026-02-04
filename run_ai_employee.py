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
        print("Watcher stopped by user")
    except Exception as e:
        print(f"Error in watcher: {e}")

def run_processor():
    """Run the task processor"""
    try:
        subprocess.run([sys.executable, "Watchers/task_processor.py"])
    except KeyboardInterrupt:
        print("Processor stopped by user")
    except Exception as e:
        print(f"Error in processor: {e}")

def main():
    """Main entry point for the AI Employee system"""
    print("Starting AI Employee Bronze Tier System...")
    print("=========================================")

    # Initialize required directories
    dirs_to_create = ['Inbox', 'Needs_Action', 'Done', 'Plans', 'Logs', 'Skills', 'Watchers', 'Docs']
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)

    print("✓ Directories initialized")
    print("✓ Starting file system watcher...")
    print("✓ Starting task processor...")
    print("\nSystem is now running. Press Ctrl+C to stop.\n")

    # Create threads for both components
    watcher_thread = threading.Thread(target=run_watcher, daemon=True)
    processor_thread = threading.Thread(target=run_processor, daemon=True)

    # Start both threads
    watcher_thread.start()
    processor_thread.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down AI Employee system...")
        print("All processes will terminate shortly.")
        sys.exit(0)

if __name__ == "__main__":
    main()