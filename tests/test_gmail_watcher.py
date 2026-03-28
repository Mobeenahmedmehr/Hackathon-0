import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Watchers.gmail_watcher import authenticate_gmail, fetch_unread_emails, process_new_emails, create_task_file, mark_email_as_read


class TestGmailWatcher(unittest.TestCase):
    """
    Test suite for Gmail watcher functionality.
    """

    @patch.dict(os.environ, {
        'GMAIL_CLIENT_ID': 'test_client_id',
        'GMAIL_CLIENT_SECRET': 'test_client_secret',
        'GMAIL_REFRESH_TOKEN': 'test_refresh_token'
    })
    @patch('Watchers.gmail_watcher.build')
    def test_authenticate_gmail(self, mock_build):
        """
        Test Gmail authentication function.
        """
        # Mock the service creation
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Call the function
        service = authenticate_gmail()

        # Verify the service was created correctly
        self.assertEqual(service, mock_service)
        mock_build.assert_called_once()

    @patch('Watchers.gmail_watcher.parse_email_payload')
    def test_fetch_unread_emails(self, mock_parse):
        """
        Test fetching unread emails from Gmail service.
        """
        # Mock the Gmail service
        mock_service = MagicMock()

        # Mock the response from the Gmail API
        mock_results = {
            'messages': [
                {
                    'id': 'test_email_id_1'
                }
            ]
        }

        # Mock the individual message response
        mock_message = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'Subject', 'value': 'Test Subject'},
                    {'name': 'Date', 'value': 'Mon, 15 Mar 2026 10:30:00 GMT'}
                ],
                'parts': []
            },
            'internalDate': '1742112600000'  # Timestamp in milliseconds
        }

        # Configure the mock service to return the expected responses
        mock_service.users().messages().list().execute.return_value = mock_results
        mock_service.users().messages().get().execute.return_value = mock_message

        # Mock the parse_email_payload function
        mock_parse.return_value = 'Test email body'

        # Call the function
        emails = fetch_unread_emails(mock_service)

        # Verify the results
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0]['sender'], 'sender@example.com')
        self.assertEqual(emails[0]['subject'], 'Test Subject')
        self.assertEqual(emails[0]['body_text'], 'Test email body')
        self.assertEqual(emails[0]['email_id'], 'test_email_id_1')

    @patch('Watchers.gmail_watcher.get_needs_action_path')
    def test_create_task_file(self, mock_get_path):
        """
        Test creating a task file from email data.
        """
        # Mock the path function
        mock_get_path.return_value = '/mock/path'

        # Sample email data
        email_data = {
            'email_id': 'test_email_id',
            'sender': 'sender@example.com',
            'subject': 'Test Subject',
            'body_text': 'Test email body content',
            'timestamp': '2026-03-15 10:30:00'
        }

        # Mock the file writing
        with patch('builtins.open', create=True) as mock_open:
            # Call the function
            task_path = create_task_file(email_data)

            # Verify the file was opened correctly
            mock_open.assert_called_once()
            handle = mock_open()
            handle.write.assert_called_once()

            # Check that the path was constructed correctly
            expected_path = '/mock/path/email_test_email_id.md'
            self.assertEqual(task_path, expected_path)

    @patch('Watchers.gmail_watcher.build')
    def test_mark_email_as_read(self, mock_build):
        """
        Test marking an email as read.
        """
        # Mock the Gmail service
        mock_service = MagicMock()

        # Mock the users().messages().modify() chain
        mock_modify = mock_service.users().messages().modify()
        mock_modify.execute.return_value = {}

        # Call the function
        mark_email_as_read(mock_service, 'test_email_id')

        # Verify the modify call was made correctly
        mock_service.users().messages().modify.assert_called_once_with(
            userId='me',
            id='test_email_id',
            body={'removeLabelIds': ['UNREAD']}
        )

    @patch('Watchers.gmail_watcher.authenticate_gmail')
    @patch('Watchers.gmail_watcher.fetch_unread_emails')
    @patch('Watchers.gmail_watcher.create_task_file')
    @patch('Watchers.gmail_watcher.mark_email_as_read')
    def test_process_new_emails(self, mock_mark_read, mock_create_task, mock_fetch_emails, mock_auth):
        """
        Test the process_new_emails function.
        """
        # Mock the service and email data
        mock_service = MagicMock()
        mock_auth.return_value = mock_service

        mock_email_data = [
            {
                'email_id': 'test_email_id',
                'sender': 'sender@example.com',
                'subject': 'Test Subject',
                'body_text': 'Test body',
                'timestamp': '2026-03-15 10:30:00'
            }
        ]

        mock_fetch_emails.return_value = mock_email_data
        mock_create_task.return_value = '/path/to/task/file.md'

        # Call the function
        process_new_emails()

        # Verify the functions were called
        mock_auth.assert_called_once()
        mock_fetch_emails.assert_called_once_with(mock_service)
        mock_create_task.assert_called_once()
        mock_mark_read.assert_called_once_with(mock_service, 'test_email_id')


if __name__ == '__main__':
    unittest.main()