import re
import logging
from logging_setup import get_logger

logger = get_logger(__name__)

def classify_task(task_text):
    """
    Classifies a task based on simple keyword heuristics.

    Args:
        task_text (str): Text content of the task to classify

    Returns:
        str: Classification category (email, sales_lead, linkedin_task, web_automation, research_task)
    """
    task_text_lower = task_text.lower()

    # Define keywords for each category
    email_keywords = [
        'email', 'mail', 'reply', 'response', 'send', 'draft', 'compose',
        'inbox', 'outbox', 'message', 'communication', 'correspondence'
    ]

    sales_keywords = [
        'lead', 'sale', 'customer', 'client', 'prospect', 'deal', 'opportunity',
        'contact', 'follow up', 'outreach', 'pitch', 'quote', 'proposal'
    ]

    linkedin_keywords = [
        'linkedin', 'connection', 'network', 'profile', 'post', 'comment',
        'endorse', 'message', 'invitation', 'inmail', 'connection request'
    ]

    web_automation_keywords = [
        'automate', 'browser', 'click', 'form', 'fill', 'scrape', 'extract',
        'navigate', 'website', 'webpage', 'automation', 'script'
    ]

    research_keywords = [
        'research', 'analyze', 'study', 'investigate', 'find', 'lookup',
        'information', 'data', 'statistics', 'report', 'summary', 'learn'
    ]

    # Count occurrences of keywords in each category
    email_score = sum(1 for keyword in email_keywords if keyword in task_text_lower)
    sales_score = sum(1 for keyword in sales_keywords if keyword in task_text_lower)
    linkedin_score = sum(1 for keyword in linkedin_keywords if keyword in task_text_lower)
    web_automation_score = sum(1 for keyword in web_automation_keywords if keyword in task_text_lower)
    research_score = sum(1 for keyword in research_keywords if keyword in task_text_lower)

    # Determine the highest scoring category
    scores = {
        'email': email_score,
        'sales_lead': sales_score,
        'linkedin_task': linkedin_score,
        'web_automation': web_automation_score,
        'research_task': research_score
    }

    # Return the category with the highest score
    # If there's a tie, return the first one in the order of priority
    max_score = max(scores.values())
    if max_score == 0:
        # If no keywords matched, default to a general category
        logger.info("No keywords matched, defaulting to research_task")
        return 'research_task'

    for category, score in scores.items():
        if score == max_score:
            logger.info(f"Classified task as {category} with score {score}")
            return category