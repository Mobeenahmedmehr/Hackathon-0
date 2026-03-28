import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright


async def load_linkedin_session():
    """
    Load saved LinkedIn session using Playwright.

    Returns:
        Page object if successful, None otherwise
    """
    try:
        # Initialize Playwright
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)  # Set to True for production
        context = await browser.new_context()

        # Path to save/load cookies
        cookies_file = Path("sessions/linkedin_cookies.json")

        # Create sessions directory if it doesn't exist
        cookies_file.parent.mkdir(parents=True, exist_ok=True)

        # Load cookies if they exist
        if cookies_file.exists():
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print("Loaded LinkedIn session from cookies")
        else:
            print("No saved session found, please log in to LinkedIn manually")

        # Create a new page
        page = await context.new_page()

        # Navigate to LinkedIn to verify the session
        await page.goto("https://www.linkedin.com/feed/")
        await page.wait_for_load_state("networkidle")

        # Check if we're still logged in by looking for elements that appear when logged in
        try:
            # Look for elements that indicate a successful login
            await page.wait_for_selector("img[alt='Me']", timeout=5000)
            print("Verified LinkedIn login session")
        except:
            print("Session may have expired or not logged in. Please log in manually.")
            # Navigate to login page
            await page.goto("https://www.linkedin.com/login")

        return page

    except Exception as e:
        print(f"Error loading LinkedIn session: {str(e)}")
        return None


async def save_linkedin_session(page):
    """
    Save the current LinkedIn session cookies to file.

    Args:
        page: Playwright page object with active LinkedIn session
    """
    try:
        # Get the context from the page
        context = page.context

        # Get cookies for LinkedIn
        cookies = await context.cookies("https://www.linkedin.com")

        # Save cookies to file
        cookies_file = Path("sessions/linkedin_cookies.json")
        cookies_file.parent.mkdir(parents=True, exist_ok=True)

        with open(cookies_file, 'w') as f:
            json.dump(cookies, f, indent=2)

        print(f"Saved LinkedIn session to {cookies_file}")

    except Exception as e:
        print(f"Error saving LinkedIn session: {str(e)}")


if __name__ == "__main__":
    async def main():
        page = await load_linkedin_session()
        if page:
            print("Successfully loaded LinkedIn session")
            # Optionally save the session after performing actions
            # await save_linkedin_session(page)

            # Close the page and browser when done
            try:
                await page.context.browser.close()
            except AttributeError:
                print("Could not close browser - page context not available")
        else:
            print("Failed to load LinkedIn session")

    asyncio.run(main())