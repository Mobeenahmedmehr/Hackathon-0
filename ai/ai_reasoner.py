"""
AI Reasoner Module for AI Employee System

This module handles the intelligence layer of the AI Employee.
It reads tasks from markdown files and generates structured plans using the Qwen API.
"""

import json
import os
import re
import time
from pathlib import Path
import requests
from config.config_loader import load_config
from config.paths import PLANS_DIR
from logging_setup import get_logger
from ai.task_classifier import classify_task
from ai.prompt_templates import TASK_ANALYSIS_PROMPT, PLAN_GENERATION_PROMPT


logger = get_logger("ai_reasoner")


def read_task_file(task_path):
    """
    Read a task markdown file and extract structured information.

    Args:
        task_path (str): Path to the markdown task file

    Returns:
        dict: Dictionary containing source, sender, timestamp, task description, raw message
    """
    try:
        with open(task_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Extract information using basic heuristics
        lines = content.split('\n')

        # Look for common fields in the markdown
        source = "unknown"
        sender = "unknown"
        timestamp = "unknown"
        task_description = ""
        raw_message = content

        for line in lines:
            if line.startswith('# Source:'):
                source = line.replace('# Source:', '').strip()
            elif line.startswith('# Sender:'):
                sender = line.replace('# Sender:', '').strip()
            elif line.startswith('# Timestamp:'):
                timestamp = line.replace('# Timestamp:', '').strip()

        # Extract task description (first paragraph after headers)
        in_description = False
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                if not task_description:
                    task_description = stripped_line
                break

        if not task_description:
            task_description = content[:500]  # Fallback to first 500 chars

        return {
            'source': source,
            'sender': sender,
            'timestamp': timestamp,
            'task_description': task_description,
            'raw_message': raw_message
        }
    except Exception as e:
        logger.error(f"Error reading task file {task_path}: {str(e)}")
        return {
            'source': 'unknown',
            'sender': 'unknown',
            'timestamp': 'unknown',
            'task_description': '',
            'raw_message': ''
        }


def build_ai_prompt(task_data):
    """
    Build a structured prompt for the Qwen API to analyze the task.

    Args:
        task_data (dict): Task data dictionary from read_task_file

    Returns:
        str: Structured prompt for the AI
    """
    prompt = PLAN_GENERATION_PROMPT.format(
        task_description=task_data['task_description'],
        raw_message=task_data['raw_message'],
        source=task_data['source'],
        sender=task_data['sender']
    )

    return prompt


def call_qwen_api(prompt):
    """
    Call the Qwen API with the given prompt.

    Args:
        prompt (str): Prompt to send to the Qwen API

    Returns:
        str: Response from the Qwen API
    """
    config = load_config()

    if not config.QWEN_API_KEY:
        raise ValueError("QWEN_API_KEY not found in configuration")

    headers = {
        "Authorization": f"Bearer {config.QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare the payload for the Qwen API
    # Note: Adjust the API endpoint and payload structure according to the actual Qwen API
    payload = {
        "model": "qwen-max",  # or whatever model is appropriate
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Qwen API (attempt {attempt + 1}/{max_retries})")

            response = requests.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()

                # Extract the content from the response
                # This may vary depending on the actual Qwen API response structure
                if 'output' in result and 'text' in result['output']:
                    return result['output']['text']
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    logger.warning(f"Unexpected response format: {result}")
                    return str(result)
            elif response.status_code == 429:
                logger.warning(f"Rate limited by Qwen API, waiting {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
            else:
                logger.error(f"Qwen API returned status code {response.status_code}: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    raise Exception(f"Qwen API request failed with status {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            logger.error(f"Qwen API request timed out (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise Exception("Qwen API request timed out after retries")
        except requests.exceptions.RequestException as e:
            logger.error(f"Qwen API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise Exception(f"Qwen API request failed after retries: {str(e)}")

    raise Exception("Max retries reached for Qwen API call")


def save_plan(task_id, plan_text):
    """
    Save the generated plan to the Plans directory.

    Args:
        task_id (str): Unique identifier for the task
        plan_text (str): Plan content to save

    Returns:
        str: Path to the saved plan file
    """
    # Sanitize the task_id to create a valid filename
    sanitized_task_id = re.sub(r'[^\w\-_]', '_', task_id)
    plan_filename = f"{sanitized_task_id}-plan.md"
    plan_path = PLANS_DIR / plan_filename

    try:
        with open(plan_path, 'w', encoding='utf-8') as file:
            file.write(plan_text)

        logger.info(f"Plan saved to {plan_path}")
        return str(plan_path)
    except Exception as e:
        logger.error(f"Error saving plan to {plan_path}: {str(e)}")
        raise


def generate_plan(task_path):
    """
    Full pipeline to generate a plan from a task file.

    Args:
        task_path (str): Path to the task markdown file

    Returns:
        str: Path to the generated plan file
    """
    logger.info(f"Starting plan generation for task: {task_path}")

    # Read the task file
    task_data = read_task_file(task_path)

    # Build the AI prompt
    prompt = build_ai_prompt(task_data)

    # Call the Qwen API
    plan_text = call_qwen_api(prompt)

    # Generate a task ID from the file path
    task_filename = Path(task_path).stem
    task_id = task_filename

    # Save the plan
    plan_path = save_plan(task_id, plan_text)

    logger.info(f"Plan generation completed. Saved to: {plan_path}")

    return plan_path