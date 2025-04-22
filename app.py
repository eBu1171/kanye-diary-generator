from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import json
import secrets
from datetime import datetime, timedelta
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
import uuid  # For generating unique IDs
import requests

# Import our generators
from batch_generate_kanye import generate_entries as generate_kanye
from batch_generate_tickets import generate_tickets as generate_support_tickets

# Twitter/X API
import tweepy

# Import configuration
import config

# Import Supabase functions
from db import save_content_to_db, get_content_from_db, update_content_in_db, delete_content_from_db, get_content_by_id_from_db

# In-memory content storage
content_store = {"entries": []}

def save_content(content):
    """Save content to in-memory storage"""
    global content_store
    content_store = content

def load_content():
    """Load content from in-memory storage"""
    return content_store

app = Flask(__name__, 
            template_folder=config.TEMPLATES_DIR, 
            static_folder=config.STATIC_DIR)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# In-memory storage - in production, use Supabase
generated_content = []  # Stores recently generated content
posting_schedule = []   # Stores scheduled posts
posting_stats = {
    "kanye": {"today": 0, "total": 0, "failures": 0},
    "support_tickets": {"today": 0, "total": 0, "failures": 0}
}
settings = {
    "content_type": "kanye",  # or "support_tickets"
    "frequency": 5,  # posts per day
    "is_posting": False
}

# Twitter/X API client
def get_twitter_client():
    try:
        # OAuth 2.0 with Client ID and Client Secret
        if config.TWITTER_CLIENT_ID and config.TWITTER_CLIENT_SECRET:
            print("Using OAuth 2.0 authentication")
            
            # Check if we have a valid access token in the session
            if 'twitter_oauth2_token' in session:
                print("Using OAuth 2.0 token from session as access token")
                client = tweepy.Client(
                    consumer_key=config.TWITTER_CLIENT_ID,
                    consumer_secret=config.TWITTER_CLIENT_SECRET,
                    access_token=session['twitter_oauth2_token']
                )
                return client
                
        # If we get here, we can't authenticate
        print("No valid authentication method found")
        return None
    except Exception as e:
        print(f"Error creating Twitter client: {e}")
        return None

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Generate content based on type
def generate_content(content_type):
    try:
        if content_type == "kanye":
            entries = generate_kanye(1)
            content = {
                "id": str(uuid.uuid4()),
                "type": "kanye",
                "text": entries[0]["entry"],
                "generated_at": datetime.now().isoformat(),
                "status": "pending"
            }
        else:  # support_tickets
            tickets = generate_support_tickets(1)
            content = {
                "id": str(uuid.uuid4()),
                "type": "support_ticket",
                "text": tickets[0]["generated_ticket"],
                "generated_at": datetime.now().isoformat(),
                "status": "pending"
            }
        
        # Add to in-memory storage
        generated_content.insert(0, content)  # Add to the beginning of the list
        
        # Keep only the most recent 20 items
        if len(generated_content) > config.MAX_CONTENT_ITEMS:
            generated_content.pop()
        
        # Save to Supabase
        save_content_to_db(content)
            
        return content
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

# Post content to Twitter/X
def post_to_twitter(content_id):
    if 'twitter_oauth2_token' not in session:
        flash("Twitter not connected", "error")
        return False
        
    # Step 1: Try to find content in memory first
    content = next((c for c in generated_content if c.get("id") == content_id), None)
    
    # Step 2: If not found in memory, try to get it from Supabase
    if not content:
        print(f"Content ID {content_id} not found in memory, trying Supabase...")
        # Get content from Supabase
        content = get_content_by_id_from_db(content_id)
        
        # If found in Supabase, add it to in-memory storage
        if content:
            print(f"Content found in Supabase: {content.get('type')}")
            generated_content.append(content)
    
    # Step 3: If still not found, return error
    if not content:
        flash("Content not found in memory or database", "error")
        return False
    
    # Try different authentication methods
    error_messages = []
    
    # Direct API call with requests
    try:
        print("Trying direct API call with requests...")
        token = session['twitter_oauth2_token']
        
        # Make the request to post a tweet
        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {"text": content["text"]}
        
        response = requests.post(url, headers=headers, json=data)
        print(f"API response: {response.status_code} - {response.text}")
        
        if response.status_code in [200, 201]:
            # Success
            tweet_data = response.json()
            tweet_id = tweet_data.get('data', {}).get('id')
            
            if tweet_id:
                # Update content status in memory
                content["status"] = "posted"
                content["tweet_id"] = tweet_id
                content["posted_at"] = datetime.now().isoformat()
                
                # Update in Supabase
                update_data = {
                    "status": "posted",
                    "tweet_id": tweet_id,
                    "posted_at": datetime.now().isoformat()
                }
                update_content_in_db(content_id, update_data)
                
                # Update stats
                posting_stats[content["type"]]["today"] += 1
                posting_stats[content["type"]]["total"] += 1
                
                print(f"Successfully posted tweet with ID: {tweet_id}")
                flash("Posted to Twitter", "success")
                return True
            else:
                error_messages.append("Tweet posted but could not extract tweet ID")
        else:
            error_messages.append(f"Direct API call failed: {response.status_code} - {response.text}")
    except Exception as e:
        error_messages.append(f"Direct API call exception: {str(e)}")
        
    # If we get here, all methods failed
    error_message = "\n".join(error_messages)
    print(f"All posting methods failed:\n{error_message}")
    
    # Update error status
    content["status"] = "failed"
    content["error"] = error_message
    
    # Update in Supabase
    update_data = {
        "status": "failed",
        "error": error_message
    }
    update_content_in_db(content_id, update_data)
    
    posting_stats[content["type"]]["failures"] += 1
    
    # Show actual error to user
    flash(f"Twitter Error: {error_message}", "error")
    return False

# Schedule next posts based on frequency setting
def schedule_posts():
    if not settings["is_posting"]:
        return
    
    # Clear existing schedule
    for job in scheduler.get_jobs():
        if job.id.startswith("post_"):
            scheduler.remove_job(job.id)
    
    # Calculate posting times
    posts_per_day = settings["frequency"]
    if posts_per_day <= 0:
        return
    
    now = datetime.now()
    waking_hours = 16  # Assume 16 hours of active time (8am - midnight)
    interval_mins = (waking_hours * 60) // posts_per_day
    
    # Schedule posts
    posting_schedule.clear()
    for i in range(posts_per_day):
        post_time = now + timedelta(minutes=interval_mins * (i + 1))
        
        # Don't schedule posts between midnight and 8am
        hour = post_time.hour
        if hour < 8:
            post_time = post_time.replace(hour=8, minute=0)
        
        # Generate a unique ID for this scheduled post
        job_id = f"post_{i}_{post_time.isoformat()}"
        
        # Add a job to generate and post content
        def scheduled_post():
            # Check if we have a valid OAuth 2.0 token
            if 'twitter_oauth2_token' not in session:
                print("Scheduled post failed: Twitter not connected")
                return
                
            content = generate_content(settings["content_type"])
            if content:
                post_to_twitter(content["id"])
        
        scheduler.add_job(
            func=scheduled_post,
            trigger="date",
            run_date=post_time,
            id=job_id
        )
        
        posting_schedule.append({
            "id": i,
            "time": post_time.isoformat(),
            "content_type": settings["content_type"]
        })

# Reset daily stats at midnight
@scheduler.scheduled_job('cron', hour=0, minute=0)
def reset_daily_stats():
    for content_type in posting_stats:
        posting_stats[content_type]["today"] = 0

# Routes
@app.route('/')
def index():
    # Check if Twitter is connected via OAuth 2.0
    twitter_connected = 'twitter_oauth2_token' in session
    
    # Set username if we have a connection but no username
    if twitter_connected and 'twitter_username' not in session:
        try:
            # Create client with proper access token
            client = tweepy.Client(
                consumer_key=config.TWITTER_CLIENT_ID,
                consumer_secret=config.TWITTER_CLIENT_SECRET,
                access_token=session['twitter_oauth2_token']
            )
            
            # Get user information
            response = client.get_me()
            if response and response.data:
                session['twitter_username'] = response.data.username
        except Exception as e:
            print(f"Error getting Twitter credentials: {e}")
    
    # Calculate next post time
    next_post_time = None
    if posting_schedule:
        next_post = min(posting_schedule, key=lambda x: x["time"])
        next_post_time = datetime.fromisoformat(next_post["time"])
    
    # Get content from Supabase if available, otherwise use in-memory
    db_content = get_content_from_db(10)
    content_to_display = db_content if db_content else generated_content[:10]
    
    return render_template(
        'index.html',
        twitter_connected=twitter_connected,
        content=content_to_display,
        settings=settings,
        stats=posting_stats,
        next_post_time=next_post_time
    )

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        content_type = request.form.get('content_type', settings["content_type"])
        
        # Generate content using our utility function
        content = generate_content(content_type)
        
        if content:
            flash(f"Successfully generated 1 new {content_type.capitalize()} entry!", "success")
        else:
            flash("Failed to generate content", "error")
        
        return redirect(url_for('index'))
    
    return render_template('generate.html')

@app.route('/post/<content_id>', methods=['POST'])
def post(content_id):
    success = post_to_twitter(content_id)
    
    if success:
        flash("Posted to Twitter", "success")
    else:
        flash("Failed to post to Twitter", "error")
        
    return redirect(url_for('index'))

@app.route('/settings', methods=['POST'])
def update_settings():
    settings["content_type"] = request.form.get('content_type', settings["content_type"])
    settings["frequency"] = int(request.form.get('frequency', settings["frequency"]))
    
    is_posting = request.form.get('is_posting') == 'true'
    if is_posting != settings["is_posting"]:
        settings["is_posting"] = is_posting
        if is_posting:
            schedule_posts()
        else:
            # Clear existing schedule
            for job in scheduler.get_jobs():
                if job.id.startswith("post_"):
                    scheduler.remove_job(job.id)
            posting_schedule.clear()
    
    flash("Settings updated", "success")
    return redirect(url_for('index'))

@app.route('/twitter/auth')
def twitter_auth():
    # OAuth 2.0 Authorization URL with required scopes for posting tweets
    redirect_uri = config.TWITTER_CALLBACK_URL
    
    # Create a random state to prevent CSRF attacks
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    
    # Create a code challenge (for PKCE)
    code_verifier = "challenge123456789012345678901234567890"  # Use the same value for challenge and verifier
    session['code_verifier'] = code_verifier  # Save for callback verification
    
    # Request the specific scopes needed for posting tweets
    scopes = "tweet.read tweet.write users.read offline.access"
    
    oauth2_url = (
        f"https://twitter.com/i/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={config.TWITTER_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
        f"&state={state}"
        f"&code_challenge={code_verifier}"
        f"&code_challenge_method=plain"
    )
    
    print(f"Redirecting to Twitter auth URL: {oauth2_url}")
    return redirect(oauth2_url)

@app.route('/twitter/callback')
def twitter_callback():
    code = request.args.get('code')
    if not code:
        flash("Authentication failed - no code received", "error")
        return redirect(url_for('index'))
    
    try:
        # Exchange code for access token
        token_url = "https://api.twitter.com/2/oauth2/token"
        
        # Get the code verifier from session
        code_verifier = session.get('code_verifier', "challenge123456789012345678901234567890")
        
        payload = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': config.TWITTER_CLIENT_ID,
            'redirect_uri': config.TWITTER_CALLBACK_URL,
            'code_verifier': code_verifier  # Must match the challenge used in auth
        }
        
        auth = (config.TWITTER_CLIENT_ID, config.TWITTER_CLIENT_SECRET)
        token_response = requests.post(token_url, data=payload, auth=auth)
        
        print(f"Token response: {token_response.status_code} - {token_response.text}")
        
        if token_response.status_code != 200:
            flash(f"Failed to get access token: {token_response.text}", "error")
            return redirect(url_for('index'))
        
        token_data = token_response.json()
        print(f"Token data received: {token_data.keys()}")
        
        # Store the complete token data in session
        session['twitter_oauth2_token'] = token_data['access_token']
        
        # For debugging - print token info
        print(f"Access token: {token_data['access_token'][:10]}...")
        print(f"Token type: {token_data.get('token_type', 'not provided')}")
        print(f"Expires in: {token_data.get('expires_in', 'not provided')}")
        
        # Get user info using the token
        client = None
        try:
            # Try first as bearer token
            client = tweepy.Client(bearer_token=token_data['access_token'])
            user_response = client.get_me()
            username = user_response.data.username
            session['twitter_username'] = username
        except Exception as e:
            print(f"Bearer token approach failed: {e}")
            try:
                # Fall back to access_token approach
                client = tweepy.Client(
                    consumer_key=config.TWITTER_CLIENT_ID,
                    consumer_secret=config.TWITTER_CLIENT_SECRET,
                    access_token=token_data['access_token']
                )
                user_response = client.get_me()
                username = user_response.data.username
                session['twitter_username'] = username
            except Exception as e2:
                print(f"Access token approach also failed: {e2}")
                # If both failed, try direct API call with the token
                headers = {
                    "Authorization": f"Bearer {token_data['access_token']}",
                    "Content-Type": "application/json"
                }
                me_response = requests.get("https://api.twitter.com/2/users/me", headers=headers)
                print(f"Direct API call result: {me_response.status_code} - {me_response.text}")
                user_data = me_response.json()
                if 'data' in user_data and 'username' in user_data['data']:
                    session['twitter_username'] = user_data['data']['username']
                    flash(f"Connected to Twitter as @{user_data['data']['username']}", "success")
                    return redirect(url_for('index'))
                else:
                    raise Exception("Could not get username from API response")
        
        flash(f"Connected to Twitter as @{session['twitter_username']}", "success")
    except Exception as e:
        flash(f"Twitter authentication failed: {e}", "error")
        print(f"Detailed auth error: {e}")
        
    return redirect(url_for('index'))

@app.route('/twitter/disconnect')
def twitter_disconnect():
    session.pop('twitter_oauth2_token', None)
    session.pop('twitter_username', None)
    
    flash("Disconnected from Twitter", "success")
    return redirect(url_for('index'))

@app.route('/api/entries')
def api_entries():
    content = load_content()
    return jsonify(content["entries"])

@app.route('/entries/<int:entry_id>')
def view_entry(entry_id):
    content = load_content()
    if 0 <= entry_id < len(content["entries"]):
        entry = content["entries"][entry_id]
        return render_template('entry.html', entry=entry, entry_id=entry_id)
    flash("Entry not found", "error")
    return redirect(url_for('index'))

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    content = load_content()
    if 0 <= entry_id < len(content["entries"]):
        content["entries"].pop(entry_id)
        save_content(content)
        flash("Entry deleted successfully", "success")
    else:
        flash("Entry not found", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize content store if empty
    if not content_store["entries"]:
        save_content({"entries": []})
    
    # Debug: Print API key (redacted)
    api_key = config.OPENAI_API_KEY
    if api_key:
        print(f"Using OpenAI API key: {api_key[:5]}...{api_key[-4:]}")
    else:
        print("WARNING: No OpenAI API key found!")
        
    app.run(host='0.0.0.0', port=5001) 