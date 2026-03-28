import unittest
import tempfile
import os
from pathlib import Path
import shutil

from core.orchestrator import Orchestrator, orchestrator_cycle


class TestOrchestrator(unittest.TestCase):
    """
    Test script that:
    - creates a fake task in Needs_Action
    - runs orchestrator_cycle()
    - verifies plan generation
    - prints result
    """

    def setUp(self):
        """
        Set up test environment with temporary directories
        """
        self.test_dir = tempfile.mkdtemp()

        # Create temporary directory structure
        self.needs_action_dir = os.path.join(self.test_dir, "Needs_Action")
        self.plans_dir = os.path.join(self.test_dir, "Plans")
        self.pending_approval_dir = os.path.join(self.test_dir, "Pending_Approval")
        self.approved_dir = os.path.join(self.test_dir, "Approved")
        self.drafts_dir = os.path.join(self.test_dir, "Drafts")
        self.done_dir = os.path.join(self.test_dir, "Done")
        self.errors_dir = os.path.join(self.test_dir, "Errors")

        os.makedirs(self.needs_action_dir, exist_ok=True)
        os.makedirs(self.plans_dir, exist_ok=True)
        os.makedirs(self.pending_approval_dir, exist_ok=True)
        os.makedirs(self.approved_dir, exist_ok=True)
        os.makedirs(self.drafts_dir, exist_ok=True)
        os.makedirs(self.done_dir, exist_ok=True)
        os.makedirs(self.errors_dir, exist_ok=True)

        # Temporarily change working directory
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Import paths after changing directory
        from utils.paths import (
            get_needs_action_path, get_plans_path, get_pending_approval_path,
            get_approved_path, get_drafts_path, get_done_path, get_errors_path
        )

        # Patch the functions to return our test paths
        import utils.paths
        utils.paths.get_needs_action_path = lambda: self.needs_action_dir
        utils.paths.get_plans_path = lambda: self.plans_dir
        utils.paths.get_pending_approval_path = lambda: self.pending_approval_dir
        utils.paths.get_approved_path = lambda: self.approved_dir
        utils.paths.get_drafts_path = lambda: self.drafts_dir
        utils.paths.get_done_path = lambda: self.done_dir
        utils.paths.get_errors_path = lambda: self.errors_dir

    def tearDown(self):
        """
        Clean up test environment
        """
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_scan_new_tasks(self):
        """
        Test scanning for new tasks and generating plans
        """
        # Create a fake task file
        task_content = """# Task
Source: Gmail
Sender: test@example.com
Timestamp: 2026-03-15 10:30:00

Subject: Test Subject

Message:
Please prepare a report on quarterly sales figures.
"""

        task_file_path = os.path.join(self.needs_action_dir, "test_task_001.md")
        with open(task_file_path, 'w') as f:
            f.write(task_content)

        # Create orchestrator and scan for tasks
        orchestrator = Orchestrator()
        generated_plans = orchestrator.scan_new_tasks()

        # Verify that a plan was generated
        self.assertEqual(len(generated_plans), 1)
        self.assertTrue(os.path.exists(generated_plans[0]))

        # Verify the task was moved to Plans directory
        plan_files = list(Path(self.plans_dir).glob("*.md"))
        self.assertEqual(len([f for f in plan_files if 'plan_' in f.name]), 1)
        self.assertEqual(len([f for f in plan_files if 'task_' in f.name]), 1)

    def test_send_for_approval(self):
        """
        Test sending a plan for approval
        """
        # Create a plan file
        plan_content = """# Plan for: Test Task

## Goal
Process the test task

## Steps
1. Step 1
2. Step 2
"""

        plan_file_path = os.path.join(self.plans_dir, "test_plan_001.md")
        with open(plan_file_path, 'w') as f:
            f.write(plan_content)

        # Create orchestrator and send for approval
        orchestrator = Orchestrator()
        approval_path = orchestrator.send_for_approval(plan_file_path)

        # Verify the plan was moved to Pending_Approval with metadata
        pending_files = list(Path(self.pending_approval_dir).glob("*.md"))
        self.assertEqual(len(pending_files), 1)

        with open(pending_files[0], 'r') as f:
            content = f.read()
            self.assertIn("Approval Status: Pending", content)
            self.assertIn("Requested By: AI Employee", content)

    def test_check_approved_plans(self):
        """
        Test checking for approved plans
        """
        # Create an approved plan file
        plan_content = """---
Approval Status: Approved
Created Time: 2026-03-15 10:30:00
Requested By: AI Employee
---

# Plan for: Test Task

## Goal
Process the test task

## Steps
1. Step 1
2. Step 2
"""

        plan_file_path = os.path.join(self.approved_dir, "approved_plan_001.md")
        with open(plan_file_path, 'w') as f:
            f.write(plan_content)

        # Create orchestrator and check for approved plans
        orchestrator = Orchestrator()
        approved_plans = orchestrator.check_approved_plans()

        # Verify the approved plan is found
        self.assertEqual(len(approved_plans), 1)
        self.assertIn("approved_plan_001.md", approved_plans[0])

    def test_execute_plan(self):
        """
        Test executing a plan
        """
        # Create an approved plan file
        plan_content = """---
Approval Status: Approved
Created Time: 2026-03-15 10:30:00
Requested By: AI Employee
---

# Plan for: Test Task

## Goal
Process the test task

## Task Type
General

## Recommended Agent
Default Agent

## Tools Required
- File System Access

## Steps
1. Read the task content
2. Process the information
3. Generate output

## Approval Required
Yes
"""

        plan_file_path = os.path.join(self.approved_dir, "exec_plan_001.md")
        with open(plan_file_path, 'w') as f:
            f.write(plan_content)

        # Create orchestrator and execute the plan
        orchestrator = Orchestrator()
        result = orchestrator.execute_plan(plan_file_path)

        # Verify execution was successful
        self.assertTrue(result)

        # Check that output was created in Done directory
        done_files = list(Path(self.done_dir).glob("*.md"))
        executed_files = [f for f in done_files if 'executed_' in f.name]
        self.assertEqual(len(executed_files), 1)

    def test_orchestrator_cycle(self):
        """
        Test the complete orchestrator cycle
        """
        # Create a fake task file
        task_content = """# Task
Source: Gmail
Sender: test@example.com
Timestamp: 2026-03-15 10:30:00

Subject: Test Subject

Message:
Please prepare a report on quarterly sales figures.
"""

        task_file_path = os.path.join(self.needs_action_dir, "cycle_task_001.md")
        with open(task_file_path, 'w') as f:
            f.write(task_content)

        # Run the orchestrator cycle
        orchestrator = Orchestrator()
        cycle_results = orchestrator.orchestrator_cycle()

        # Verify results
        self.assertEqual(cycle_results['new_plans_generated'], 1)
        self.assertEqual(cycle_results['approved_plans_executed'], 0)  # No approved plans yet

        # Now create an approved plan and run cycle again
        plan_files = list(Path(self.pending_approval_dir).glob("*.md"))
        for plan_file in plan_files:
            # Update the plan to show it's approved
            with open(plan_file, 'r') as f:
                content = f.read()

            # Replace "Pending" with "Approved" in the status
            content = content.replace("Approval Status: Pending", "Approval Status: Approved")

            approved_plan_path = os.path.join(self.approved_dir, os.path.basename(plan_file))
            with open(approved_plan_path, 'w') as f:
                f.write(content)

        # Run cycle again to execute the approved plan
        cycle_results = orchestrator.orchestrator_cycle()

        # Now verify that the plan was executed
        self.assertEqual(cycle_results['approved_plans_executed'], 1)

    def test_full_integration(self):
        """
        Full integration test of the orchestrator
        """
        print("\n=== Running Full Integration Test ===")

        # Create a task
        task_content = """# Task
Source: Gmail
Sender: manager@company.com
Timestamp: 2026-03-15 10:30:00

Subject: Quarterly Report Request

Message:
Hi, please prepare a comprehensive report on quarterly sales figures. Include charts and recommendations for next quarter.
"""

        task_file_path = os.path.join(self.needs_action_dir, "integration_task.md")
        with open(task_file_path, 'w') as f:
            f.write(task_content)

        print(f"1. Created test task: {os.path.basename(task_file_path)}")
        print(f"   Tasks in Needs_Action: {len(list(Path(self.needs_action_dir).glob('*.md')))}")

        # Run orchestrator cycle
        cycle_results = orchestrator_cycle()

        print(f"2. Orchestrator cycle completed")
        print(f"   New plans generated: {cycle_results['new_plans_generated']}")
        print(f"   Approved plans executed: {cycle_results['approved_plans_executed']}")

        # Check results
        plans_count = len(list(Path(self.plans_dir).glob("*.md")))
        pending_count = len(list(Path(self.pending_approval_dir).glob("*.md")))

        print(f"3. Results:")
        print(f"   Plans created: {plans_count}")
        print(f"   Plans sent for approval: {pending_count}")

        # Verify we have one plan in pending approval
        self.assertGreaterEqual(pending_count, 1, "Should have at least one plan in pending approval")

        print("=== Integration Test Completed Successfully ===\n")


if __name__ == '__main__':
    unittest.main()