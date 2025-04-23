# Synthetic Data Generator

A Flask application that generates synthetic content using fine-tuned OpenAI models, focusing on Kanye West diary entries and support tickets. The app allows for easy content generation, Twitter posting, and scheduling.

## Features

- Generate Kanye West style diary entries
- Generate realistic support tickets
- Post generated content to Twitter
- Schedule automatic posting
- Web interface for content management
- Railway deployment support

## Setup

### 1. Environment Setup

Clone the repository and create a `.env` file with your API keys:

```bash
# Clone the repository
git clone <repository-url>
cd synthetic-data-generator

# Create and edit .env file with your API keys
cp .env.example .env
```

Edit the `.env` file with your credentials:

```
OPENAI_API_KEY=your_openai_api_key
TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_CALLBACK_URL=http://localhost:5001/twitter/callback
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 2. Twitter OAuth Configuration

For Twitter integration to work, you need to set up a Twitter Developer account and configure OAuth:

1. Go to the [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new project and app
3. Configure User Authentication Settings:
   - Enable OAuth 2.0
   - Set the callback URL to match your TWITTER_CALLBACK_URL in .env
   - For local development: `http://localhost:5001/twitter/callback`
   - For production: Your deployment URL (e.g., `https://your-app.up.railway.app/twitter/callback`)
4. Request the following scopes:
   - `tweet.read`
   - `tweet.write` 
   - `users.read`
   - `offline.access`

**Important**: When deploying to Railway or any other platform, update both:
- The callback URL in your Twitter Developer Portal
- The TWITTER_CALLBACK_URL environment variable in your deployment

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
flask run --port=5001
```

Visit `http://localhost:5001` in your browser.

## Deployment to Railway

### 1. Create Railway Account

Sign up at [Railway](https://railway.app/) using GitHub.

### 2. Deploy Your Project

1. In the Railway dashboard, create a new project
2. Choose "Deploy from GitHub repo"
3. Connect your GitHub account and select your repository
4. Configure environment variables in the Railway dashboard

### 3. Set Up Scheduled Tasks

Railway supports cron jobs for automatic content generation and posting:

1. Create a new service in your project
2. Select "Empty Service"
3. Set the start command to: `python cron.py`
4. Configure as cron job with schedule: `0 0 * * *` (daily at midnight)

## API Keys Safety

This project uses environment variables for all sensitive information:

- API keys are loaded from `.env` file locally
- When deploying, set environment variables in the Railway dashboard
- The `.env` file is in `.gitignore` to prevent accidental commits
- Never hardcode API keys in the source code

## Usage

### Generate Kanye Diary Entry in Terminal

```bash
python generate_kanye_terminal.py
```

## Notes

- The Twitter API requires OAuth 2.0 authentication
- Fine-tuned model IDs are configured in `config.py` 