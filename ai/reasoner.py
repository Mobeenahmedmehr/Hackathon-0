import os
from datetime import datetime
from pathlib import Path
import logging

from logging_setup import get_logger


class AIReasoner:
    """
    AI Reasoning module for generating structured plans.
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    def generate_plan(self, task_file_path: str) -> str:
        """
        Generate a structured plan based on a task file.

        Args:
            task_file_path: Path to the task file

        Returns:
            String content of the generated plan
        """
        logger = self.logger

        try:
            # Read the task content
            with open(task_file_path, 'r', encoding='utf-8') as f:
                task_content = f.read()

            # Extract task information for plan generation
            task_title = "Untitled Task"
            task_description = task_content

            # Look for a title in the task file
            lines = task_content.split('\n')
            for line in lines:
                if line.strip().startswith('# '):
                    task_title = line.strip()[2:]  # Remove '# ' prefix
                    break
                elif line.strip():
                    task_description = line.strip()
                    break

            # Generate a structured plan
            plan_content = self._create_structured_plan(task_title, task_description, task_content)

            logger.info(f"Generated plan for task: {task_file_path}")
            return plan_content

        except Exception as e:
            logger.error(f"Error generating plan for {task_file_path}: {str(e)}")
            # Return a default plan structure in case of error
            return self._create_default_plan(task_file_path)

    def _create_structured_plan(self, task_title: str, task_description: str, full_task: str) -> str:
        """
        Create a structured plan based on the task.
        """
        # Determine task type based on content
        task_type = self._determine_task_type(full_task)

        # Determine recommended agent based on task type
        recommended_agent = self._determine_agent(task_type)

        # Generate appropriate steps based on task
        steps = self._generate_steps(task_type, full_task)

        # Determine required tools
        tools_required = self._determine_tools(task_type)

        # Format the plan
        plan = f"""# Plan for: {task_title}

## Goal
{task_description}

## Task Type
{task_type}

## Recommended Agent
{recommended_agent}

## Tools Required
"""
        for tool in tools_required:
            plan += f"- {tool}\n"

        plan += "\n## Steps\n"
        for i, step in enumerate(steps, 1):
            plan += f"{i}. {step}\n"

        plan += f"\n## Approval Required
Yes

## Generated At
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return plan

    def _create_default_plan(self, task_file_path: str) -> str:
        """
        Create a default plan when generation fails.
        """
        return f"""# Plan for: {os.path.basename(task_file_path)}

## Goal
Process the provided task

## Task Type
General

## Recommended Agent
Default Agent

## Tools Required
- File System Access
- Logging

## Steps
1. Read the task content
2. Analyze requirements
3. Execute appropriate actions
4. Log results
5. Update status

## Approval Required
Yes

## Generated At
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    def _determine_task_type(self, task_content: str) -> str:
        """
        Determine the type of task based on its content.
        """
        content_lower = task_content.lower()

        if any(keyword in content_lower for keyword in ['email', 'gmail', 'message']):
            return 'Email Processing'
        elif any(keyword in content_lower for keyword in ['whatsapp', 'sms', 'text']):
            return 'Messaging'
        elif any(keyword in content_lower for keyword in ['linkedin', 'social', 'network']):
            return 'Social Media'
        elif any(keyword in content_lower for keyword in ['schedule', 'calendar', 'meeting']):
            return 'Scheduling'
        elif any(keyword in content_lower for keyword in ['document', 'write', 'draft']):
            return 'Content Creation'
        elif any(keyword in content_lower for keyword in ['data', 'analyze', 'report']):
            return 'Data Analysis'
        else:
            return 'General Task'

    def _determine_agent(self, task_type: str) -> str:
        """
        Determine the recommended agent based on task type.
        """
        agent_mapping = {
            'Email Processing': 'Email Agent',
            'Messaging': 'Communication Agent',
            'Social Media': 'Social Media Agent',
            'Scheduling': 'Calendar Agent',
            'Content Creation': 'Content Agent',
            'Data Analysis': 'Analytics Agent'
        }

        return agent_mapping.get(task_type, 'General Agent')

    def _generate_steps(self, task_type: str, task_content: str) -> list:
        """
        Generate appropriate steps based on task type.
        """
        base_steps = [
            "Analyze the task requirements",
            "Gather necessary information",
            "Execute the primary action",
            "Verify the results",
            "Prepare completion report"
        ]

        # Add task-type-specific steps
        if task_type == 'Email Processing':
            return [
                "Parse the email content",
                "Identify sender and context",
                "Determine appropriate response",
                "Draft response if needed",
                "Schedule sending or archive",
                "Update contact records"
            ] + base_steps

        elif task_type == 'Messaging':
            return [
                "Identify the messaging platform",
                "Extract message content and intent",
                "Validate sender identity",
                "Prepare appropriate response",
                "Send response through proper channel",
                "Log interaction"
            ] + base_steps

        elif task_type == 'Social Media':
            return [
                "Identify the social media platform",
                "Analyze post/content requirements",
                "Gather relevant information",
                "Create appropriate response or content",
                "Post or respond according to guidelines",
                "Track engagement metrics"
            ] + base_steps

        elif task_type == 'Content Creation':
            return [
                "Analyze content requirements",
                "Research necessary information",
                "Draft initial content",
                "Review and edit for quality",
                "Format for intended medium",
                "Submit for approval"
            ] + base_steps

        else:
            return base_steps

    def _determine_tools(self, task_type: str) -> list:
        """
        Determine tools required based on task type.
        """
        tool_mapping = {
            'Email Processing': ['Gmail API', 'Email Parser', 'Template Engine'],
            'Messaging': ['WhatsApp API', 'SMS Gateway', 'Message Formatter'],
            'Social Media': ['LinkedIn API', 'Social Media Manager', 'Content Scheduler'],
            'Scheduling': ['Calendar API', 'Time Zone Converter', 'Notification Service'],
            'Content Creation': ['Document Editor', 'Template Library', 'Style Checker'],
            'Data Analysis': ['Data Processor', 'Visualization Tools', 'Report Generator']
        }

        return tool_mapping.get(task_type, ['File System Access', 'Logging'])


# Global instance for backward compatibility
ai_reasoner = AIReasoner()


def generate_plan(task_file_path: str) -> str:
    """
    Standalone function to generate a plan.
    """
    return ai_reasoner.generate_plan(task_file_path)