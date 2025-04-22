import os
import json
import time
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
import config

# Initialize OpenAI client with API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_completion(prompt, model=config.KANYE_MODEL_ID, temperature=1):
    """Get completion from OpenAI API"""
    try:
        # Use chat completions instead of completions
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1000,
            n=1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting completion: {e}")
        return None

def generate_kanye_prompt(date_str=None):
    """Generate a prompt for Kanye diary entry"""
    if not date_str:
        date_str = datetime.now().strftime("%B %d, %Y")
    
    # prompt = f"Diary entry, {date_str}\n\n"
    prompt = "Write a diary entry for today as Kanye West."
    return prompt

def generate_entries(num_entries=1, save_to_file=False):
    """Generate a specified number of Kanye-style diary entries"""
    entries = []
    
    for _ in range(num_entries):
        prompt = generate_kanye_prompt()
        entry_text = get_completion(prompt)
        
        if entry_text:
            entry = {
                "entry": entry_text,
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt
            }
            entries.append(entry)
        
        # Add a small delay to avoid rate limits
        time.sleep(0.5)
    
    # Save to file if requested
    if save_to_file and entries:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"kanye_entries_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(entries, f, indent=2)
        
        print(f"Saved {len(entries)} entries to {filename}")
    
    return entries

if __name__ == "__main__":
    # Example usage
    num_entries = 5
    entries = generate_entries(num_entries, save_to_file=True)
    
    # Print the first entry
    if entries:
        print("\nFirst generated entry:")
        print(entries[0]["entry"])