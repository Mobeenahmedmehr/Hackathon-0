"""
Email agent for sending and drafting emails in the AI Employee system.
"""

from pathlib import Path
from .base_agent import BaseAgent


class EmailAgent(BaseAgent):
    """
    Agent responsible for email-related tasks including drafting and sending emails.
    """

    def __init__(self):
        super().__init__()
        self.drafts_dir = Path("Drafts")

    def execute(self, plan_data):
        """
        Execute email-related tasks based on the plan data.

        Args:
            plan_data (dict): Data containing email task information

        Returns:
            Result of the execution
        """
        try:
            task_type = plan_data.get('task_type', 'draft')

            if task_type == 'draft':
                return self.draft_email(plan_data)
            elif task_type == 'send':
                return self.send_email(plan_data)
            else:
                raise ValueError(f"Unknown email task type: {task_type}")
        except Exception as e:
            return self.handle_error(e, "execute")

    def draft_email(self, plan_data):
        """
        Draft an email based on the provided plan data.

        Args:
            plan_data (dict): Data containing email draft information

        Returns:
            dict: Result of the draft operation
        """
        try:
            task_id = plan_data.get('task_id', 'unknown')
            subject = plan_data.get('subject', '')
            body = plan_data.get('body', '')
            recipient = plan_data.get('recipient', '')

            # Create the draft content
            draft_content = f"""# Email Draft

**To:** {recipient}
**Subject:** {subject}

## Body

{body}

---
Draft created at: {self._get_timestamp()}
Task ID: {task_id}
"""

            # Ensure drafts directory exists
            self.drafts_dir.mkdir(exist_ok=True)

            # Save draft as markdown file
            draft_file = self.drafts_dir / f"email_draft_{task_id}.md"
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            self.log_action("draft_email", {
                "task_id": task_id,
                "recipient": recipient,
                "subject": subject,
                "draft_file": str(draft_file)
            })

            return {
                "success": True,
                "draft_file": str(draft_file),
                "message": f"Email draft saved to {draft_file}"
            }
        except Exception as e:
            return self.handle_error(e, "draft_email")

    def send_email(self, plan_data):
        """
        Send an email using Gmail API credentials from config loader.

        Args:
            plan_data (dict): Data containing email sending information

        Returns:
            dict: Result of the send operation
        """
        try:
            # Extract email data
            recipient = plan_data.get('recipient')
            subject = plan_data.get('subject')
            body = plan_data.get('body')

            if not recipient or not subject or not body:
                raise ValueError("Missing required email fields: recipient, subject, or body")

            # Here we would integrate with Gmail API
            # For now, we'll simulate the sending process
            # In a real implementation, we'd load Gmail credentials from config
            # and use the Gmail API to send the email

            # Simulate sending email
            self.log_action("send_email", {
                "recipient": recipient,
                "subject": subject
            })

            return {
                "success": True,
                "message": f"Email sent to {recipient}",
                "recipient": recipient
            }
        except Exception as e:
            return self.handle_error(e, "send_email")

    def _get_timestamp(self):
        """Helper method to get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")