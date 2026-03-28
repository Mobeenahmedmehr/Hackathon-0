import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright


async def login_to_linkedin():
    """
    Asynchronously logs into LinkedIn using Playwright.
    Prompts user for manual login and saves the session for future use.
    """
    # Create sessions directory if it doesn't exist
    sessions_dir = Path("sessions")
    sessions_dir.mkdir(exist_ok=True)

    session_file = sessions_dir / "linkedin_session.json"

    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)  # headless=False to allow manual login
        context = await browser.new_context()

        # Create a new page
        page = await context.new_page()

        # Navigate to LinkedIn login page
        await page.goto('https://www.linkedin.com/login')

        print("LinkedIn login page opened. Please enter your credentials and log in manually.")
        print("After successful login, please close this browser window to continue...")

        # Wait for user to complete login manually
        print("Waiting for manual login. Please complete the login process in the browser...")

        # Wait for navigation to the homepage or other post-login pages
        try:
            # Wait up to 2 minutes for the user to log in
            await page.wait_for_url('https://www.linkedin.com/feed/**', timeout=120000)
            print("Detected successful login! Saving session...")
        except:
            # If the URL didn't change, check for presence of elements that indicate login
            try:
                await page.wait_for_selector('div.global-nav__me-menu-trigger', timeout=5000)
                print("Login detected! Saving session...")
            except:
                print("Could not verify login status. Please ensure you are logged in, then we'll save the session anyway...")

        # Check if user is logged in by checking for presence of logout button or profile icon
        try:
            # Wait for either the profile dropdown or homepage elements to confirm login
            await page.wait_for_selector('div.global-nav__me-menu-trigger', timeout=10000)
            print("Login appears to be successful!")
        except:
            try:
                # Alternative selector for logged-in state
                await page.wait_for_selector('img[alt*="Profile photo"]', timeout=10000)
                print("Login appears to be successful!")
            except:
                print("Warning: Could not verify login status. Proceeding anyway...")

        # Save session cookies and storage state
        storage_state = await context.storage_state()

        # Write session data to file
        with open(session_file, 'w') as f:
            json.dump(storage_state, f, indent=2)

        print(f"Session saved to {session_file}")

        # Close the browser
        await browser.close()


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

        # Verify if still logged in
        try:
            await page.wait_for_selector('div.global-nav__me-menu-trigger', timeout=10000)
            print("Successfully loaded existing LinkedIn session!")
            return browser, context, page
        except:
            print("Session may have expired. Please log in again.")
            await browser.close()
            return None


if __name__ == "__main__":
    # Run the login function
    asyncio.run(login_to_linkedin())