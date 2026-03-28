import os
from pathlib import Path

def show_recent_logs():
    """Read from Logs/ directory and display last 50 log entries."""
    logs_dir = Path("Logs")
    if not logs_dir.exists():
        print("Logs directory not found.")
        return

    # Get all log files in the directory
    log_files = list(logs_dir.glob("*.log"))
    if not log_files:
        print("No log files found in Logs/ directory.")
        return

    print(f"\nRecent Logs (last 50 entries from each file):")
    print("=" * 60)

    for log_file in log_files:
        print(f"\n--- {log_file.name} ---")

        try:
            # Read all lines from the log file
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Show last 50 lines or all lines if fewer than 50
            recent_lines = lines[-50:] if len(lines) > 50 else lines

            for line in recent_lines:
                print(line.rstrip())  # rstrip() removes trailing newline

        except Exception as e:
            print(f"Error reading {log_file.name}: {e}")

def view_log_file(filename):
    """View a specific log file."""
    log_path = Path("Logs") / filename

    if not log_path.exists():
        print(f"Log file {filename} not found in Logs/ directory.")
        return

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Show last 50 lines or all lines if fewer than 50
        recent_lines = lines[-50:] if len(lines) > 50 else lines

        print(f"\n--- Contents of {filename} (last 50 lines) ---")
        for line in recent_lines:
            print(line.rstrip())

    except Exception as e:
        print(f"Error reading {filename}: {e}")

def list_log_files():
    """List all log files in the Logs directory."""
    logs_dir = Path("Logs")
    if not logs_dir.exists():
        print("Logs directory not found.")
        return []

    log_files = list(logs_dir.glob("*.log"))
    if not log_files:
        print("No log files found in Logs/ directory.")
        return []

    print(f"\nLog Files in Logs/ directory:")
    print("-" * 30)
    for i, log_file in enumerate(log_files, 1):
        print(f"{i}. {log_file.name}")

    return log_files

def log_viewer_menu():
    """Menu for log viewing functionality."""
    while True:
        print("\nLog Viewer")
        print("=" * 30)
        print("1. Show recent logs from all files")
        print("2. List log files")
        print("3. View specific log file")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            show_recent_logs()
        elif choice == "2":
            list_log_files()
        elif choice == "3":
            log_files = list_log_files()
            if log_files:
                try:
                    file_num = int(input(f"Enter file number (1-{len(log_files)}): "))
                    if 1 <= file_num <= len(log_files):
                        view_log_file(log_files[file_num - 1].name)
                    else:
                        print("Invalid file number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "4":
            print("Exiting log viewer...")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    log_viewer_menu()