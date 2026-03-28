import random
from datetime import datetime
from typing import Dict, List


def get_latest_ai_news() -> List[Dict[str, str]]:
    """
    Fetch latest AI news. If no API is available, return sample news.

    Returns:
        List of dictionaries containing news data with keys: title, summary, source
    """
    # Sample AI news data - in a real implementation, this would fetch from an API
    sample_news = [
        {
            "title": "OpenAI releases new GPT model with improved reasoning",
            "summary": "The latest iteration of GPT shows significant improvements in logical reasoning and problem-solving capabilities.",
            "source": "OpenAI Blog"
        },
        {
            "title": "Anthropic introduces Constitutional AI 2.0",
            "summary": "Enhanced alignment techniques promise safer and more reliable AI systems for enterprise deployment.",
            "source": "Anthropic Research"
        },
        {
            "title": "Google DeepMind unveils breakthrough in protein folding prediction",
            "summary": "New AI model achieves unprecedented accuracy in predicting protein structures, accelerating drug discovery.",
            "source": "Nature Journal"
        },
        {
            "title": "Microsoft announces Azure OpenAI Service enhancements",
            "summary": "New features include improved security controls and enhanced integration with Microsoft 365 suite.",
            "source": "Microsoft Tech Blog"
        },
        {
            "title": "Stability AI releases new text-to-video model",
            "summary": "The model generates high-quality videos from text prompts, opening new possibilities for content creation.",
            "source": "TechCrunch"
        }
    ]

    # Randomly select 1-3 news items to return
    num_articles = random.randint(1, min(3, len(sample_news)))
    selected_news = random.sample(sample_news, num_articles)

    return selected_news