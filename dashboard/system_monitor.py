import os
from pathlib import Path

def count_tasks_in_directory(directory_name):
    """Count the number of files in a directory."""
    dir_path = Path(directory_name)
    if not dir_path.exists():
        return 0

    # Count all files in the directory (not just .md files)
    return len(list(dir_path.iterdir()))

def display_system_status():
    """Display system health information."""
    print("\nAI Employee System Status")
    print("=" * 50)

    # Count tasks in Needs_Action
    needs_action_count = count_tasks_in_directory("Needs_Action")
    print(f"Tasks in Needs_Action/: {needs_action_count}")

    # Count plans in Pending_Approval
    pending_approval_count = count_tasks_in_directory("Pending_Approval")
    print(f"Plans in Pending_Approval/: {pending_approval_count}")

    # Count approved plans
    approved_count = count_tasks_in_directory("Approved")
    print(f"Approved plans: {approved_count}")

    # Count completed tasks
    completed_count = count_tasks_in_directory("Done")
    print(f"Completed tasks: {completed_count}")

    # Count errors
    errors_count = count_tasks_in_directory("Errors")
    print(f"Error logs: {errors_count}")

    print("=" * 50)

def get_system_summary():
    """Get a dictionary with system status information."""
    summary = {
        "needs_action": count_tasks_in_directory("Needs_Action"),
        "pending_approval": count_tasks_in_directory("Pending_Approval"),
        "approved": count_tasks_in_directory("Approved"),
        "completed": count_tasks_in_directory("Done"),
        "errors": count_tasks_in_directory("Errors")
    }
    return summary

def print_status_summary():
    """Print a concise status summary."""
    summary = get_system_summary()

    print("\nSystem Summary:")
    print(f"  • {summary['needs_action']} tasks need processing")
    print(f"  • {summary['pending_approval']} plans pending approval")
    print(f"  • {summary['approved']} plans approved")
    print(f"  • {summary['completed']} tasks completed")
    print(f"  • {summary['errors']} errors recorded")

def monitor_system_health():
    """Monitor and display system health information."""
    display_system_status()
    print_status_summary()

if __name__ == "__main__":
    monitor_system_health()