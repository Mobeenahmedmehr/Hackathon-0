"""
Task manager for the AI Employee system
Handles task lifecycle operations
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class TaskManager:
    """
    Manages the lifecycle of tasks in the AI Employee system
    """

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.needs_action_dir = self.base_dir / "Needs_Action"
        self.plans_dir = self.base_dir / "Plans"
        self.pending_approval_dir = self.base_dir / "Pending_Approval"
        self.approved_dir = self.base_dir / "Approved"
        self.done_dir = self.base_dir / "Done"
        self.errors_dir = self.base_dir / "Errors"

        # Create directories if they don't exist
        for dir_path in [self.needs_action_dir, self.plans_dir,
                         self.pending_approval_dir, self.approved_dir,
                         self.done_dir, self.errors_dir]:
            dir_path.mkdir(exist_ok=True)

    def create_task(self, task_data: Dict, destination: str = "Needs_Action") -> str:
        """
        Create a new task file

        Args:
            task_data: Dictionary containing task information
            destination: Destination folder (default: Needs_Action)

        Returns:
            Path to the created task file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"task_{timestamp}.md"

        if destination == "Needs_Action":
            filepath = self.needs_action_dir / filename
        elif destination == "Plans":
            filepath = self.plans_dir / filename
        elif destination == "Pending_Approval":
            filepath = self.pending_approval_dir / filename
        elif destination == "Approved":
            filepath = self.approved_dir / filename
        elif destination == "Done":
            filepath = self.done_dir / filename
        elif destination == "Errors":
            filepath = self.errors_dir / filename
        else:
            raise ValueError(f"Invalid destination: {destination}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {task_data.get('title', 'Untitled Task')}\n\n")
            f.write(f"Created: {datetime.now().isoformat()}\n\n")

            for key, value in task_data.items():
                if key != 'title':
                    f.write(f"**{key.replace('_', ' ').title()}**: {value}\n")

        return str(filepath)

    def move_task(self, task_path: str, destination: str) -> str:
        """
        Move a task file to a different directory

        Args:
            task_path: Current path of the task file
            destination: Destination folder

        Returns:
            New path of the task file
        """
        task_path = Path(task_path)
        if not task_path.exists():
            raise FileNotFoundError(f"Task file does not exist: {task_path}")

        if destination == "Needs_Action":
            dest_dir = self.needs_action_dir
        elif destination == "Plans":
            dest_dir = self.plans_dir
        elif destination == "Pending_Approval":
            dest_dir = self.pending_approval_dir
        elif destination == "Approved":
            dest_dir = self.approved_dir
        elif destination == "Done":
            dest_dir = self.done_dir
        elif destination == "Errors":
            dest_dir = self.errors_dir
        else:
            raise ValueError(f"Invalid destination: {destination}")

        new_path = dest_dir / task_path.name
        os.rename(task_path, new_path)

        return str(new_path)

    def get_tasks(self, source: str = "Needs_Action") -> List[str]:
        """
        Get list of task files from a specific directory

        Args:
            source: Source directory to get tasks from

        Returns:
            List of task file paths
        """
        if source == "Needs_Action":
            src_dir = self.needs_action_dir
        elif source == "Plans":
            src_dir = self.plans_dir
        elif source == "Pending_Approval":
            src_dir = self.pending_approval_dir
        elif source == "Approved":
            src_dir = self.approved_dir
        elif source == "Done":
            src_dir = self.done_dir
        elif source == "Errors":
            src_dir = self.errors_dir
        else:
            raise ValueError(f"Invalid source: {source}")

        return [str(file_path) for file_path in src_dir.glob("*.md")]

    def read_task(self, task_path: str) -> str:
        """
        Read the content of a task file

        Args:
            task_path: Path to the task file

        Returns:
            Content of the task file
        """
        with open(task_path, 'r', encoding='utf-8') as f:
            return f.read()

def get_task_manager() -> TaskManager:
    """
    Create and return a task manager instance

    Returns:
        TaskManager instance
    """
    return TaskManager()