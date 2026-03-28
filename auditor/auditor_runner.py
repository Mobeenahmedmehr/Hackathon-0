import os
from datetime import datetime
from typing import Dict, Any
import logging

from auditor.task_analyzer import analyze_completed_tasks
from auditor.performance_metrics import calculate_performance_metrics
from auditor.report_generator import generate_business_intelligence_report

logger = logging.getLogger(__name__)

def generate_weekly_report(done_dir: str = "Done/", errors_dir: str = "Errors/", reports_dir: str = "Reports/") -> str:
    """
    Run the full auditing pipeline.

    Workflow:
    1. Analyze tasks
    2. Compute metrics
    3. Generate report
    4. Save report

    Args:
        done_dir: Directory containing successful task files
        errors_dir: Directory containing failed task files
        reports_dir: Directory to store generated reports

    Returns:
        Path to the generated report
    """
    logger.info("Starting weekly report generation...")

    # Ensure reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    # Step 1: Analyze tasks
    logger.info("Analyzing completed tasks...")
    task_stats = analyze_completed_tasks(done_dir, errors_dir)

    # Step 2: Compute metrics
    logger.info("Calculating performance metrics...")
    performance_metrics = calculate_performance_metrics(done_dir, errors_dir)

    # Combine stats and metrics for the report
    combined_data = {
        **task_stats,
        **performance_metrics
    }

    # Step 3: Generate report
    logger.info("Generating business intelligence report...")
    report_path = os.path.join(reports_dir, f"weekly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    report_content = generate_business_intelligence_report(combined_data, report_path)

    logger.info(f"Weekly report generated successfully: {report_path}")
    return report_path

if __name__ == "__main__":
    # Run the auditor if called directly
    report_path = generate_weekly_report()
    print(f"Weekly report generated at: {report_path}")