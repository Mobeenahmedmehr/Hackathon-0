#!/bin/bash

# Initial setup script for AI Employee system

echo "Setting up AI Employee system..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Create required folders if they don't exist
echo "Creating required folders..."
mkdir -p Needs_Action Plans Pending_Approval Approved Done Drafts Logs Reports
mkdir -p Watchers ai core config mcp_servers security auditor dashboard

# Verify environment variables
echo "Checking environment variables..."
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create one based on .env.example"
else
    echo "Environment file found"
    # Source the environment file to check if required variables are set
    set -a
    source .env
    set +a

    # Check for common required environment variables
    if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        echo "Warning: GOOGLE_APPLICATION_CREDENTIALS not set in .env"
    fi

    if [ -z "$GMAIL_CLIENT_ID" ]; then
        echo "Warning: GMAIL_CLIENT_ID not set in .env"
    fi
fi

echo "Setup complete!"