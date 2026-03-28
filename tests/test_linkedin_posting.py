import asyncio
import os
import sys
import pathlib

# Add the project root to the Python path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from ai.news_fetcher import get_latest_ai_news
from ai.content_generator import generate_linkedin_post
from ai.image_generator import generate_image_for_post
from agents.linkedin_poster_agent import post_linkedin_content


def test_linkedin_posting():
    """
    Test script to:
    1. Generate sample post
    2. Generate image
    3. Call LinkedIn poster
    """
    print("Starting LinkedIn posting test...")

    try:
        # 1. Generate sample post
        print("Fetching news...")
        news_data = get_latest_ai_news()
        print(f"Fetched {len(news_data)} news articles")

        print("Generating post content...")
        post_content = generate_linkedin_post(news_data)
        print("Generated post content (length: {})".format(len(post_content)))
        # Print without problematic characters
        safe_content = post_content.encode('ascii', errors='ignore').decode('ascii')
        print(safe_content[:200] + "..." if len(safe_content) > 200 else safe_content)

        # 2. Generate image
        print("Generating image...")
        news_title = news_data[0]['title']
        image_path = "assets/test_post_image.png"
        generate_image_for_post(news_title, image_path)
        print(f"Generated image at {image_path}")

        # 3. Call LinkedIn poster (only if in testing mode)
        print("Testing LinkedIn poster function...")

        # For testing purposes, we'll just print what would happen
        print("Would call post_linkedin_content with:")
        safe_post_content = post_content.encode('ascii', errors='ignore').decode('ascii')
        print(f"  Text: {safe_post_content[:100]}...")
        print(f"  Image: {image_path}")

        # Uncomment the following lines to actually post (requires valid session)
        # asyncio.run(post_linkedin_content(post_content, image_path))

        print("Test completed successfully!")

    except Exception as e:
        print(f"Error in test: {str(e)}")
        raise


if __name__ == "__main__":
    test_linkedin_posting()