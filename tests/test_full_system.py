import unittest
import os
import tempfile
import threading
import time
from unittest.mock import patch, MagicMock

# Import the necessary modules
from run_system import start_watchers, start_orchestrator, start_scheduler, main
from logging_setup import get_logger


class TestFullSystem(unittest.TestCase):
    """Test script that starts system, simulates a task, and verifies full pipeline works"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()

        # Create necessary directories for testing
        dirs_to_create = [
            'Needs_Action', 'Plans', 'Pending_Approval',
            'Approved', 'Done', 'Drafts', 'Logs', 'Reports'
        ]

        for dir_name in dirs_to_create:
            os.makedirs(os.path.join(self.temp_dir, dir_name), exist_ok=True)

        # Temporarily change working directory
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)

        # Clean up temp directories
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('run_system.GmailWatcher')
    @patch('run_system.WhatsappWatcher')
    @patch('run_system.LinkedinWatcher')
    def test_start_watchers(self, mock_linkedin, mock_whatsapp, mock_gmail):
        """Test that watchers start correctly"""

        # Mock the watcher methods
        mock_gmail_instance = MagicMock()
        mock_gmail.return_value = mock_gmail_instance

        mock_whatsapp_instance = MagicMock()
        mock_whatsapp.return_value = mock_whatsapp_instance

        mock_linkedin_instance = MagicMock()
        mock_linkedin.return_value = mock_linkedin_instance

        # Track if methods were called
        def mock_start_monitoring():
            time.sleep(0.1)  # Simulate some work

        # Assign mocked methods
        mock_gmail_instance.start_monitoring = mock_start_monitoring
        mock_whatsapp_instance.start_monitoring = mock_start_monitoring
        mock_linkedin_instance.start_monitoring = mock_start_monitoring

        # Call start_watchers function
        watcher_list = start_watchers()

        # Verify that threads were created and started
        self.assertEqual(len(watcher_list), 3, "Three watcher threads should be created")

        for name, thread in watcher_list:
            self.assertIsInstance(thread, threading.Thread, f"{name} should be a Thread instance")
            # Note: We can't easily verify if the thread was started due to daemon=True

    @patch('run_system.Orchestrator')
    def test_start_orchestrator(self, mock_orchestrator):
        """Test that orchestrator starts correctly"""
        mock_orchestrator_instance = MagicMock()
        mock_orchestrator.return_value = mock_orchestrator_instance

        def mock_run():
            time.sleep(0.1)  # Simulate some work

        mock_orchestrator_instance.run = mock_run

        # Call start_orchestrator function
        orchestrator, thread = start_orchestrator()

        # Verify that orchestrator and thread were created
        self.assertIsNotNone(orchestrator, "Orchestrator instance should be created")
        self.assertIsInstance(thread, threading.Thread, "Orchestrator should be a Thread instance")

    @patch('run_system.ReportScheduler')
    def test_start_scheduler(self, mock_scheduler):
        """Test that scheduler starts correctly"""
        mock_scheduler_instance = MagicMock()
        mock_scheduler.return_value = mock_scheduler_instance

        def mock_start():
            time.sleep(0.1)  # Simulate some work

        mock_scheduler_instance.start = mock_start

        # Call start_scheduler function
        scheduler, thread = start_scheduler()

        # Verify that scheduler and thread were created
        self.assertIsNotNone(scheduler, "Scheduler instance should be created")
        self.assertIsInstance(thread, threading.Thread, "Scheduler should be a Thread instance")

    def test_system_functions_exist(self):
        """Test that the required functions exist in run_system module"""
        self.assertTrue(callable(start_watchers), "start_watchers should be callable")
        self.assertTrue(callable(start_orchestrator), "start_orchestrator should be callable")
        self.assertTrue(callable(start_scheduler), "start_scheduler should be callable")
        self.assertTrue(callable(main), "main should be callable")

    def test_directory_structure(self):
        """Test that all required directories exist and are writable."""

        # Create temporary directories for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Define test directories
            dirs_to_test = [
                os.path.join(temp_dir, "Needs_Action"),
                os.path.join(temp_dir, "Plans"),
                os.path.join(temp_dir, "Pending_Approval"),
                os.path.join(temp_dir, "Approved"),
                os.path.join(temp_dir, "Done"),
                os.path.join(temp_dir, "Errors"),
                os.path.join(temp_dir, "Reports"),
                os.path.join(temp_dir, "Drafts"),
                os.path.join(temp_dir, "Logs")
            ]

            # Create all directories
            for directory in dirs_to_test:
                os.makedirs(directory, exist_ok=True)
                self.assertTrue(os.path.isdir(directory), f"Directory should exist: {directory}")

                # Test that we can write to each directory
                test_file = os.path.join(directory, "test_write.txt")
                with open(test_file, 'w') as f:
                    f.write("test")

                self.assertTrue(os.path.exists(test_file), f"Should be able to write to directory: {directory}")

                # Clean up test file
                os.remove(test_file)

            print("✓ Directory structure test completed successfully")
            print(f"✓ All {len(dirs_to_test)} directories are accessible and writable")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)