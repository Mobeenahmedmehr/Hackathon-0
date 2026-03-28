import asyncio
import logging
import random
from pathlib import Path
from playwright.async_api import async_playwright


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def post_linkedin_content(text: str, image_path: str):
    """
    Post content to LinkedIn using Playwright.

    Args:
        text: The text content to post
        image_path: Path to the image to upload
    """
    # Import the session loader
    from Watchers.linkedin_session import load_linkedin_session

    # Load the saved LinkedIn session
    result = await load_linkedin_session()
    if not result:
        logger.error("Failed to load LinkedIn session")
        return False

    page = result

    try:
        # Navigate to LinkedIn homepage
        await page.goto('https://www.linkedin.com/feed/')
        logger.info("Navigated to LinkedIn homepage")

        # Wait a random amount of time to simulate human behavior
        await asyncio.sleep(random.uniform(1, 3))

        # Click the "Start a post" button
        # This selector may vary depending on LinkedIn's UI, but this is a common one
        post_button = await page.wait_for_selector(
            'button[aria-label="Start a post"]',
            timeout=10000
        )
        await post_button.click()
        logger.info("Clicked 'Start a post' button")

        # Wait a moment before typing
        await asyncio.sleep(random.uniform(1, 2))

        # Type the text content into the post editor
        text_editor = await page.wait_for_selector(
            'div[contenteditable="true"][data-test-id="artdeco-content-editable"]',
            timeout=10000
        )
        await text_editor.fill(text)
        logger.info("Filled post text content")

        # Wait before uploading image
        await asyncio.sleep(random.uniform(2, 4))

        # Upload the image
        # Click the image upload button
        image_upload_button = await page.wait_for_selector(
            'button[aria-label="Add a photo/image"]',
            timeout=10000
        )
        await image_upload_button.click()
        logger.info("Clicked image upload button")

        # Wait for the file input to appear
        await asyncio.sleep(random.uniform(1, 2))

        # Handle file upload
        file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
        await file_input.set_input_files(image_path)
        logger.info(f"Selected image: {image_path}")

        # Wait for the image to upload
        await asyncio.sleep(random.uniform(3, 5))

        # Wait before clicking post
        await asyncio.sleep(random.uniform(2, 4))

        # Click the post button
        post_submit_button = await page.wait_for_selector(
            'button[aria-label="Post"]',
            timeout=10000
        )
        await post_submit_button.click()
        logger.info("Clicked 'Post' button")

        # Wait for the post to be submitted
        await asyncio.sleep(random.uniform(3, 5))

        logger.info("Content successfully posted to LinkedIn")
        return True

    except Exception as e:
        logger.error(f"Error posting to LinkedIn: {str(e)}")
        return False

    finally:
        # Close the browser
        await page.context.browser.close()