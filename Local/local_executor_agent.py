#!/usr/bin/env python3
"""
Local Executor Agent for Platinum Tier AI Employee

This agent runs locally and is responsible for:
- Watching Local/Needs_Action
- Verifying signed plans from Cloud
- Enforcing Human-in-the-Loop approval
- Executing steps strictly as written
- Using MCP servers in DRAFT-ONLY mode

The Local Agent MUST NOT:
- Modify Cloud plans
- Perform free-form reasoning
- Execute unsigned or altered plans
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import shutil
import re
from typing import Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LocalExecutorAgent:
    def __init__(self):
        self.needs_action_dir = Path("Local/Needs_Action")
        self.executed_actions_dir = Path("Local/Executed_Actions")
        self.invalid_plans_dir = Path("Local/Invalid_Plans")
        self.cloud_signed_plans_dir = Path("Cloud/Signed_Plans")

        # Create directories if they don't exist
        self.needs_action_dir.mkdir(parents=True, exist_ok=True)
        self.executed_actions_dir.mkdir(parents=True, exist_ok=True)
        self.invalid_plans_dir.mkdir(parents=True, exist_ok=True)
        self.cloud_signed_plans_dir.mkdir(parents=True, exist_ok=True)

        # Reference to MCP servers (for draft-only operations)
        self.mcp_servers = []

        logger.info("Local Executor Agent initialized")

    def verify_plan_signature(self, plan_content: str) -> bool:
        """Verify that the plan signature is valid using the shared verification module."""
        # Import the plan verifier from the shared module
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from Local.plan_verification import verify_plan_signature as verify_func

        # Use the shared verification function
        is_valid, message = verify_func(plan_content)

        if not is_valid:
            logger.warning(f"Plan signature verification failed: {message}")
        else:
            logger.info(f"Plan signature verification passed: {message}")

        return is_valid

    def requires_human_approval(self, plan_content: str) -> bool:
        """Check if a plan requires human approval."""
        content_lower = plan_content.lower()

        # Keywords that indicate sensitive actions requiring approval
        sensitive_keywords = [
            'send email', 'send message', 'draft email', 'draft message',
            'payment', 'pay', 'transfer', 'buy', 'purchase', 'approve transaction',
            'delete', 'remove permanently', 'shutdown', 'terminate', 'cancel subscription',
            'share confidential', 'disclose', 'reveal password', 'access credentials',
            'new recipient', 'large action', 'cross-domain', 'execute file', 'run program'
        ]

        return any(keyword in content_lower for keyword in sensitive_keywords)

    def create_approval_request(self, plan_file_path: Path, plan_content: str) -> bool:
        """Create an approval request for sensitive plans."""
        try:
            # Create an approval request file in Pending_Approval
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            approval_filename = f"platinum_approval_request_{timestamp}_{plan_file_path.stem}.md"

            # Look for Pending_Approval directory in the main project
            pending_approval_dir = Path("Pending_Approval")
            pending_approval_dir.mkdir(exist_ok=True)
            approval_path = pending_approval_dir / approval_filename

            plan_title = "Unknown Plan"
            for line in plan_content.split('\n'):
                if line.startswith('# '):
                    plan_title = line[2:].strip()
                    break

            approval_content = f"""# Platinum Tier Approval Request

## Plan to Execute
**Title:** {plan_title}

## Plan Details
The following plan requires your approval before execution:

```
{plan_content[:2000]}  <!-- Limit to first 2000 chars -->
```

## Action Required
- Review the plan steps carefully
- If approved, move this file to the `Approved` folder
- If rejected, move this file to the `Rejected` folder
- If uncertain, add comments with your concerns before moving

## Safety Check
This plan was flagged as potentially sensitive because it contains operations that require human oversight.

## Metadata
- Requested: {datetime.now().isoformat()}
- Original Plan: {plan_file_path.name}
- Priority: High
- Requires Approval: Yes
- Platinum Tier: Zero-trust execution model

## Plan Signature Status
- Signature verification: {'Passed' if self.verify_plan_signature(plan_content) else 'Failed'}
"""

            with open(approval_path, 'w', encoding='utf-8') as f:
                f.write(approval_content)

            logger.info(f"Created approval request for sensitive plan: {plan_file_path.name}")
            return True

        except Exception as e:
            logger.error(f"Error creating approval request: {str(e)}")
            return False

    def execute_plan_steps(self, plan_content: str) -> bool:
        """Execute the plan steps in draft-only mode."""
        try:
            logger.info("Executing plan steps in draft-only mode...")

            # This is where the Local Agent would execute steps as written
            # For safety, we only simulate execution or use MCP servers in draft mode
            lines = plan_content.split('\n')

            for line_num, line in enumerate(lines, 1):
                line = line.strip()

                # Skip signature blocks and metadata
                if line.startswith('<!--') or 'Hash:' in line or 'Signed:' in line:
                    continue

                # Log each step as it's processed
                if line.startswith('- ') or line.startswith('* ') or line.startswith('#') or 'Step' in line:
                    logger.info(f"Processing step: {line[:100]}...")  # Limit log length

                    # Simulate draft-only execution for sensitive operations
                    if any(op in line.lower() for op in ['email', 'message', 'draft']):
                        logger.info(f"DRAFT mode: Would create draft for: {line[:50]}...")

                    if any(op in line.lower() for op in ['file', 'move', 'copy', 'create']):
                        logger.info(f"DRAFT mode: Would perform file operation: {line[:50]}...")

            logger.info("Plan execution completed in draft-only mode")
            return True

        except Exception as e:
            logger.error(f"Error executing plan steps: {str(e)}")
            return False

    def process_signed_plan(self, plan_file_path: Path) -> bool:
        """Process a signed plan from the Cloud."""
        logger.info(f"Processing signed plan: {plan_file_path.name}")

        try:
            # Read the plan content
            with open(plan_file_path, 'r', encoding='utf-8') as f:
                plan_content = f.read()

            # Verify the plan signature
            if not self.verify_plan_signature(plan_content):
                logger.warning(f"Plan signature verification failed: {plan_file_path.name}")

                # Move to invalid plans directory
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                invalid_filename = f"invalid_{timestamp}_{plan_file_path.name}"
                invalid_path = self.invalid_plans_dir / invalid_filename
                shutil.move(str(plan_file_path), str(invalid_path))

                logger.info(f"Moved invalid plan to: {invalid_path}")
                return False

            # Check if plan requires human approval
            if self.requires_human_approval(plan_content):
                logger.info(f"Plan requires human approval: {plan_file_path.name}")

                # Create approval request and do NOT execute yet
                if self.create_approval_request(plan_file_path, plan_content):
                    # Move the original plan to a processed folder to avoid reprocessing
                    processed_dir = self.cloud_signed_plans_dir / "Processed"
                    processed_dir.mkdir(exist_ok=True)
                    processed_path = processed_dir / plan_file_path.name
                    shutil.move(str(plan_file_path), str(processed_path))

                    logger.info(f"Created approval request and moved plan to Processed folder: {plan_file_path.name}")
                    return True
                else:
                    logger.error(f"Failed to create approval request for: {plan_file_path.name}")
                    return False

            else:
                # Execute the plan in draft-only mode
                logger.info(f"Executing plan in draft-only mode: {plan_file_path.name}")

                if self.execute_plan_steps(plan_content):
                    # Move to executed actions
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    executed_filename = f"executed_{timestamp}_{plan_file_path.name}"
                    executed_path = self.executed_actions_dir / executed_filename
                    shutil.move(str(plan_file_path), str(executed_path))

                    logger.info(f"Successfully executed and moved plan to: {executed_path}")
                    return True
                else:
                    logger.error(f"Failed to execute plan: {plan_file_path.name}")
                    return False

        except Exception as e:
            logger.error(f"Error processing signed plan {plan_file_path.name}: {str(e)}")
            return False

    def scan_and_execute_plans(self) -> int:
        """Scan for and execute all pending signed plans."""
        # First, check for plans that came from Cloud/Signed_Plans
        if not self.cloud_signed_plans_dir.exists():
            return 0

        plan_files = [f for f in self.cloud_signed_plans_dir.iterdir()
                     if f.is_file() and not f.name.startswith('.')]
        executed_count = 0

        for plan_file in plan_files:
            # Skip if it's a directory or a processed folder
            if plan_file.is_dir() or plan_file.name == "Processed":
                continue

            if self.process_signed_plan(plan_file):
                executed_count += 1

        # Also check Local/Needs_Action for any local tasks that need processing
        if self.needs_action_dir.exists():
            local_task_files = [f for f in self.needs_action_dir.iterdir()
                               if f.is_file() and not f.name.startswith('.')]

            for task_file in local_task_files:
                if task_file.is_dir():
                    continue

                # Local tasks need to be sent to cloud for planning first
                # For now, we'll log this as these should be handled by the loop
                logger.debug(f"Local task found: {task_file.name} - should be sent to cloud for planning")

        return executed_count

    def run(self, scan_interval: int = 5):
        """Main run loop for the Local Executor Agent."""
        logger.info("Local Executor Agent started")
        logger.info(f"Monitoring: {self.cloud_signed_plans_dir}")
        logger.info(f"Output to: {self.executed_actions_dir}")

        try:
            while True:
                # Scan and execute plans
                executed_count = self.scan_and_execute_plans()

                if executed_count > 0:
                    logger.info(f"Executed {executed_count} plans")

                # Wait before next scan
                time.sleep(scan_interval)

        except KeyboardInterrupt:
            logger.info("Local Executor Agent stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error in Local Executor Agent: {str(e)}")
            raise


class ZeroTrustValidator:
    """Validates zero-trust boundaries between Cloud and Local."""

    def __init__(self):
        self.cloud_dirs = ["Cloud"]
        self.local_dirs = ["Local", "Inbox", "Needs_Action", "Done", "Pending_Approval", "Approved", "Rejected"]

    def validate_boundary_violation(self, operation: str, source: str, dest: str) -> bool:
        """Validate that an operation doesn't violate zero-trust boundaries."""
        # Cloud should not access Local directories directly
        if source.startswith("Cloud") and any(dest.startswith(local_dir) for local_dir in ["Local/", "Inbox/", "Needs_Action/", "Done/", "Pending_Approval/", "Approved/", "Rejected/"]):
            logger.error(f"ZERO-TRUST VIOLATION: Cloud attempted to access Local directory: {operation} from {source} to {dest}")
            return False

        # Local should not modify Cloud plan directories directly
        if source.startswith("Local") and dest.startswith("Cloud/Signed_Plans"):
            logger.error(f"ZERO-TRUST VIOLATION: Local attempted to modify Cloud plans: {operation} from {source} to {dest}")
            return False

        return True


if __name__ == "__main__":
    agent = LocalExecutorAgent()
    print("Starting Local Executor Agent...")
    print("This agent will:")
    print("- Watch Local/Needs_Action and Cloud/Signed_Plans")
    print("- Verify signed plans from Cloud")
    print("- Enforce Human-in-the-Loop approval")
    print("- Execute steps strictly as written in DRAFT-ONLY mode")
    print("- NEVER modify Cloud plans or perform free-form reasoning")
    print("\nPress Ctrl+C to stop")
    agent.run()