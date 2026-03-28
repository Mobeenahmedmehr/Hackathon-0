"""
Channel manager for running multiple watchers simultaneously.
"""

import threading
import time
from pathlib import Path

# Import the watchers
from watchers.gmail_watcher import run_watcher_loop as run_gmail_watcher
from watchers.whatsapp_watcher import WhatsAppWatcher
from watchers.linkedin_watcher import LinkedInWatcher

from logging_setup import get_logger


class ChannelManager:
    """
    Manages multiple watchers simultaneously using threading.
    """

    def __init__(self):
        self.logger = get_logger("channel.manager")
        self.watchers = []
        self.threads = []
        self.running = False

    def start_all_watchers(self):
        """
        Start all watchers in separate threads.
        This runs:
        - gmail_watcher
        - whatsapp_watcher
        - linkedin_watcher
        """
        self.logger.info("Starting all watchers...")

        # Initialize watchers
        try:
            whatsapp_watcher = WhatsAppWatcher()
            linkedin_watcher = LinkedInWatcher()

            self.watchers = [
                ('Gmail', run_gmail_watcher),
                ('WhatsApp', whatsapp_watcher),
                ('LinkedIn', linkedin_watcher)
            ]

            # Create and start threads for each watcher
            for name, watcher in self.watchers:
                if name == 'Gmail':
                    # Gmail watcher is a function, not a class instance
                    thread = threading.Thread(
                        target=watcher,  # Just the function
                        name=f"{name}WatcherThread"
                    )
                else:
                    # Other watchers are class instances with methods
                    thread = threading.Thread(
                        target=self._run_watcher,
                        args=(name, watcher),
                        name=f"{name}WatcherThread"
                    )

                self.threads.append(thread)
                thread.daemon = True  # Dies when main thread dies
                thread.start()
                self.logger.info(f"Started {name} watcher thread")

            self.running = True

            # Keep the main thread alive
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Received interrupt signal, stopping all watchers...")
                self.stop_all_watchers()

        except Exception as e:
            self.logger.error(f"Error starting watchers: {str(e)}")

    def _run_watcher(self, name, watcher):
        """
        Internal method to run a specific watcher.

        Args:
            name (str): Name of the watcher
            watcher: Watcher instance
        """
        try:
            if name == 'WhatsApp':
                watcher.run_whatsapp_watcher()
            elif name == 'LinkedIn':
                watcher.run_linkedin_watcher()
            else:
                self.logger.error(f"Unknown watcher type: {name}")
        except Exception as e:
            self.logger.error(f"Error running {name} watcher: {str(e)}")

    def stop_all_watchers(self):
        """
        Stop all running watchers.
        """
        self.logger.info("Stopping all watchers...")
        self.running = False

        # Give threads a chance to stop gracefully
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)  # Wait up to 5 seconds for each thread

        self.logger.info("All watchers stopped")


def main():
    """
    Main function to run the channel manager.
    """
    manager = ChannelManager()
    manager.start_all_watchers()


if __name__ == "__main__":
    main()