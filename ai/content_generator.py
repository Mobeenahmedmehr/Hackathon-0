import os
import logging
from typing import Dict, List
from config.config_loader import load_config_dict
from ai.news_fetcher import get_latest_ai_news


def generate_linkedin_post(news_data: List[Dict[str, str]]) -> str:
    """
    Generate LinkedIn post content using Qwen API.

    Args:
        news_data: List of dictionaries containing news data with keys: title, summary, source

    Returns:
        Generated LinkedIn post content
    """
    # Load configuration
    config = load_config_dict()

    # Prepare the prompt for the Qwen API
    news_titles = [item['title'] for item in news_data]
    news_summaries = [item['summary'] for item in news_data]

    # Construct the prompt
    prompt = f"""
    Generate an engaging LinkedIn post about the following AI news:
    News titles: {'; '.join(news_titles)}
    News summaries: {'; '.join(news_summaries)}

    The post should include:
    1. An engaging hook that draws attention
    2. A short explanation of the significance
    3. A valuable insight or takeaway
    4. A call to action

    Keep the tone professional but human-like, and the post concise (under 500 characters).
    """

    # For now, we'll return a mock response since we don't have the actual Qwen API setup
    # In a real implementation, you would call the Qwen API here
    sample_posts = [
        f"🚀 Just reviewed the latest in AI!\n\n{news_data[0]['title']}\n\n{news_data[0]['summary']}\n\nWhat are your thoughts on these developments?\n\n#AI #MachineLearning #Innovation",

        f" fascinating developments in AI this week:\n\n{news_data[0]['title']}\n\n{news_data[0]['summary']}\n\nThis represents a major step forward in the field.\n\nWhat's your perspective?\n\n#ArtificialIntelligence #TechNews #Future",

        f"🔥 Latest AI news that caught my attention:\n\n{news_data[0]['title']}\n\n{news_data[0]['summary']}\n\nExciting times ahead for the industry!\n\nWhat excites you most about these advancements?\n\n#AIDevelopment #Technology #Innovation"
    ]

    import random
    return random.choice(sample_posts)