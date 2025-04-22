import os
from supabase import create_client

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

def save_content_to_db(content):
    """Save content to Supabase"""
    if not supabase:
        return False
        
    data = {
        "type": content["type"],
        "text": content["text"],
        "generated_at": content["generated_at"],
        "status": content["status"]
    }
    
    if "tweet_id" in content:
        data["tweet_id"] = content["tweet_id"]
        
    if "posted_at" in content:
        data["posted_at"] = content["posted_at"]
        
    if "error" in content:
        data["error"] = content["error"]
        
    response = supabase.table("content").insert(data).execute()
    return response.data
    
def get_content_from_db(limit=10):
    """Get content from Supabase"""
    if not supabase:
        return []
        
    response = supabase.table("content").select("*").order("generated_at", desc=True).limit(limit).execute()
    return response.data

def update_content_in_db(content_id, updates):
    """Update content in Supabase"""
    if not supabase:
        return False
        
    response = supabase.table("content").update(updates).eq("id", content_id).execute()
    return response.data

def delete_content_from_db(content_id):
    """Delete content from Supabase"""
    if not supabase:
        return False
        
    response = supabase.table("content").delete().eq("id", content_id).execute()
    return response.data

def get_content_by_id_from_db(content_id):
    """Get specific content from Supabase by ID"""
    if not supabase:
        return None
        
    try:
        response = supabase.table("content").select("*").eq("id", content_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting content by ID from Supabase: {e}")
        return None 