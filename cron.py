import os
import requests
import json
import openai
import uuid
from datetime import datetime

# Set up API key and base URL
api_key = os.environ.get('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

# Your model ID
model_id = "ft:gpt-3.5-turbo-0125:coworth:kanye-diary-generator:BNkcq9DD"

# Twitter API 
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')

def generate_kanye_content():
    """Generate content using the Kanye model"""
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are Kanye West writing a diary entry. Be authentic and raw."},
                {"role": "user", "content": "Write a diary entry for today as Kanye West."}
            ],
            temperature=0.9,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def post_to_twitter(content):
    """Post content to Twitter API"""
    if not content:
        print("No content to post")
        return False
    
    # Truncate if needed
    if len(content) > 280:
        content = content[:277] + "..."
    
    headers = {
        "Authorization": f"Bearer {TWITTER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": content
    }
    
    try:
        response = requests.post(
            "https://api.twitter.com/2/tweets",
            headers=headers,
            json=data
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"Successfully posted tweet with ID: {result['data']['id']}")
            return True
        else:
            print(f"Failed to post tweet: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error posting to Twitter: {e}")
        return False

def main():
    print(f"Running scheduled job at {datetime.now()}")
    content = generate_kanye_content()
    if content:
        print("Generated content:", content[:50] + "...")
        success = post_to_twitter(content)
        if success:
            print("Successfully posted to Twitter")
        else:
            print("Failed to post to Twitter")
    else:
        print("Failed to generate content")

if __name__ == "__main__":
    main() 