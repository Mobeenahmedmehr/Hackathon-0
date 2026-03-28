import os
import shutil
from datetime import datetime
from pathlib import Path

def list_pending_plans():
    """Display all files inside Pending_Approval/"""
    pending_dir = Path("Pending_Approval")
    if not pending_dir.exists():
        print("No Pending_Approval directory found.")
        return []

    plan_files = list(pending_dir.glob("*.md"))
    if not plan_files:
        print("No pending plans found.")
        return []

    print(f"\nPending Plans ({len(plan_files)}):")
    print("-" * 40)
    for i, plan_file in enumerate(plan_files, 1):
        print(f"{i}. {plan_file.name}")
    print()
    return plan_files

def view_plan(plan_id):
    """Open and print plan content."""
    pending_dir = Path("Pending_Approval")
    plan_files = list(pending_dir.glob("*.md"))

    if not plan_files or plan_id > len(plan_files) or plan_id <= 0:
        print("Invalid plan ID.")
        return False

    plan_file = plan_files[plan_id - 1]
    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n--- Plan: {plan_file.name} ---")
        print(content)
        print("--- End of Plan ---\n")
        return True
    except Exception as e:
        print(f"Error reading plan: {e}")
        return False

def approve_plan(plan_id):
    """Move file from Pending_Approval/ → Approved/ with approval metadata."""
    pending_dir = Path("Pending_Approval")
    approved_dir = Path("Approved")
    approved_dir.mkdir(exist_ok=True)

    plan_files = list(pending_dir.glob("*.md"))
    if not plan_files or plan_id > len(plan_files) or plan_id <= 0:
        print("Invalid plan ID.")
        return False

    plan_file = plan_files[plan_id - 1]

    # Read current content
    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading plan: {e}")
        return False

    # Add approval metadata to the top
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    approval_header = f"""Approval Status: Approved
Approved By: Human
Approval Timestamp: {timestamp}

"""

    updated_content = approval_header + content

    # Move to Approved directory with new filename to avoid conflicts
    approved_file = approved_dir / plan_file.name
    counter = 1
    while approved_file.exists():
        name_parts = plan_file.stem.split('_')
        if len(name_parts) > 1 and name_parts[-1].isdigit():
            new_name = '_'.join(name_parts[:-1]) + f"_{int(name_parts[-1])+1}{plan_file.suffix}"
        else:
            new_name = f"{plan_file.stem}_{counter}{plan_file.suffix}"
        approved_file = approved_dir / new_name
        counter += 1

    try:
        with open(approved_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Remove original file from Pending_Approval
        plan_file.unlink()

        print(f"Plan '{plan_file.name}' approved and moved to Approved/")
        return True
    except Exception as e:
        print(f"Error approving plan: {e}")
        return False

def reject_plan(plan_id, reason="Rejected by human"):
    """Move file to Errors/ with rejection reason."""
    pending_dir = Path("Pending_Approval")
    errors_dir = Path("Errors")
    errors_dir.mkdir(exist_ok=True)

    plan_files = list(pending_dir.glob("*.md"))
    if not plan_files or plan_id > len(plan_files) or plan_id <= 0:
        print("Invalid plan ID.")
        return False

    plan_file = plan_files[plan_id - 1]

    # Read current content
    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading plan: {e}")
        return False

    # Add rejection metadata to the top
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rejection_header = f"""Approval Status: Rejected
Rejected By: Human
Rejection Reason: {reason}
Rejection Timestamp: {timestamp}

"""

    updated_content = rejection_header + content

    # Move to Errors directory
    error_file = errors_dir / plan_file.name
    counter = 1
    while error_file.exists():
        name_parts = plan_file.stem.split('_')
        if len(name_parts) > 1 and name_parts[-1].isdigit():
            new_name = '_'.join(name_parts[:-1]) + f"_{int(name_parts[-1])+1}{plan_file.suffix}"
        else:
            new_name = f"{plan_file.stem}_{counter}{plan_file.suffix}"
        error_file = errors_dir / new_name
        counter += 1

    try:
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Remove original file from Pending_Approval
        plan_file.unlink()

        print(f"Plan '{plan_file.name}' rejected and moved to Errors/")
        return True
    except Exception as e:
        print(f"Error rejecting plan: {e}")
        return False

def cli_interface():
    """Command-line interface for reviewing AI plans."""
    while True:
        print("\nAI Employee Approval Dashboard")
        print("=" * 40)
        print("1. List pending plans")
        print("2. View plan")
        print("3. Approve plan")
        print("4. Reject plan")
        print("5. Exit")

        try:
            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                list_pending_plans()

            elif choice == "2":
                plan_files = list_pending_plans()
                if plan_files:
                    try:
                        plan_id = int(input("Enter plan number to view: "))
                        view_plan(plan_id)
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            elif choice == "3":
                plan_files = list_pending_plans()
                if plan_files:
                    try:
                        plan_id = int(input("Enter plan number to approve: "))
                        approve_plan(plan_id)
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            elif choice == "4":
                plan_files = list_pending_plans()
                if plan_files:
                    try:
                        plan_id = int(input("Enter plan number to reject: "))
                        reason = input("Enter rejection reason (optional): ").strip()
                        if not reason:
                            reason = "Rejected by human"
                        reject_plan(plan_id, reason)
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            elif choice == "5":
                print("Exiting dashboard...")
                break

            else:
                print("Invalid choice. Please enter a number between 1-5.")

        except KeyboardInterrupt:
            print("\n\nExiting dashboard...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_interface()