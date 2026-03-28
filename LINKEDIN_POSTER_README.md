# Automated LinkedIn Content Posting System

This system automatically creates and posts LinkedIn content about the latest AI news. It's part of the AI Employee project that monitors various platforms and handles tasks autonomously.

## Components

### 1. `ai/news_fetcher.py`
- Fetches the latest AI news from various sources
- If no API is available, returns sample news data
- Returns news items with title, summary, and source

### 2. `ai/content_generator.py`
- Generates LinkedIn post content using the Qwen API
- Creates engaging hooks, explanations, insights, and calls to action
- Maintains a professional yet human-like tone

### 3. `ai/image_generator.py`
- Generates images for LinkedIn posts
- Creates placeholder images with text overlays using PIL
- Saves images to `assets/post_image.png`

### 4. `agents/linkedin_poster_agent.py`
- Posts content to LinkedIn using Playwright
- Loads saved LinkedIn sessions
- Simulates human behavior with random delays
- Handles text and image uploads

### 5. `core/content_scheduler.py`
- Automates the posting workflow
- Orchestrates fetching news, generating content, and posting
- Runs once per day

### 6. `tests/test_linkedin_posting.py`
- Tests the entire LinkedIn posting workflow
- Verifies each component works together

### 7. `watchers/linkedin_session.py`
- Manages LinkedIn session persistence
- Saves and loads cookies to maintain login state

## Setup

1. Install dependencies:
```bash
pip install -r requirements_linkedin.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

3. Set up environment variables in `.env`:
```env
QWEN_API_KEY=your_qwen_api_key
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
```

## Usage

Run the system once:
```bash
python run_linkedin_poster.py
```

Or schedule it to run daily:
```bash
python -c "from core.content_scheduler import schedule_daily_posts; schedule_daily_posts()"
```

## Features

- **Automated News Fetching**: Gets the latest AI news from various sources
- **AI-Powered Content Generation**: Creates engaging LinkedIn posts
- **Visual Content**: Generates custom images for each post
- **Human-like Behavior**: Random delays and varied posting times
- **Session Management**: Maintains LinkedIn login state
- **Logging**: Comprehensive logging for monitoring and debugging
- **Safety Measures**: Approval workflows and logging for all actions

## Safety & Compliance

- All posts are logged for auditing
- Human approval required for sensitive operations
- Rate limiting to avoid spam detection
- Secure credential handling via environment variables