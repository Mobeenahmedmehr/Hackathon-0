import os
from datetime import datetime
from typing import Dict, Any

def generate_business_intelligence_report(stats: Dict[str, Any], output_path: str = None) -> str:
    """
    Generate business intelligence reports.

    Args:
        stats: Statistics dictionary from task_analyzer
        output_path: Path to save the report (optional)

    Returns:
        Markdown report content as string
    """
    # Create report filename if not provided
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"Reports/weekly_report_{timestamp}.md"

    # Ensure Reports directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Format the report
    report_content = format_report(stats)

    # Write the report to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return report_content

def format_report(stats: Dict[str, Any]) -> str:
    """
    Format the statistics into a readable markdown report.

    Args:
        stats: Statistics dictionary from task_analyzer

    Returns:
        Formatted markdown report
    """
    # Calculate success rate
    success_rate = 0
    if stats.get("total_tasks", 0) > 0:
        success_rate = (stats.get("successful_tasks", 0) / stats["total_tasks"]) * 100

    # Format the report
    report = f"""# AI Employee Weekly Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total tasks processed: {stats.get('total_tasks', 0)}
- Successful tasks: {stats.get('successful_tasks', 0)}
- Failed tasks: {stats.get('failed_tasks', 0)}
- Success rate: {success_rate:.2f}%

## Task Breakdown
"""

    # Task types breakdown
    if stats.get('task_types'):
        report += "### Tasks by Type\n"
        for task_type, count in stats['task_types'].items():
            report += f"- {task_type}: {count}\n"
        report += "\n"

    # Agent activity
    if stats.get('agents_used'):
        report += "## Agent Activity\n"
        report += "### Which agents were used most\n"
        for agent, count in sorted(stats['agents_used'].items(), key=lambda x: x[1], reverse=True):
            report += f"- {agent}: {count}\n"
        report += "\n"

    # Tool usage
    if stats.get('tools_used'):
        report += "## Tool Usage\n"
        report += "### Which tools were executed\n"
        for tool, count in sorted(stats['tools_used'].items(), key=lambda x: x[1], reverse=True):
            report += f"- {tool}: {count}\n"
        report += "\n"

    # Productivity insights
    report += "## Productivity Insights\n"
    total_tasks = stats.get('total_tasks', 0)
    successful_tasks = stats.get('successful_tasks', 0)
    failed_tasks = stats.get('failed_tasks', 0)

    if total_tasks > 0:
        report += f"- Overall system processed {total_tasks} tasks this week\n"
        if successful_tasks > 0:
            report += f"- {successful_tasks} tasks completed successfully ({(successful_tasks/total_tasks)*100:.1f}% success rate)\n"
        if failed_tasks > 0:
            report += f"- {failed_tasks} tasks failed to complete\n"

    # Identify most common task type
    if stats.get('task_types'):
        most_common_task = max(stats['task_types'], key=stats['task_types'].get)
        report += f"- Most common task type: {most_common_task} ({stats['task_types'][most_common_task]} instances)\n"

    # Identify most active agent
    if stats.get('agents_used'):
        most_active_agent = max(stats['agents_used'], key=stats['agents_used'].get)
        report += f"- Most active agent: {most_active_agent} ({stats['agents_used'][most_active_agent]} tasks)\n"

    # Identify most used tool
    if stats.get('tools_used'):
        most_used_tool = max(stats['tools_used'], key=stats['tools_used'].get)
        report += f"- Most frequently used tool: {most_used_tool} ({stats['tools_used'][most_used_tool]} executions)\n"

    # Additional insights based on patterns
    if successful_tasks == 0 and total_tasks > 0:
        report += "- ⚠️  Warning: No tasks completed successfully this week. System requires attention.\n"
    elif success_rate < 50:
        report += "- ⚠️  Low success rate. Consider reviewing error logs for issues.\n"
    else:
        report += "- System performing well with high success rate.\n"

    report += f"\n*Report generated automatically by AI Employee Audit System*"

    return report