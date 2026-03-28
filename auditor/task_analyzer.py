import os
import json
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

def analyze_completed_tasks(done_dir: str = "Done/", errors_dir: str = "Errors/") -> Dict[str, Any]:
    """
    Analyze completed tasks and extract statistics.

    Args:
        done_dir: Directory containing successful task files
        errors_dir: Directory containing failed task files

    Returns:
        Dictionary containing structured statistics
    """
    stats = {
        "total_tasks": 0,
        "successful_tasks": 0,
        "failed_tasks": 0,
        "task_types": {},
        "agents_used": {},
        "tools_used": {}
    }

    # Process successful tasks
    if os.path.exists(done_dir):
        for filename in os.listdir(done_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(done_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    stats["successful_tasks"] += 1
                    stats["total_tasks"] += 1

                    # Extract task type, agent, and tools used from content
                    task_type = extract_task_type(content)
                    agent_used = extract_agent_used(content)
                    tools_used = extract_tools_used(content)

                    # Update statistics
                    if task_type:
                        stats["task_types"][task_type] = stats["task_types"].get(task_type, 0) + 1
                    if agent_used:
                        stats["agents_used"][agent_used] = stats["agents_used"].get(agent_used, 0) + 1
                    for tool in tools_used:
                        stats["tools_used"][tool] = stats["tools_used"].get(tool, 0) + 1

                except Exception as e:
                    logger.error(f"Error analyzing successful task {filepath}: {str(e)}")

    # Process failed tasks
    if os.path.exists(errors_dir):
        for filename in os.listdir(errors_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(errors_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    stats["failed_tasks"] += 1
                    stats["total_tasks"] += 1

                    # Extract task type, agent, and tools used from content
                    task_type = extract_task_type(content)
                    agent_used = extract_agent_used(content)
                    tools_used = extract_tools_used(content)

                    # Update statistics
                    if task_type:
                        stats["task_types"][task_type] = stats["task_types"].get(task_type, 0) + 1
                    if agent_used:
                        stats["agents_used"][agent_used] = stats["agents_used"].get(agent_used, 0) + 1
                    for tool in tools_used:
                        stats["tools_used"][tool] = stats["tools_used"].get(tool, 0) + 1

                except Exception as e:
                    logger.error(f"Error analyzing failed task {filepath}: {str(e)}")

    return stats

def extract_task_type(content: str) -> str:
    """Extract task type from content"""
    # Look for common indicators of task types in the content
    lines = content.split('\n')
    for line in lines[:10]:  # Check first 10 lines for type indicators
        line_lower = line.lower()
        if 'email' in line_lower:
            return 'Email'
        elif 'lead' in line_lower:
            return 'Lead Generation'
        elif 'task' in line_lower and 'created' in line_lower:
            return 'Task Creation'
        elif 'approval' in line_lower:
            return 'Approval Request'
        elif 'report' in line_lower:
            return 'Report Generation'

    return 'General'

def extract_agent_used(content: str) -> str:
    """Extract agent used from content"""
    # Look for agent indicators in the content
    lines = content.split('\n')
    for line in lines[:15]:  # Check first 15 lines for agent indicators
        if 'agent' in line.lower():
            parts = line.split()
            for i, part in enumerate(parts):
                if 'agent' in part.lower() and i + 1 < len(parts):
                    return parts[i + 1].strip('.,!?')

    return 'Unknown'

def extract_tools_used(content: str) -> List[str]:
    """Extract tools used from content"""
    tools = []
    lines = content.split('\n')
    for line in lines:
        line_lower = line.lower()
        if 'tool' in line_lower or 'api' in line_lower:
            # Look for common tools mentioned in content
            if 'gmail' in line_lower:
                tools.append('Gmail API')
            if 'browser' in line_lower or 'playwright' in line_lower:
                tools.append('Browser Automation')
            if 'email' in line_lower:
                tools.append('Email Sender')
            if 'whatsapp' in line_lower:
                tools.append('WhatsApp API')
            if 'slack' in line_lower:
                tools.append('Slack API')

    return list(set(tools))  # Remove duplicates