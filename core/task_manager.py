import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
import logging

from logging_setup import get_logger


class TaskManager:
    """
    Manage task lifecycle.
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    def create_task_id(self):
        """
        Generate a unique task ID.
        """
        task_id = str(uuid.uuid4())
        self.logger.debug(f"Created new task ID: {task_id}")
        return task_id

    def move_task(self, src, dst):
        """
        Move a task file from source to destination.
        """
        logger = self.logger

        try:
            src_path = Path(src)
            dst_path = Path(dst)

            # Ensure destination directory exists
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(src_path), str(dst_path))

            logger.info(f"Moved task from {src} to {dst}")
            return True

        except Exception as e:
            logger.error(f"Failed to move task from {src} to {dst}: {str(e)}")
            return False

    def mark_task_done(self, task_id):
        """
        Mark a task as done by moving it to the Done folder.
        """
        logger = self.logger

        # Find the task file by task_id in any of the working directories
        # We'll search in Needs_Action, Plans, and Pending_Approval directories
        from utils.paths import get_needs_action_path, get_plans_path, get_pending_approval_path, get_done_path

        search_dirs = [
            get_needs_action_path(),
            get_plans_path(),
            get_pending_approval_path()
        ]

        task_file = None
        for dir_path in search_dirs:
            for file_path in Path(dir_path).iterdir():
                if file_path.is_file() and task_id in file_path.name:
                    task_file = file_path
                    break
            if task_file:
                break

        if not task_file:
            logger.warning(f"Task file with ID {task_id} not found for marking as done")
            return False

        # Move to Done directory
        done_path = get_done_path()
        new_path = os.path.join(done_path, f"done_{task_file.name}")

        try:
            shutil.move(str(task_file), new_path)
            logger.info(f"Marked task {task_id} as done: moved to {new_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to mark task {task_id} as done: {str(e)}")
            return False

    def mark_task_error(self, task_id):
        """
        Mark a task as having an error by moving it to the Errors folder.
        """
        logger = self.logger

        # Find the task file by task_id in any of the working directories
        from utils.paths import get_needs_action_path, get_plans_path, get_pending_approval_path, get_approved_path, get_errors_path

        search_dirs = [
            get_needs_action_path(),
            get_plans_path(),
            get_pending_approval_path(),
            get_approved_path()
        ]

        task_file = None
        for dir_path in search_dirs:
            for file_path in Path(dir_path).iterdir():
                if file_path.is_file() and task_id in file_path.name:
                    task_file = file_path
                    break
            if task_file:
                break

        if not task_file:
            logger.warning(f"Task file with ID {task_id} not found for marking as error")
            return False

        # Move to Errors directory
        errors_path = get_errors_path()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        error_path = os.path.join(errors_path, f"error_{timestamp}_{task_file.name}")

        try:
            shutil.move(str(task_file), error_path)
            logger.info(f"Marked task {task_id} as error: moved to {error_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to mark task {task_id} as error: {str(e)}")
            return False


def create_task_id():
    """
    Standalone function to create a task ID.
    """
    tm = TaskManager()
    return tm.create_task_id()


def move_task(src, dst):
    """
    Standalone function to move a task.
    """
    tm = TaskManager()
    return tm.move_task(src, dst)


def mark_task_done(task_id):
    """
    Standalone function to mark a task as done.
    """
    tm = TaskManager()
    return tm.mark_task_done(task_id)


def mark_task_error(task_id):
    """
    Standalone function to mark a task as error.
    """
    tm = TaskManager()
    return tm.mark_task_error(task_id)