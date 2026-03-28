"""
WhatsApp watcher for monitoring WhatsApp messages and converting them to tasks.
"""

import os
import time
import threading
from datetime import datetime
from pathlib import Path

try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from logging_setup import get_logger

# Import config_loader if available, otherwise use basic config
try:
    from config.config_loader import load_config
except ImportError:
    def load_config():
        return {}


class WhatsAppWatcher:
    """
    Watches WhatsApp for new messages and converts them into task files.
    """

    def __init__(self):
        self.logger = get_logger("watcher.whatsapp")
        self.driver = None
        self.is_running = False

    def start_whatsapp_session(self):
        """
        Open WhatsApp Web using browser automation and maintain login session.
        """
        try:
            if not SELENIUM_AVAILABLE:
                self.logger.error("Selenium is not available. Please install selenium.")
                return False

            # Setup Chrome driver with options
            options = webdriver.ChromeOptions()
            options.add_argument("--user-data-dir=./chrome_profile")  # Persist session
            options.add_argument("--profile-directory=Default")

            self.driver = webdriver.Chrome(options=options)
            self.driver.get("https://web.whatsapp.com/")

            self.logger.info("WhatsApp Web opened. Please scan QR code if not logged in.")

            # Wait for user to log in (wait for chat list to appear)
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list']"))
                )
                self.logger.info("Successfully logged into WhatsApp Web")
                return True
            except:
                self.logger.error("Failed to log into WhatsApp Web within 60 seconds")
                return False

        except Exception as e:
            self.logger.error(f"Error starting WhatsApp session: {str(e)}")
            return False

    def fetch_new_messages(self):
        """
        Detect new unread chats and extract message information.

        Returns:
            list: List of messages with sender, text, and timestamp
        """
        if not self.driver:
            self.logger.error("No WhatsApp session available")
            return []

        try:
            messages = []

            # Find all unread chat elements
            unread_chats = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'unread')]//../..")

            for chat in unread_chats:
                try:
                    # Get sender name
                    sender_element = chat.find_element(By.XPATH, ".//span[@dir='auto']")
                    sender_name = sender_element.text

                    # Get last message text
                    message_element = chat.find_element(By.XPATH, ".//span[@class='_11JPr selectable-text copyable-text']")
                    message_text = message_element.text

                    # Get timestamp
                    timestamp_element = chat.find_element(By.XPATH, ".//span[@class='_2f-RV']")
                    timestamp = timestamp_element.get_attribute("title") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Mark as read by clicking on the chat
                    chat.click()

                    messages.append({
                        'sender_name': sender_name,
                        'message_text': message_text,
                        'timestamp': timestamp
                    })

                except Exception as e:
                    self.logger.warning(f"Could not process chat element: {str(e)}")
                    continue

            return messages

        except Exception as e:
            self.logger.error(f"Error fetching messages: {str(e)}")
            return []

    def convert_message_to_task(self, message):
        """
        Convert a WhatsApp message into a markdown task file.

        Args:
            message (dict): Message with sender_name, message_text, timestamp
        """
        try:
            # Ensure Needs_Action directory exists
            needs_action_dir = Path("Needs_Action")
            needs_action_dir.mkdir(exist_ok=True)

            # Create task content
            task_content = f"""# Task

**Source:** WhatsApp
**Sender:** {message['sender_name']}
**Timestamp:** {message['timestamp']}

## Message:
{message['message_text']}

---
Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

            # Generate filename with timestamp
            timestamp_safe = message['timestamp'].replace(':', '-').replace(' ', '_').replace('/', '-')
            filename = f"whatsapp_{timestamp_safe}_{message['sender_name'][:20].replace(' ', '_')}.md"
            filepath = needs_action_dir / filename

            # Write task file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(task_content)

            self.logger.info(f"WhatsApp task created: {filepath}")

            return str(filepath)

        except Exception as e:
            self.logger.error(f"Error converting message to task: {str(e)}")
            return None

    def run_whatsapp_watcher(self):
        """
        Continuously check for new messages every 60 seconds.
        """
        if not self.start_whatsapp_session():
            self.logger.error("Could not start WhatsApp session, exiting watcher")
            return

        self.is_running = True

        while self.is_running:
            try:
                messages = self.fetch_new_messages()

                for message in messages:
                    self.convert_message_to_task(message)

                if messages:
                    self.logger.info(f"Processed {len(messages)} new WhatsApp messages")

                # Wait for 60 seconds before checking again
                time.sleep(60)

            except KeyboardInterrupt:
                self.logger.info("WhatsApp watcher interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"Error in WhatsApp watcher loop: {str(e)}")
                time.sleep(60)  # Wait before retrying

        # Cleanup
        if self.driver:
            self.driver.quit()

    def stop_watcher(self):
        """
        Stop the watcher and cleanup resources.
        """
        self.is_running = False
        if self.driver:
            self.driver.quit()


def main():
    """
    Main function to run the WhatsApp watcher.
    """
    watcher = WhatsAppWatcher()
    try:
        watcher.run_whatsapp_watcher()
    except KeyboardInterrupt:
        print("Stopping WhatsApp watcher...")
        watcher.stop_watcher()


if __name__ == "__main__":
    main()