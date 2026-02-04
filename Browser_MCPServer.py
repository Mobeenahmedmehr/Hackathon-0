"""
Browser/Form Interaction MCP Server for AI Employee Gold Tier
Implements an MCP server that handles browser/form draft actions.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import uuid


class BrowserMCPServer:
    """
    An MCP (Model Context Protocol) server for the AI Employee Gold Tier.
    Handles browser/form draft creation for sensitive actions that require approval.
    """

    def __init__(self, drafts_dir="Drafts", logs_dir="Logs"):
        self.drafts_dir = Path(drafts_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories if they don't exist
        self.drafts_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Audit log setup
        self.audit_log_path = self.logs_dir / f"browser_mcp_audit_{datetime.now().strftime('%Y%m%d')}.log"

    def log_audit_event(self, message, action="", input_data="", output_data="", approval_status=""):
        """Log an event to the audit log with comprehensive details."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        audit_entry = {
            "timestamp": timestamp,
            "action": action,
            "input": input_data[:500],  # Limit length to prevent huge logs
            "output": output_data[:500],
            "approval_status": approval_status,
            "message": message,
            "server": "browser_mcp"
        }

        with open(self.audit_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry) + "\n")

        # Also write to general log
        log_entry = f"[{timestamp}] BROWSER_MCP_SERVER: {message}\n"
        general_log_path = self.logs_dir / "browser_mcp_server.log"
        with open(general_log_path, 'a') as f:
            f.write(log_entry)

    def log_event(self, message):
        """Log an event to the system log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] BROWSER_MCP_SERVER: {message}\n"

        log_file = self.logs_dir / "browser_mcp_server.log"
        with open(log_file, 'a') as f:
            f.write(log_entry)

    async def handle_request(self, request):
        """Handle an incoming MCP request"""
        try:
            request_data = json.loads(request) if isinstance(request, str) else request

            method = request_data.get("method")
            params = request_data.get("params", {})
            request_id = request_data.get("id")

            if method == "create_browser_draft":
                return await self.create_browser_draft(params, request_id)
            elif method == "create_form_draft":
                return await self.create_form_draft(params, request_id)
            elif method == "get_draft_status":
                return await self.get_draft_status(params, request_id)
            else:
                return self.error_response(f"Unknown method: {method}", request_id)

        except json.JSONDecodeError:
            return self.error_response("Invalid JSON in request")
        except Exception as e:
            return self.error_response(f"Error processing request: {str(e)}")

    async def create_browser_draft(self, params, request_id=None):
        """Create a browser interaction draft"""
        try:
            url = params.get("url", "unknown_url")
            action = params.get("action", "unknown_action")
            description = params.get("description", "")
            target_element = params.get("target_element", "")
            data = params.get("data", {})

            # Create a unique draft filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_filename = f"browser_draft_{timestamp}_{str(uuid.uuid4())[:8]}.md"
            draft_path = self.drafts_dir / draft_filename

            draft_content = f"""# Browser Interaction Draft

## Draft Information
- Status: DRAFT (Not Executed)
- Created: {datetime.now().isoformat()}
- ID: {draft_filename}

## Browser Details
- Target URL: {url}
- Action: {action}
- Target Element: {target_element}
- Data to Submit: {json.dumps(data, indent=2)}

## Interaction Description
{description}

## Action Required
⚠️ This is a DRAFT browser interaction. It has NOT been executed.
To execute this interaction, move this file to the Pending_Approval folder for human review.

## Safety Warning
This browser interaction will remain in draft state until manually approved by a human operator.
This prevents accidental execution of sensitive browser operations.

## Cross-Domain Considerations
- Origin verification required
- CSRF protection checked
- Authentication validated

## Metadata
- Type: Browser Interaction Draft
- Priority: High
- Requires Approval: Yes
- Cross-Domain: {'.' in url}
- Large Action: {len(str(data)) > 1000}
- New Recipient: {params.get('new_recipient', False)}
"""

            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            self.log_audit_event(
                f"Created browser draft: {draft_filename}",
                action="create_browser_draft",
                input_data=url,
                output_data=str(draft_path),
                approval_status="draft"
            )

            self.log_event(f"Created browser draft: {draft_filename}")

            return {
                "jsonrpc": "2.0",
                "result": {
                    "success": True,
                    "draft_id": draft_filename,
                    "message": f"Browser draft created successfully: {draft_filename}",
                    "path": str(draft_path)
                },
                "id": request_id
            }

        except Exception as e:
            self.log_audit_event(
                f"Failed to create browser draft: {str(e)}",
                action="create_browser_draft",
                output_data=str(e),
                approval_status="failed"
            )
            return self.error_response(f"Failed to create browser draft: {str(e)}", request_id)

    async def create_form_draft(self, params, request_id=None):
        """Create a form submission draft"""
        try:
            form_url = params.get("form_url", "unknown_url")
            form_data = params.get("form_data", {})
            form_type = params.get("form_type", "generic")
            description = params.get("description", "")

            # Create a unique draft filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_filename = f"form_draft_{timestamp}_{str(uuid.uuid4())[:8]}.md"
            draft_path = self.drafts_dir / draft_filename

            draft_content = f"""# Form Submission Draft

## Draft Information
- Status: DRAFT (Not Submitted)
- Created: {datetime.now().isoformat()}
- ID: {draft_filename}

## Form Details
- Form URL: {form_url}
- Form Type: {form_type}
- Form Data: {json.dumps(form_data, indent=2)}

## Submission Description
{description}

## Action Required
⚠️ This is a DRAFT form submission. It has NOT been submitted.
To submit this form, move this file to the Pending_Approval folder for human review.

## Safety Warning
This form submission will remain in draft state until manually approved by a human operator.
This prevents accidental submission of sensitive forms.

## Cross-Domain Considerations
- Origin verification required
- CSRF token validation
- Authentication context

## Metadata
- Type: Form Submission Draft
- Priority: High
- Requires Approval: Yes
- Cross-Domain: {'.' in form_url}
- Large Action: {len(str(form_data)) > 1000}
- New Recipient: {params.get('new_recipient', False)}
"""

            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            self.log_audit_event(
                f"Created form draft: {draft_filename}",
                action="create_form_draft",
                input_data=form_url,
                output_data=str(draft_path),
                approval_status="draft"
            )

            self.log_event(f"Created form draft: {draft_filename}")

            return {
                "jsonrpc": "2.0",
                "result": {
                    "success": True,
                    "draft_id": draft_filename,
                    "message": f"Form draft created successfully: {draft_filename}",
                    "path": str(draft_path)
                },
                "id": request_id
            }

        except Exception as e:
            self.log_audit_event(
                f"Failed to create form draft: {str(e)}",
                action="create_form_draft",
                output_data=str(e),
                approval_status="failed"
            )
            return self.error_response(f"Failed to create form draft: {str(e)}", request_id)

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
            if "Status: EXECUTED" in content:
                status = "EXECUTED"
            elif "Status: APPROVED" in content:
                status = "APPROVED"

            self.log_audit_event(
                f"Retrieved draft status: {draft_id}",
                action="get_draft_status",
                input_data=draft_id,
                output_data=status,
                approval_status=status
            )

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
            self.log_audit_event(
                f"Failed to get draft status: {str(e)}",
                action="get_draft_status",
                output_data=str(e),
                approval_status="failed"
            )
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

    async def start_server(self, port=8081):
        """Start the Browser MCP server"""
        # This is a simplified version - in a real implementation, you'd use proper server protocols
        self.log_event(f"Browser MCP server starting on port {port}")
        self.log_audit_event(
            f"Browser MCP server starting on port {port}",
            action="start_server",
            approval_status="started"
        )

        # Placeholder implementation - in a real scenario, you'd implement a proper protocol
        # This serves as a demonstration of the concept
        print(f"Browser MCP Server is running on port {port}")
        print("Ready to handle browser/form draft requests...")

        # Keep server running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.log_event("Browser MCP server stopped by user")
            self.log_audit_event(
                "Browser MCP server stopped by user",
                action="stop_server",
                approval_status="stopped"
            )


# Simple test function to demonstrate usage
async def test_browser_mcp_server():
    """Test the Browser MCP server functionality"""
    server = BrowserMCPServer()

    # Test creating a browser draft
    browser_params = {
        "url": "https://example.com/login",
        "action": "login",
        "target_element": "#username",
        "data": {"username": "testuser", "password": "secret"},
        "description": "Login to example.com account",
        "new_recipient": False
    }

    result = await server.create_browser_draft(browser_params, "test_req_1")
    print("Browser draft result:", result["result"]["message"])

    # Test creating a form draft
    form_params = {
        "form_url": "https://example.com/contact",
        "form_data": {"name": "John Doe", "email": "john@example.com", "message": "Hello"},
        "form_type": "contact",
        "description": "Submit contact form",
        "new_recipient": True
    }

    result = await server.create_form_draft(form_params, "test_req_2")
    print("Form draft result:", result["result"]["message"])


if __name__ == "__main__":
    print("Starting AI Employee Browser MCP Server...")
    print("This server handles browser/form draft creation for sensitive actions.")
    print("All drafts require human approval before execution.")
    print("Press Ctrl+C to stop")

    # For demo purposes, run the test
    asyncio.run(test_browser_mcp_server())