#!/bin/bash

# Install dependencies script for AI Employee System

echo "Setting up AI Employee System dependencies..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment (works for both Unix and Windows)
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium firefox webkit

echo "Installation complete!"
echo ""
echo "To activate the environment in the future, run:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  venv\Scripts\activate.bat (on Windows Command Prompt)"
    echo "  or source venv/Scripts/activate (on Git Bash)"
else
    echo "  source venv/bin/activate"
fi
echo ""
echo "Then you can run the system with:"
echo "  python run_system.py"