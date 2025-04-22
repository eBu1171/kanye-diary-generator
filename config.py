import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Get the absolute path to the .env file
env_path = Path('.') / '.env'
# Load environment variables from .env file if it exists
if env_path.exists():
    print(f"Loading .env file from: {env_path.absolute()}")
    load_dotenv(dotenv_path=env_path)
else:
    print("WARNING: .env file not found!")

# Flask configuration
SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
KANYE_MODEL_ID = os.getenv("KANYE_MODEL_ID", "ft:gpt-3.5-turbo-0125:coworth:kanye-diary-generator-v2:BOouRAAp")

# Twitter API configuration
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# Twitter OAuth 2.0
TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID", "")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET", "")

# Content management
MAX_CONTENT_ITEMS = int(os.getenv("MAX_CONTENT_ITEMS", "50"))
DEFAULT_POST_INTERVAL = int(os.getenv("DEFAULT_POST_INTERVAL", "3600"))  # in seconds, default 1 hour

# Database configuration (if needed)
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///content.db")

# App paths
CONTENT_STORE_PATH = os.getenv("CONTENT_STORE_PATH", "content_store.json")
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Generator models
SUPPORT_TICKET_MODEL_ID = os.environ.get('SUPPORT_TICKET_MODEL_ID', 'ft:gpt-3.5-turbo-0125:coworth:support-ticket-generator:BNXnFkcy')

# Flask settings
TWITTER_CALLBACK_URL = os.getenv("TWITTER_CALLBACK_URL", "http://localhost:5001/twitter/callback")

# App settings
MAX_CONTENT_ITEMS = 20  # Maximum number of content items to store in memory 