#!/bin/bash

# Script to create GitHub repository and push backend code
# Make sure you have GitHub CLI (gh) installed or create the repo manually first

REPO_NAME="ai-book-backend"
GITHUB_USER=$(git config user.name 2>/dev/null || echo "YOUR_GITHUB_USERNAME")

echo "Setting up GitHub repository for $REPO_NAME"
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "GitHub CLI detected. Creating repository..."
    gh repo create $REPO_NAME --public --source=. --remote=origin --push
    echo "Repository created and code pushed!"
else
    echo "GitHub CLI not found. Please follow these steps:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named: $REPO_NAME"
    echo "3. DO NOT initialize with README, .gitignore, or license"
    echo "4. Then run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
fi

