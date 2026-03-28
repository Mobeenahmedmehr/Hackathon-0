import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def save_task_as_markdown(sender, message_text, timestamp, message_id=None):
    """
    Save the LinkedIn message as a markdown task file in the Needs_Action directory.
    """
    # Create the Needs_Action directory if it doesn't exist
    needs_action_dir = Path("Needs_Action")
    needs_action_dir.mkdir(exist_ok=True)

    # Create a filename with timestamp
    if message_id:
        filename = f"linkedin_{message_id}_{int(timestamp.timestamp())}.md"
    else:
        filename = f"linkedin_{int(timestamp.timestamp())}.md"

    filepath = needs_action_dir / filename

    # Format the markdown content
    markdown_content = f"""# Task
Source: LinkedIn
Sender: {sender}
Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Message: {message_text}
"""

    # Write the content to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    logger.info(f"Saved LinkedIn message from {sender} to {filepath}")


async def load_linkedin_session():
    """
    Loads an existing LinkedIn session from file and returns a page object.
    """
    session_file = Path("sessions") / "linkedin_session.json"

    # Check if session file exists
    if not session_file.exists():
        logger.error(f"No session file found at {session_file}")
        logger.error("Please run the login script first to create a session.")
        return None

    try:
        async with async_playwright() as p:
            # Load the saved session data
            with open(session_file, 'r') as f:
                storage_state = json.load(f)

            # Launch browser with saved storage state
            browser = await p.chromium.launch(headless=False)  # Set to False so it's visible
            context = await browser.new_context(storage_state=storage_state)

            # Create a new page
            page = await context.new_page()

            # Navigate to LinkedIn to verify the session is valid
            await page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded')

            # Verify if still logged in by checking for logged-in elements
            try:
                # Wait for elements that appear only when logged in
                await page.wait_for_selector(
                    'div.global-nav__me-menu-trigger, img.global-nav__profile-img, button[data-test-id="profile-nav-item"]',
                    timeout=10000
                )
                logger.info("Successfully loaded LinkedIn session. You are logged in.")
                return browser, context, page
            except Exception as e:
                logger.error(f"Session may have expired or is invalid: {str(e)}")
                await browser.close()
                return None

    except Exception as e:
        logger.error(f"Error loading LinkedIn session: {str(e)}")
        return None


async def check_linkedin_messages(page):
    """
    Check LinkedIn for new/unread messages and return them.
    """
    try:
        # Navigate to the LinkedIn messaging page
        await page.goto('https://www.linkedin.com/messaging/', wait_until='domcontentloaded')

        # Wait for the messaging page to load
        await page.wait_for_selector('div.msg-overlay-conversation-bubble', timeout=10000)

        # Find unread/conversations with new messages
        # Look for conversation items that might have unread indicators
        conversation_elements = await page.query_selector_all('li.msg-conversation-listitem')

        new_messages = []

        for element in conversation_elements:
            try:
                # Check if the conversation has unread messages
                unread_indicator = await element.query_selector('.msg-conversation-listitem__unread-count')

                if unread_indicator:
                    # Extract sender name
                    sender_element = await element.query_selector('.msg-conversation-listitem__participant-names')
                    sender = await sender_element.text_content() if sender_element else "Unknown"

                    # Click on the conversation to view messages
                    await element.click()

                    # Wait for messages to load
                    await page.wait_for_selector('.msg-s-event-listitem', timeout=5000)

                    # Get all message elements in the conversation
                    message_elements = await page.query_selector_all('.msg-s-event-listitem')

                    for msg_element in message_elements:
                        # Check if the message is from the other person (not the current user)
                        is_from_user = await msg_element.get_attribute('data-from-actor-id')

                        # Get message text
                        message_text_element = await msg_element.query_selector('.msg-s-event__body')
                        if message_text_element:
                            message_text = await message_text_element.text_content()

                            # Get timestamp
                            timestamp_element = await msg_element.query_selector('.msg-s-event__created-time')
                            timestamp_str = await timestamp_element.text_content() if timestamp_element else ""
                            timestamp = datetime.now()  # Fallback to current time if parsing fails

                            new_messages.append({
                                'sender': sender.strip(),
                                'message': message_text.strip(),
                                'timestamp': timestamp,
                                'timestamp_str': timestamp_str
                            })

                    # Go back to the conversations list
                    await page.goto('https://www.linkedin.com/messaging/', wait_until='domcontentloaded')
                    await page.wait_for_selector('li.msg-conversation-listitem', timeout=5000)

            except Exception as e:
                logger.warning(f"Error processing conversation: {str(e)}")
                continue

        # Alternative approach: check for the notification badge on the main messaging icon
        try:
            messaging_icon = await page.query_selector('a[data-test-global-typeahead-keyboard-search-input]')
            if messaging_icon:
                # Navigate to the main messaging page
                await page.goto('https://www.linkedin.com/mynetwork/')

                # Find and click the messaging nav item
                messaging_nav_item = await page.query_selector('a[href="/messaging/"]')
                if messaging_nav_item:
                    await messaging_nav_item.click()

                    # Wait for page to load
                    await page.wait_for_selector('[data-view-name="messaging-thread"]', timeout=5000)

                    # Look for unread messages
                    unread_messages = await page.query_selector_all('[data-test-is-unread="true"]')

                    for msg in unread_messages:
                        # Extract message details
                        sender_elem = await msg.query_selector('.msg-conversation-card__participant-names')
                        sender = await sender_elem.text_content() if sender_elem else "Unknown"

                        message_elem = await msg.query_selector('.msg-conversation-card__last-snippet')
                        message_text = await message_elem.text_content() if message_elem else "No message content"

                        new_messages.append({
                            'sender': sender.strip(),
                            'message': message_text.strip(),
                            'timestamp': datetime.now(),
                            'timestamp_str': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })

        except Exception as e:
            logger.debug(f"Alternative message checking failed: {str(e)}")

        return new_messages

    except Exception as e:
        logger.error(f"Error checking LinkedIn messages: {str(e)}")
        return []


async def linkedin_watcher():
    """
    Main LinkedIn watcher loop that checks for new messages every 60 seconds.
    """
    logger.info("Starting LinkedIn watcher...")

    # Load LinkedIn session
    result = await load_linkedin_session()

    if not result:
        logger.error("Failed to load LinkedIn session. Exiting.")
        return

    browser, context, page = result

    # Keep track of processed messages to avoid duplicates
    processed_message_ids = set()

    try:
        while True:
            logger.info("Checking LinkedIn for new messages...")

            # Check for new messages
            new_messages = await check_linkedin_messages(page)

            # Process new messages
            for message in new_messages:
                # Create a unique identifier for the message to prevent duplicates
                message_id = f"{message['sender']}_{message['timestamp'].timestamp()}_{len(message['message'])}"

                if message_id not in processed_message_ids:
                    # Save the message as a markdown task
                    save_task_as_markdown(
                        sender=message['sender'],
                        message_text=message['message'],
                        timestamp=message['timestamp']
                    )

                    # Add to processed set
                    processed_message_ids.add(message_id)

                    logger.info(f"New message from {message['sender']}: {message['message'][:50]}...")

            if new_messages:
                logger.info(f"Processed {len(new_messages)} new messages")
            else:
                logger.info("No new messages found")

            # Wait for 60 seconds before next check
            logger.info("Waiting 60 seconds before next check...")
            await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("LinkedIn watcher stopped by user")
    except Exception as e:
        logger.error(f"Error in LinkedIn watcher: {str(e)}")
    finally:
        # Close the browser when done
        await browser.close()
        logger.info("Browser closed")


if __name__ == "__main__":
    asyncio.run(linkedin_watcher())