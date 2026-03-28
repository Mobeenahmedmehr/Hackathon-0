#!/usr/bin/env python3
"""
Main script to run the automated LinkedIn content posting system.
"""

import asyncio
import logging
from core.content_scheduler import run_daily_post

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main function to run the LinkedIn content posting system."""
    logger.info("Starting automated LinkedIn content posting system...")

    # Run the daily post workflow
    success = asyncio.run(run_daily_post())

    if success:
        logger.info("LinkedIn content posting completed successfully!")
    else:
        logger.error("LinkedIn content posting failed!")


if __name__ == "__main__":
    main()