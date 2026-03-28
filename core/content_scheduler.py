import asyncio
import logging
from datetime import datetime
from ai.news_fetcher import get_latest_ai_news
from ai.content_generator import generate_linkedin_post
from ai.image_generator import generate_image_for_post
from agents.linkedin_poster_agent import post_linkedin_content


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def run_daily_post():
    """
    Automate posting by running the full workflow:
    1. Fetch news
    2. Generate post
    3. Generate image
    4. Send to LinkedIn agent
    """
    logger.info("Starting daily LinkedIn post workflow")

    try:
        # 1. Fetch latest AI news
        logger.info("Fetching latest AI news...")
        news_data = get_latest_ai_news()
        logger.info(f"Fetched {len(news_data)} news articles")

        if not news_data:
            logger.warning("No news articles fetched, skipping post")
            return

        # 2. Generate LinkedIn post content
        logger.info("Generating LinkedIn post content...")
        post_content = generate_linkedin_post(news_data)
        logger.info("Generated LinkedIn post content")

        # 3. Generate image for the post
        logger.info("Generating image for the post...")
        news_title = news_data[0]['title']  # Use the first article's title
        image_path = "assets/post_image.png"
        generate_image_for_post(news_title, image_path)
        logger.info(f"Generated image at {image_path}")

        # 4. Post to LinkedIn
        logger.info("Posting content to LinkedIn...")
        success = await post_linkedin_content(post_content, image_path)

        if success:
            logger.info("Successfully posted to LinkedIn!")
        else:
            logger.error("Failed to post to LinkedIn")

    except Exception as e:
        logger.error(f"Error in daily post workflow: {str(e)}")
        raise


def main():
    """
    Main function to run the daily post scheduler
    """
    # For now, run once
    asyncio.run(run_daily_post())


if __name__ == "__main__":
    main()