#!/bin/bash
set -e  # Exit on error

echo "----- Starting Build Process -----"

# Navigate to backend
cd backend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Install Playwright with Chromium
echo "Installing Playwright..."
npx playwright install --with-deps chromium

echo "----- Build Completed Successfully -----"
