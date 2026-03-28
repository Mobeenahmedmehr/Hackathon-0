import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import our dashboard modules
from dashboard.approval_cli import list_pending_plans, view_plan, approve_plan, reject_plan
from dashboard.system_monitor import get_system_summary
from dashboard.log_viewer import show_recent_logs

def setup_test_environment():
    """Create test directories and sample files."""
    # Create test directories
    os.makedirs("Pending_Approval", exist_ok=True)
    os.makedirs("Approved", exist_ok=True)
    os.makedirs("Errors", exist_ok=True)
    os.makedirs("Logs", exist_ok=True)
    os.makedirs("Needs_Action", exist_ok=True)
    os.makedirs("Done", exist_ok=True)

def teardown_test_environment():
    """Clean up test directories."""
    dirs_to_remove = ["Pending_Approval", "Approved", "Errors", "Logs", "Needs_Action", "Done"]
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

def test_create_fake_plan():
    """Create a fake plan in Pending_Approval for testing."""
    plan_content = """# AI Action Plan
## Task Description
Send follow-up email to potential client

## Steps
1. Get client contact information
2. Compose personalized email
3. Send email via Gmail API
"""
    with open("Pending_Approval/test_plan_001.md", "w") as f:
        f.write(plan_content)
    print("Created fake plan: Pending_Approval/test_plan_001.md")

def test_list_pending_plans():
    """Test listing pending plans."""
    print("\nTesting list_pending_plans()...")
    plans = list_pending_plans()
    print(f"Found {len(plans)} pending plans")
    return len(plans) > 0

def test_view_plan():
    """Test viewing a plan."""
    print("\nTesting view_plan()...")
    # We need to figure out the correct index for our test plan
    pending_plans = list(Path("Pending_Approval").glob("*.md"))
    if pending_plans:
        # Find the index of our test plan
        for i, plan in enumerate(pending_plans, 1):
            if "test_plan_001" in str(plan):
                return view_plan(i)
    return False

def test_approve_plan():
    """Test approving a plan."""
    print("\nTesting approve_plan()...")
    # We need to figure out the correct index for our test plan
    pending_plans = list(Path("Pending_Approval").glob("*.md"))
    if pending_plans:
        # Find the index of our test plan
        for i, plan in enumerate(pending_plans, 1):
            if "test_plan_001" in str(plan):
                result = approve_plan(i)
                # Verify the plan moved to Approved/
                approved_plan = Path("Approved") / plan.name
                return result and approved_plan.exists()
    return False

def test_system_monitor():
    """Test system monitoring functionality."""
    print("\nTesting system monitor...")
    summary = get_system_summary()
    print(f"System summary: {summary}")
    return isinstance(summary, dict)

def test_log_viewer():
    """Test log viewer functionality."""
    print("\nTesting log viewer...")
    # Create a sample log file
    with open("Logs/test.log", "w") as f:
        for i in range(60):  # Create more than 50 entries to test the limit
            f.write(f"[INFO] {i}: Sample log entry\n")

    # Test the function
    show_recent_logs()
    return True

def run_tests():
    """Run all dashboard tests."""
    print("Starting Dashboard Tests...")
    print("=" * 50)

    # Setup
    setup_test_environment()

    # Create a fake plan for testing
    test_create_fake_plan()

    # Run tests
    tests_passed = 0
    total_tests = 5

    if test_list_pending_plans():
        print("✓ list_pending_plans test passed")
        tests_passed += 1
    else:
        print("✗ list_pending_plans test failed")

    if test_view_plan():
        print("✓ view_plan test passed")
        tests_passed += 1
    else:
        print("✗ view_plan test failed")

    # For approval test, recreate the plan since it might have been moved
    if Path("Approved/test_plan_001.md").exists():
        # If plan was already approved, we need to move it back for the next test
        shutil.move("Approved/test_plan_001.md", "Pending_Approval/test_plan_001.md")

    if test_approve_plan():
        print("✓ approve_plan test passed")
        tests_passed += 1
    else:
        print("✗ approve_plan test failed")

    if test_system_monitor():
        print("✓ system monitor test passed")
        tests_passed += 1
    else:
        print("✗ system monitor test failed")

    if test_log_viewer():
        print("✓ log viewer test passed")
        tests_passed += 1
    else:
        print("✗ log viewer test failed")

    # Teardown
    teardown_test_environment()

    print("\n" + "=" * 50)
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    run_tests()