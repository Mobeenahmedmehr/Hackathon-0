import os
import tempfile
import shutil
from datetime import datetime
import pytest

from auditor.auditor_runner import generate_weekly_report
from auditor.task_analyzer import analyze_completed_tasks
from auditor.performance_metrics import calculate_performance_metrics
from auditor.report_generator import generate_business_intelligence_report

def test_sample_done_tasks():
    """Test script that creates sample Done tasks, runs auditor, and confirms report generated in Reports/"""

    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        done_dir = os.path.join(temp_dir, "Done")
        errors_dir = os.path.join(temp_dir, "Errors")
        reports_dir = os.path.join(temp_dir, "Reports")

        os.makedirs(done_dir, exist_ok=True)
        os.makedirs(errors_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)

        # Create sample Done tasks
        sample_tasks = [
            "sample_task_1.md",
            "sample_task_2.md",
            "sample_task_3.md"
        ]

        for i, task_file in enumerate(sample_tasks):
            task_path = os.path.join(done_dir, task_file)
            with open(task_path, 'w') as f:
                f.write(f"""# Task {i+1} Completion Report
Date: {datetime.now().strftime('%Y-%m-%d')}
Status: Completed
Agent: EmailAgent
Task Type: Email Processing
Tool: Gmail API
Duration: {120+i*30} seconds
Result: Success
""")

        # Create sample Error tasks
        error_tasks = [
            "error_task_1.md",
            "error_task_2.md"
        ]

        for i, error_file in enumerate(error_tasks):
            error_path = os.path.join(errors_dir, error_file)
            with open(error_path, 'w') as f:
                f.write(f"""# Task {i+1} Error Report
Date: {datetime.now().strftime('%Y-%m-%d')}
Status: Failed
Agent: LeadAgent
Task Type: Lead Generation
Tool: Browser Automation
Error: Connection Timeout
""")

        # Run the auditor
        report_path = generate_weekly_report(
            done_dir=done_dir,
            errors_dir=errors_dir,
            reports_dir=reports_dir
        )

        # Verify report was generated
        assert os.path.exists(report_path), f"Report was not generated at {report_path}"
        assert report_path.startswith(reports_dir), "Report was not saved in the Reports directory"
        assert os.path.isfile(report_path), "Report path is not a file"

        # Read the report to verify it has content
        with open(report_path, 'r') as f:
            report_content = f.read()

        assert "# AI Employee Weekly Report" in report_content, "Report doesn't contain expected header"
        assert "Summary" in report_content, "Report doesn't contain summary section"
        assert "Task Breakdown" in report_content, "Report doesn't contain task breakdown section"
        assert "Agent Activity" in report_content, "Report doesn't contain agent activity section"
        assert "Tool Usage" in report_content, "Report doesn't contain tool usage section"

        # Verify the statistics reflect our test data
        assert "Total tasks processed: 5" in report_content, "Incorrect total task count"
        assert "Successful tasks: 3" in report_content, "Incorrect successful task count"
        assert "Failed tasks: 2" in report_content, "Incorrect failed task count"

        print(f"✓ Report generated successfully: {report_path}")
        print(f"✓ Report contains {len(report_content)} characters")
        print("✓ All tests passed!")

def test_task_analyzer():
    """Test the task analyzer functionality"""

    with tempfile.TemporaryDirectory() as temp_dir:
        done_dir = os.path.join(temp_dir, "Done")
        errors_dir = os.path.join(temp_dir, "Errors")

        os.makedirs(done_dir, exist_ok=True)
        os.makedirs(errors_dir, exist_ok=True)

        # Create a sample task
        task_path = os.path.join(done_dir, "test_task.md")
        with open(task_path, 'w') as f:
            f.write("""# Test Task
Agent: TestAgent
Task Type: Email
Tool: Gmail API
Result: Success
""")

        # Analyze tasks
        stats = analyze_completed_tasks(done_dir, errors_dir)

        assert stats["total_tasks"] == 1, "Total tasks should be 1"
        assert stats["successful_tasks"] == 1, "Successful tasks should be 1"
        assert stats["failed_tasks"] == 0, "Failed tasks should be 0"
        assert "Email" in stats["task_types"], "Should detect Email task type"
        assert "TestAgent" in stats["agents_used"], "Should detect TestAgent"
        assert "Gmail API" in stats["tools_used"], "Should detect Gmail API tool"

        print("✓ Task analyzer tests passed!")

def test_performance_metrics():
    """Test the performance metrics functionality"""

    with tempfile.TemporaryDirectory() as temp_dir:
        done_dir = os.path.join(temp_dir, "Done")
        errors_dir = os.path.join(temp_dir, "Errors")

        os.makedirs(done_dir, exist_ok=True)
        os.makedirs(errors_dir, exist_ok=True)

        # Create a sample task
        task_path = os.path.join(done_dir, "perf_task.md")
        with open(task_path, 'w') as f:
            f.write("""# Performance Test Task
Agent: PerfAgent
Task Type: Processing
Tool: API
Duration: 150 seconds
Result: Success
""")

        # Calculate metrics
        metrics = calculate_performance_metrics(done_dir, errors_dir)

        assert "agent_success_rate" in metrics, "Should contain agent success rate"
        assert "error_frequency" in metrics, "Should contain error frequency"

        print("✓ Performance metrics tests passed!")

def test_report_generator():
    """Test the report generator functionality"""

    with tempfile.TemporaryDirectory() as temp_dir:
        reports_dir = os.path.join(temp_dir, "Reports")
        os.makedirs(reports_dir, exist_ok=True)

        # Sample statistics
        stats = {
            "total_tasks": 10,
            "successful_tasks": 8,
            "failed_tasks": 2,
            "task_types": {"Email": 5, "Lead": 3, "General": 2},
            "agents_used": {"EmailAgent": 5, "LeadAgent": 3, "GeneralAgent": 2},
            "tools_used": {"Gmail API": 5, "Browser": 3, "API": 2}
        }

        # Generate report
        report_path = os.path.join(reports_dir, "test_report.md")
        report_content = generate_business_intelligence_report(stats, report_path)

        # Verify report was created
        assert os.path.exists(report_path), "Report file should exist"

        # Verify content
        with open(report_path, 'r') as f:
            content = f.read()

        assert "AI Employee Weekly Report" in content, "Report should have correct title"
        assert "Total tasks processed: 10" in content, "Report should have correct task count"
        assert "Successful tasks: 8" in content, "Report should have correct success count"

        print("✓ Report generator tests passed!")

if __name__ == "__main__":
    print("Running auditor tests...")

    test_task_analyzer()
    test_performance_metrics()
    test_report_generator()
    test_sample_done_tasks()

    print("\n🎉 All tests passed successfully!")