import os
from approval_cli import cli_interface
from system_monitor import monitor_system_health
from log_viewer import log_viewer_menu

def main_menu():
    """Main dashboard menu for the human control dashboard."""
    while True:
        print("\n" + "="*50)
        print("AI EMPLOYEE HUMAN CONTROL DASHBOARD")
        print("="*50)
        print("1. Approval Dashboard")
        print("2. System Monitor")
        print("3. View Logs")
        print("4. Exit")
        print("="*50)

        try:
            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                print("\nLaunching Approval Dashboard...")
                cli_interface()
            elif choice == "2":
                print("\nLaunching System Monitor...")
                monitor_system_health()
            elif choice == "3":
                print("\nLaunching Log Viewer...")
                log_viewer_menu()
            elif choice == "4":
                print("\nThank you for using the AI Employee Dashboard. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1-4.")

        except KeyboardInterrupt:
            print("\n\nExiting dashboard...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_menu()