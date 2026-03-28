import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright


async def load_linkedin_session():
    """
    Loads an existing LinkedIn session from file and returns a page object.

    Returns:
        Page object if successful, None if failed
    """
    session_file = Path("sessions") / "linkedin_session.json"

    # Check if session file exists
    if not session_file.exists():
        print(f"No session file found at {session_file}")
        print("Please run the login script first to create a session.")
        return None

    try:
        async with async_playwright() as p:
            # Load the saved session data
            with open(session_file, 'r') as f:
                storage_state = json.load(f)

            # Launch browser with saved storage state
            browser = await p.chromium.launch(headless=False)
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
                print("Successfully loaded LinkedIn session. You are logged in.")

                # Return only the page object as requested
                return page
            except Exception as e:
                print(f"Session may have expired or is invalid: {str(e)}")
                await browser.close()
                return None

    except Exception as e:
        print(f"Error loading LinkedIn session: {str(e)}")
        return None


if __name__ == "__main__":
    # Example usage
    async def main():
        page = await load_linkedin_session()

        if page:
            browser = page.context.browser
            # Example: Navigate to a LinkedIn page
            await page.goto('https://www.linkedin.com/mynetwork/')

            print("Page is loaded with LinkedIn session. Press Enter to close...")
            input()
            await browser.close()
        else:
            print("Failed to load LinkedIn session")

    asyncio.run(main())