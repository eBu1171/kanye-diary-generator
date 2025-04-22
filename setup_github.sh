#!/bin/bash

# This script sets up a new GitHub repository and pushes the code

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install git first."
    exit 1
fi

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    echo "Git repository initialized."
fi

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Project setup with API safety"

# Get GitHub repository URL from user
echo "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git):"
read github_url

# Add remote and push
if [ -n "$github_url" ]; then
    git remote add origin $github_url
    git branch -M main
    git push -u origin main
    echo "Code pushed to GitHub successfully."
else
    echo "No GitHub URL provided. You can push manually later with:"
    echo "git remote add origin YOUR_GITHUB_REPO_URL"
    echo "git branch -M main"
    echo "git push -u origin main"
fi

echo "Setup complete!" 