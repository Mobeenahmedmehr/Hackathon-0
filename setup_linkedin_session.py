#!/usr/bin/env python3
"""
Script to manually set up LinkedIn session for the AI Employee system.
This script will open a browser where you can log in to LinkedIn manually.
After logging in, the session will be saved for future use.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from Watchers.linkedin_session import load_linkedin_session, save_linkedin_session

async def setup_linkedin_session_manually():
    """
    Manually set up LinkedIn session by logging in through browser
    """
    print("="*60)
    print("LINKEDIN SESSION SETUP")
    print("="*60)
    print("\nThis script will help you set up your LinkedIn session.")
    print("A browser window will open shortly.")
    print("\nPlease follow these steps:")
    print("1. Log in to your LinkedIn account in the browser")
    print("2. Navigate to your feed to ensure you're logged in")
    print("3. Come back to this terminal and press Enter when done")
    print("\nIMPORTANT: Use a dedicated account for automation, not your personal account.")
    print("="*60)

    print("\nOpening LinkedIn in browser...")
    page = await load_linkedin_session()

    if page:
        print("\nBrowser opened. Please log in to LinkedIn now.")
        print("After logging in, press Enter in this terminal when you're done.")
        input("Press Enter when you have successfully logged in: ")

        # Save the session cookies after successful login
        await save_linkedin_session(page)

        print("\n✅ Session saved successfully!")
        print("The session will be used by the LinkedIn poster system.")
        print("\nYou can now run the test script to verify everything works:")
        print("python tests/test_linkedin_posting.py")

        # Close the browser
        try:
            await page.context.browser.close()
        except:
            pass
    else:
        print("❌ Could not initialize browser session")
        print("Make sure you have installed Playwright browsers:")
        print("playwright install chromium")

if __name__ == "__main__":
    print("Setting up LinkedIn session...")
    asyncio.run(setup_linkedin_session_manually())