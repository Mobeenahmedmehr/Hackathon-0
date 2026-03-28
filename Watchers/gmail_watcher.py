import os
import time
import base64
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import logging

from config.config_loader import load_config
from utils.paths import get_needs_action_path
from logging_setup import get_logger
from .email_parser import parse_email_payload


def authenticate_gmail():
    """
    Authenticate with Gmail API using OAuth credentials from environment variables.
    """
    logger = get_logger(__name__)

    # Load credentials from environment variables
    client_id = os.getenv('GMAIL_CLIENT_ID')
    client_secret = os.getenv('GMAIL_CLIENT_SECRET')
    refresh_token = os.getenv('GMAIL_REFRESH_TOKEN')

    if not client_id or not client_secret or not refresh_token:
        raise ValueError("Missing Gmail OAuth credentials in environment variables")

    # Create credentials object
    creds = Credentials(
        token=None,  # We'll use the refresh token to get a new access token
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret
    )

    # Build the Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
        logger.info("Successfully authenticated with Gmail API")
        return service
    except Exception as e:
        logger.error(f"Failed to authenticate with Gmail API: {str(e)}")
        raise


def fetch_unread_emails(service):
    """
    Fetch unread emails from Gmail.

    Args:
        service: Authenticated Gmail service object

    Returns:
        List of dictionaries containing email information
    """
    logger = get_logger(__name__)

    try:
        # Query for unread emails
        results = service.users().messages().list(
            userId='me',
            q='is:unread'
        ).execute()

        messages = results.get('messages', [])
        emails = []

        for message in messages:
            msg_id = message['id']

            # Get the full message
            msg = service.users().messages().get(
                userId='me',
                id=msg_id
            ).execute()

            # Extract email parts
            headers = msg['payload']['headers']
            sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown')
            subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')

            # Extract timestamp
            timestamp_raw = next((header['value'] for header in headers if header['name'].lower() == 'date'), '')
            try:
                # Convert Gmail timestamp to readable format
                timestamp = datetime.fromtimestamp(int(msg['internalDate'])/1000).strftime('%Y-%m-%d %H:%M:%S')
            except:
                timestamp = timestamp_raw

            # Extract body text
            body_text = parse_email_payload(msg['payload'])

            email_data = {
                'email_id': msg_id,
                'sender': sender,
                'subject': subject,
                'body_text': body_text,
                'timestamp': timestamp
            }

            emails.append(email_data)

        logger.info(f"Fetched {len(emails)} unread emails")
        return emails

    except Exception as e:
        logger.error(f"Failed to fetch unread emails: {str(e)}")
        return []


def create_task_file(email_data):
    """
    Create a markdown task file from email data.

    Args:
        email_data: Dictionary containing email information
    """
    logger = get_logger(__name__)

    # Create the markdown content
    task_content = f"""# Task

Source: Gmail
Sender: {email_data['sender']}
Timestamp: {email_data['timestamp']}

Subject: {email_data['subject']}

Message:
{email_data['body_text']}
"""

    # Define the file path
    task_filename = f"email_{email_data['email_id']}.md"
    task_path = os.path.join(get_needs_action_path(), task_filename)

    # Write the task file
    try:
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(task_content)

        logger.info(f"Created task file: {task_path}")
        return task_path
    except Exception as e:
        logger.error(f"Failed to create task file {task_path}: {str(e)}")
        raise


def mark_email_as_read(service, email_id):
    """
    Mark an email as read by removing the 'UNREAD' label.

    Args:
        service: Authenticated Gmail service object
        email_id: ID of the email to mark as read
    """
    logger = get_logger(__name__)

    try:
        # Remove the UNREAD label from the email
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

        logger.info(f"Marked email {email_id} as read")
    except Exception as e:
        logger.error(f"Failed to mark email {email_id} as read: {str(e)}")


def process_new_emails():
    """
    Main pipeline to process new emails:
    1. Authenticate with Gmail
    2. Fetch unread emails
    3. Convert each email to task file
    4. Mark emails as read
    5. Log results
    """
    logger = get_logger(__name__)

    try:
        # Authenticate with Gmail
        service = authenticate_gmail()

        # Fetch unread emails
        emails = fetch_unread_emails(service)

        processed_count = 0

        for email_data in emails:
            try:
                # Check if task file already exists to prevent duplicates
                task_filename = f"email_{email_data['email_id']}.md"
                task_path = os.path.join(get_needs_action_path(), task_filename)

                if os.path.exists(task_path):
                    logger.info(f"Task file already exists for email {email_data['email_id']}, skipping...")
                    continue

                # Create task file
                create_task_file(email_data)

                # Mark email as read
                mark_email_as_read(service, email_data['email_id'])

                processed_count += 1

            except Exception as e:
                logger.error(f"Failed to process email {email_data['email_id']}: {str(e)}")

        logger.info(f"Processed {processed_count} new emails")

    except Exception as e:
        logger.error(f"Error in process_new_emails: {str(e)}")


def run_watcher_loop():
    """
    Continuously check Gmail every 60 seconds.
    """
    logger = get_logger(__name__)

    logger.info("Starting Gmail watcher loop...")

    while True:
        try:
            process_new_emails()
            time.sleep(60)  # Wait 60 seconds before next check
        except KeyboardInterrupt:
            logger.info("Gmail watcher stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in watcher loop: {str(e)}")
            time.sleep(60)  # Wait before retrying


if __name__ == "__main__":
    print("Starting AI Employee Gmail Watcher...")
    print("Monitoring Gmail for new emails...")
    print("Press Ctrl+C to stop")
    run_watcher_loop()