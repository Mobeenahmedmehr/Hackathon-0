import os
import re
from datetime import datetime
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

def calculate_performance_metrics(done_dir: str = "Done/", errors_dir: str = "Errors/") -> Dict[str, Any]:
    """
    Track system performance metrics.

    Args:
        done_dir: Directory containing successful task files
        errors_dir: Directory containing failed task files

    Returns:
        Dictionary containing performance metrics
    """
    metrics = {
        "average_task_completion_time": 0,
        "agent_success_rate": {},
        "error_frequency": 0,
        "total_completion_time": 0,
        "total_tasks_analyzed": 0
    }

    completion_times = []
    successful_agents = {}
    total_agents = {}

    # Process successful tasks to calculate completion times
    if os.path.exists(done_dir):
        for filename in os.listdir(done_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(done_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract completion time from the content
                    completion_time = extract_completion_time(content, filepath)
                    if completion_time > 0:
                        completion_times.append(completion_time)

                    # Extract agent and update counters
                    agent = extract_agent_used(content)
                    if agent:
                        total_agents[agent] = total_agents.get(agent, 0) + 1
                        successful_agents[agent] = successful_agents.get(agent, 0) + 1

                    metrics["total_tasks_analyzed"] += 1

                except Exception as e:
                    logger.error(f"Error analyzing successful task {filepath}: {str(e)}")

    # Process failed tasks to update agent counters
    if os.path.exists(errors_dir):
        for filename in os.listdir(errors_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(errors_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract agent and update total counter only (not successful)
                    agent = extract_agent_used(content)
                    if agent:
                        total_agents[agent] = total_agents.get(agent, 0) + 1

                    metrics["total_tasks_analyzed"] += 1

                except Exception as e:
                    logger.error(f"Error analyzing failed task {filepath}: {str(e)}")

    # Calculate average completion time
    if completion_times:
        metrics["total_completion_time"] = sum(completion_times)
        metrics["average_task_completion_time"] = sum(completion_times) / len(completion_times)
    else:
        metrics["average_task_completion_time"] = 0

    # Calculate agent success rates
    for agent, total_count in total_agents.items():
        successful_count = successful_agents.get(agent, 0)
        metrics["agent_success_rate"][agent] = (successful_count / total_count) * 100 if total_count > 0 else 0

    # Calculate error frequency
    total_successful = len([f for f in os.listdir(done_dir) if f.endswith('.md')]) if os.path.exists(done_dir) else 0
    total_failed = len([f for f in os.listdir(errors_dir) if f.endswith('.md')]) if os.path.exists(errors_dir) else 0
    total_processed = total_successful + total_failed
    metrics["error_frequency"] = (total_failed / total_processed * 100) if total_processed > 0 else 0

    return metrics

def extract_completion_time(content: str, filepath: str) -> float:
    """
    Extract completion time from task file content.
    This function looks for timestamps in the file and calculates the time difference.
    """
    # Try to extract timestamps from the file name (based on the format in CLAUDE.md)
    filename = os.path.basename(filepath)
    # Look for timestamp pattern in filename: YYYYMMDD_HHMMSS
    timestamp_match = re.search(r'(\d{8})_(\d{6})', filename)
    if timestamp_match:
        # If timestamp is in filename, we can't calculate completion time without start time
        # So we'll return 0 or a default value
        return 0

    # If no timestamp in filename, look for timestamps in content
    # This is a simplified approach - in a real system, you'd have structured timestamps
    lines = content.split('\n')
    for line in lines:
        if 'duration' in line.lower() or 'time' in line.lower():
            # Look for time duration patterns like "Duration: 120 seconds" or "Time: 2 mins"
            time_match = re.search(r'(\d+)\s*(seconds|secs|s|min|mins|minutes)', line.lower())
            if time_match:
                time_val = int(time_match.group(1))
                unit = time_match.group(2)

                # Convert to seconds
                if unit.startswith('min'):
                    return time_val * 60
                else:
                    return time_val

    # If no time found, return 0
    return 0

def extract_agent_used(content: str) -> str:
    """Extract agent used from content"""
    lines = content.split('\n')
    for line in lines[:15]:  # Check first 15 lines for agent indicators
        if 'agent' in line.lower():
            parts = line.split()
            for i, part in enumerate(parts):
                if 'agent' in part.lower() and i + 1 < len(parts):
                    return parts[i + 1].strip('.,!?')

    return 'Unknown'