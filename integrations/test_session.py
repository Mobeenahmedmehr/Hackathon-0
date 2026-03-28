import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright


async def load_linkedin_session():
    """
    Loads an existing LinkedIn session from file.
    """
    session_file = Path("sessions") / "linkedin_session.json"

    if not session_file.exists():
        print("No existing session found. Please run login_to_linkedin() first.")
        return None

    async with async_playwright() as p:
        # Load the saved session
        with open(session_file, 'r') as f:
            storage_state = json.load(f)

        # Launch browser with saved storage state
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=storage_state)

        # Create a new page
        page = await context.new_page()

        # Navigate to LinkedIn home to verify session
        await page.goto('https://www.linkedin.com/feed/')

        # Verify if still logged in by navigating to the profile page
        await page.goto('https://www.linkedin.com/in/')

        try:
            # Wait for elements that appear after login
            await page.wait_for_selector('div.global-nav__me-menu-trigger', timeout=10000)
            print("Successfully loaded existing LinkedIn session!")
            print("You should now be logged into LinkedIn automatically.")

            # Keep the browser open briefly so you can verify
            await page.wait_for_timeout(5000)
            return browser, context, page
        except:
            print("Session may have expired. Please log in again using the main script.")
            await browser.close()
            return None


if __name__ == "__main__":
    # Run the session loading function
    asyncio.run(load_linkedin_session())