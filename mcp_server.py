"""
MCP Server for AI Employee Silver Tier
Implements an MCP server that handles draft actions like email drafts.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path


class MCPServer:
    """
    An MCP (Model Context Protocol) server for the AI Employee Silver Tier.
    Handles draft creation for sensitive actions that require approval.
    """

    def __init__(self, drafts_dir="Drafts", logs_dir="Logs"):
        self.drafts_dir = Path(drafts_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories if they don't exist
        self.drafts_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] MCP_SERVER: {message}\n"

        log_file = self.logs_dir / "mcp_server.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    async def handle_request(self, request):
        """Handle an incoming MCP request"""
        try:
            request_data = json.loads(request) if isinstance(request, str) else request

            method = request_data.get("method")
            params = request_data.get("params", {})
            request_id = request_data.get("id")

            if method == "create_draft_email":
                return await self.create_draft_email(params, request_id)
            elif method == "create_draft_message":
                return await self.create_draft_message(params, request_id)
            elif method == "get_draft_status":
                return await self.get_draft_status(params, request_id)
            else:
                return self.error_response(f"Unknown method: {method}", request_id)

        except json.JSONDecodeError:
            return self.error_response("Invalid JSON in request")
        except Exception as e:
            return self.error_response(f"Error processing request: {str(e)}")

    async def create_draft_email(self, params, request_id=None):
        """Create a draft email"""
        try:
            subject = params.get("subject", "Untitled Draft")
            recipient = params.get("recipient", "unknown@example.com")
            body = params.get("body", "")
            sender = params.get("sender", "employee@company.com")

            # Create a unique draft filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_filename = f"email_draft_{timestamp}_{subject.replace(' ', '_').replace('/', '_')}.md"
            draft_path = self.drafts_dir / draft_filename

            draft_content = f"""# Email Draft

## Draft Information
- Status: DRAFT (Not Sent)
- Created: {datetime.now().isoformat()}
- ID: {draft_filename}

## Email Details
- From: {sender}
- To: {recipient}
- Subject: {subject}

## Email Body
{body}

## Action Required
⚠️ This is a DRAFT email. It has NOT been sent.
To send this email, move this file to the Pending_Approval folder for human review.

## Safety Warning
This email will remain in draft state until manually approved by a human operator.
This prevents accidental sending of sensitive communications.

## Metadata
- Type: Email Draft
- Priority: Normal
- Requires Approval: Yes
"""

            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            self.log_event(f"Created email draft: {draft_filename}")

            return {
                "jsonrpc": "2.0",
                "result": {
                    "success": True,
                    "draft_id": draft_filename,
                    "message": f"Email draft created successfully: {draft_filename}",
                    "path": str(draft_path)
                },
                "id": request_id
            }

        except Exception as e:
            return self.error_response(f"Failed to create email draft: {str(e)}", request_id)

    async def create_draft_message(self, params, request_id=None):
        """Create a draft message"""
        try:
            recipient = params.get("recipient", "unknown")
            platform = params.get("platform", "unknown")
            content = params.get("content", "")
            subject = params.get("subject", "Message Draft")

            # Create a unique draft filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_filename = f"message_draft_{timestamp}_{platform}_{recipient.replace(' ', '_').replace('/', '_')}.md"
            draft_path = self.drafts_dir / draft_filename

            draft_content = f"""# Message Draft

## Draft Information
- Status: DRAFT (Not Sent)
- Platform: {platform}
- Created: {datetime.now().isoformat()}
- ID: {draft_filename}

## Message Details
- To: {recipient}
- Subject/Topic: {subject}

## Message Content
{content}

## Action Required
⚠️ This is a DRAFT message. It has NOT been sent.
To send this message, move this file to the Pending_Approval folder for human review.

## Safety Warning
This message will remain in draft state until manually approved by a human operator.
This prevents accidental sending of sensitive communications.

## Metadata
- Type: Message Draft
- Priority: Normal
- Requires Approval: Yes
"""

            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            self.log_event(f"Created message draft: {draft_filename}")

            return {
                "jsonrpc": "2.0",
                "result": {
                    "success": True,
                    "draft_id": draft_filename,
                    "message": f"Message draft created successfully: {draft_filename}",
                    "path": str(draft_path)
                },
                "id": request_id
            }

        except Exception as e:
            return self.error_response(f"Failed to create message draft: {str(e)}", request_id)

    async def get_draft_status(self, params, request_id=None):
        """Get the status of a draft"""
        try:
            draft_id = params.get("draft_id")
            if not draft_id:
                return self.error_response("draft_id parameter is required", request_id)

            draft_path = self.drafts_dir / draft_id
            if not draft_path.exists():
                return self.error_response(f"Draft not found: {draft_id}", request_id)

            # Read draft file to determine status
            with open(draft_path, 'r', encoding='utf-8') as f:
                content = f.read()

            status = "DRAFT"  # All files in Drafts folder are drafts
            if "Status: SENT" in content:
                status = "SENT"
            elif "Status: APPROVED" in content:
                status = "APPROVED"

            return {
                "jsonrpc": "2.0",
                "result": {
                    "draft_id": draft_id,
                    "status": status,
                    "path": str(draft_path),
                    "size": draft_path.stat().st_size
                },
                "id": request_id
            }

        except Exception as e:
            return self.error_response(f"Failed to get draft status: {str(e)}", request_id)

    def error_response(self, message, request_id=None):
        """Create an error response"""
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,  # Invalid Request
                "message": message
            },
            "id": request_id
        }

    async def start_server(self, port=8080):
        """Start the MCP server"""
        # This is a simplified version - in a real implementation, you'd use proper server protocols
        self.log_event(f"MCP server starting on port {port}")

        # Placeholder implementation - in a real scenario, you'd implement a proper protocol
        # This serves as a demonstration of the concept
        print(f"MCP Server is running on port {port}")
        print("Ready to handle draft requests...")

        # Keep server running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.log_event("MCP server stopped by user")


# Simple test function to demonstrate usage
async def test_mcp_server():
    """Test the MCP server functionality"""
    server = MCPServer()

    # Test creating an email draft
    email_params = {
        "subject": "Quarterly Report",
        "recipient": "manager@company.com",
        "body": "Please find attached the quarterly report...",
        "sender": "employee@company.com",
        "id": "test_req_1"
    }

    result = await server.create_draft_email(email_params, "test_req_1")
    print("Email draft result:", result["result"]["message"])

    # Test creating a message draft
    msg_params = {
        "recipient": "team@company.com",
        "platform": "Slack",
        "content": "Team meeting reminder for tomorrow at 10 AM.",
        "subject": "Meeting Reminder",
        "id": "test_req_2"
    }

    result = await server.create_draft_message(msg_params, "test_req_2")
    print("Message draft result:", result["result"]["message"])


if __name__ == "__main__":
    print("Starting AI Employee MCP Server...")
    print("This server handles draft creation for sensitive actions.")
    print("All drafts require human approval before sending.")
    print("Press Ctrl+C to stop")

    # For demo purposes, run the test
    asyncio.run(test_mcp_server())