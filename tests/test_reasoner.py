#!/usr/bin/env python3
"""
Test script for the AI reasoner module.

This script loads a sample task from Needs_Action/ and calls generate_plan(),
then prints the generated plan path.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path so imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai.ai_reasoner import generate_plan
from config.paths import NEEDS_ACTION_DIR, PLANS_DIR

def test_reasoner():
    """
    Test the AI reasoner by processing a sample task.
    """
    print("Testing AI Reasoner...")

    # Get the paths
    needs_action_dir = NEEDS_ACTION_DIR

    # Look for a sample task in Needs_Action/
    sample_tasks = list(needs_action_dir.glob("*.md"))

    if not sample_tasks:
        # Create a sample task for testing if none exist
        sample_task_content = """# Source: Gmail
# From: client@example.com
# Timestamp: 2023-10-15 14:30:00

Please respond to this email inquiry about our services. The client is interested in learning more about our premium offerings and has asked for a quote."""

        sample_task_path = needs_action_dir / "sample_task.md"
        with open(sample_task_path, 'w', encoding='utf-8') as f:
            f.write(sample_task_content)

        sample_tasks = [sample_task_path]
        print(f"Created sample task: {sample_task_path}")

    # Process the first sample task
    task_path = sample_tasks[0]
    print(f"Processing task: {task_path}")

    try:
        plan_path = generate_plan(str(task_path))
        print(f"Plan generated successfully: {plan_path}")

        # Print the content of the generated plan
        print("\nGenerated Plan Content:")
        print("-" * 30)
        with open(plan_path, 'r', encoding='utf-8') as f:
            print(f.read())

    except Exception as e:
        print(f"Error generating plan: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reasoner()