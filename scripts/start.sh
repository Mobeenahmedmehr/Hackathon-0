#!/bin/bash

# Quick start script for AI Employee system

echo "Starting AI Employee system..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Run the system
echo "Starting AI Employee system..."
python run_system.py

echo "System status: Running"