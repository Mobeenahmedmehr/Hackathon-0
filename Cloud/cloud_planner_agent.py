#!/usr/bin/env python3
"""
Cloud Planner Agent for Platinum Tier AI Employee

This agent runs in the cloud and is responsible for:
- Reading tasks from Cloud/Incoming_Tasks
- Generating multi-domain plans
- Applying policy checks
- Producing SIGNED plans (conceptual hash/signature)
- Writing plans to Cloud/Signed_Plans

The Cloud Agent MUST NOT:
- Execute files
- Invoke MCP servers
- Modify Local directories
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

class CloudPlannerAgent:
    def __init__(self):
        self.incoming_tasks_dir = Path("Cloud/Incoming_Tasks")
        self.signed_plans_dir = Path("Cloud/Signed_Plans")

        # Create directories if they don't exist
        self.incoming_tasks_dir.mkdir(parents=True, exist_ok=True)
        self.signed_plans_dir.mkdir(parents=True, exist_ok=True)

        # Initialize policy checker
        self.policy_checker = PolicyChecker()

        logger.info("Cloud Planner Agent initialized")

    def sign_plan(self, plan_content: str) -> str:
        """Add signature block to the plan using the shared verification module."""
        # Import the plan signer from the shared module
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from Local.plan_verification import sign_plan as sign_plan_func

        # Use the shared signing function
        return sign_plan_func(plan_content, {"source": "CloudPlannerAgent", "tier": "Platinum"})

    def read_task_file(self, task_file_path: Path) -> Optional[Dict]:
        """Read and parse a task file."""
        try:
            with open(task_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic parsing of markdown task structure
            lines = content.split('\n')
            task_title = ""
            instructions = []
            domains_needed = []
            found_instructions = False

            for line in lines:
                if line.startswith('# ') and not task_title:
                    task_title = line[2:].strip()  # Remove '# ' prefix
                elif line.startswith('## Instructions'):
                    found_instructions = True
                elif found_instructions and line.startswith('##'):
                    break  # End of instructions section
                elif found_instructions and line.strip():
                    instructions.append(line.strip())

                    # Check for domain indicators
                    line_lower = line.lower()
                    if any(domain in line_lower for domain in ['email', 'gmail', 'message', 'communication']):
                        if 'Communication' not in domains_needed:
                            domains_needed.append('Communication')
                    if any(domain in line_lower for domain in ['file', 'folder', 'directory', 'document', 'operations']):
                        if 'Operations' not in domains_needed:
                            domains_needed.append('Operations')
                    if any(domain in line_lower for domain in ['finance', 'account', 'track', 'report', 'audit', 'accounting']):
                        if 'Accounting/Tracking' not in domains_needed:
                            domains_needed.append('Accounting/Tracking')

            return {
                'title': task_title,
                'instructions': '\n'.join(instructions),
                'full_content': content,
                'domains_needed': domains_needed,
                'original_file': str(task_file_path)
            }
        except Exception as e:
            logger.error(f"Error reading task file '{task_file_path}': {str(e)}")
            return None

    def generate_multi_domain_plan(self, task_data: Dict) -> str:
        """Generate a multi-domain plan based on task requirements."""
        plan_content = f"# Multi-Domain Plan: {task_data['title']}\n\n"
        plan_content += f"Generated on: {datetime.now().isoformat()}\n\n"

        plan_content += "## Objective\n"
        plan_content += f"Complete the requested task: {task_data['title']}\n\n"

        plan_content += "## Domains Involved\n"
        if task_data['domains_needed']:
            for domain in task_data['domains_needed']:
                plan_content += f"- {domain}\n"
        else:
            plan_content += "- Operations (default)\n"
        plan_content += "\n"

        plan_content += "## Plan Steps\n"
        plan_content += "1. Analyze the requirements\n"
        plan_content += "2. Identify necessary resources across domains\n"
        plan_content += "3. Execute the planned actions in sequence\n"
        plan_content += "4. Verify completion of each step\n"
        plan_content += "5. Document results and outcomes\n\n"

        plan_content += "## Detailed Execution Steps\n"
        plan_content += "### Step 1: Requirement Analysis\n"
        plan_content += f"Analyze the original request: {task_data['title']}\n\n"

        plan_content += "### Step 2: Resource Identification\n"
        plan_content += "Identify required resources and capabilities for each domain involved.\n\n"

        plan_content += "### Step 3: Action Execution\n"
        plan_content += f"Execute the following actions based on instructions:\n{task_data['instructions']}\n\n"

        plan_content += "### Step 4: Verification\n"
        plan_content += "Verify that each step was completed successfully and meets the requirements.\n\n"

        plan_content += "### Step 5: Documentation\n"
        plan_content += "Document the results and update appropriate records.\n\n"

        plan_content += "## Expected Outcomes\n"
        plan_content += "- Task completed as specified\n"
        plan_content += "- All requirements satisfied\n"
        plan_content += "- Proper documentation maintained\n"
        plan_content += "- Cross-domain coordination verified\n\n"

        plan_content += "## Safety Checks\n"
        plan_content += "- All actions comply with policy\n"
        plan_content += "- Human approval required for sensitive actions\n"
        plan_content += "- No irreversible actions without verification\n\n"

        plan_content += "## Success Criteria\n"
        plan_content += "- Original task requirements fulfilled\n"
        plan_content += "- All domains properly coordinated\n"
        plan_content += "- Audit trail complete\n"

        return plan_content

    def process_task(self, task_file_path: Path) -> bool:
        """Process a single task file and generate a signed plan."""
        logger.info(f"Processing task: {task_file_path.name}")

        # Read the task
        task_data = self.read_task_file(task_file_path)
        if not task_data:
            logger.error(f"Failed to read task: {task_file_path.name}")
            return False

        # Apply policy checks
        if not self.policy_checker.check_task_policy(task_data):
            logger.warning(f"Policy violation in task: {task_file_path.name}")
            # Move to a quarantine area or handle appropriately
            return False

        # Generate multi-domain plan
        plan_content = self.generate_multi_domain_plan(task_data)

        # Sign the plan
        signed_plan_content = self.sign_plan(plan_content)

        # Create a plan filename based on original task name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"signed_plan_{timestamp}_{task_file_path.stem.replace(' ', '_').replace('/', '_')}.md"
        plan_path = self.signed_plans_dir / plan_filename

        # Write the signed plan
        try:
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(signed_plan_content)

            logger.info(f"Generated and signed plan: {plan_path.name}")

            # Move the original task to a processed folder to avoid reprocessing
            processed_dir = self.incoming_tasks_dir / "Processed"
            processed_dir.mkdir(exist_ok=True)
            processed_path = processed_dir / task_file_path.name
            shutil.move(str(task_file_path), str(processed_path))

            logger.info(f"Moved processed task {task_file_path.name} to Processed folder")
            return True

        except Exception as e:
            logger.error(f"Error writing signed plan: {str(e)}")
            return False

    def scan_and_process_tasks(self) -> int:
        """Scan for and process all pending tasks."""
        if not self.incoming_tasks_dir.exists():
            return 0

        task_files = [f for f in self.incoming_tasks_dir.iterdir()
                     if f.is_file() and f.name != "Processed"]
        processed_count = 0

        for task_file in task_files:
            # Skip if it's a directory
            if task_file.is_dir():
                continue

            if self.process_task(task_file):
                processed_count += 1

        return processed_count

    def run(self, scan_interval: int = 5):
        """Main run loop for the Cloud Planner Agent."""
        logger.info("Cloud Planner Agent started")
        logger.info(f"Monitoring: {self.incoming_tasks_dir}")
        logger.info(f"Output to: {self.signed_plans_dir}")

        try:
            while True:
                # Scan and process tasks
                processed_count = self.scan_and_process_tasks()

                if processed_count > 0:
                    logger.info(f"Processed {processed_count} tasks")

                # Wait before next scan
                time.sleep(scan_interval)

        except KeyboardInterrupt:
            logger.info("Cloud Planner Agent stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error in Cloud Planner Agent: {str(e)}")
            raise


class PolicyChecker:
    """Policy checker for the Cloud Planner Agent."""

    def __init__(self):
        # Define prohibited operations that the Cloud Agent should not plan
        self.prohibited_operations = [
            'execute file',
            'invoke mcp server',
            'modify local directory',
            'direct file execution',
            'run executable',
            'perform irreversible action',
            'bypass approval',
            'skip verification'
        ]

    def check_task_policy(self, task_data: Dict) -> bool:
        """Check if a task complies with Cloud Agent policies."""
        content_lower = task_data['full_content'].lower()

        # Check for prohibited operations
        for prohibited in self.prohibited_operations:
            if prohibited in content_lower:
                logger.warning(f"Policy violation: '{prohibited}' found in task content")
                return False

        # Additional policy checks can be added here
        return True


if __name__ == "__main__":
    agent = CloudPlannerAgent()
    print("Starting Cloud Planner Agent...")
    print("This agent will:")
    print("- Read tasks from Cloud/Incoming_Tasks")
    print("- Generate multi-domain plans")
    print("- Apply policy checks")
    print("- Produce signed plans in Cloud/Signed_Plans")
    print("- NEVER execute files or invoke MCP servers")
    print("\nPress Ctrl+C to stop")
    agent.run()