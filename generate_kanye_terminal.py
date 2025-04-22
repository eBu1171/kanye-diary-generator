import os
import openai
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# The model ID of your fine-tuned Kanye model
model_id = "ft:gpt-3.5-turbo-0125:coworth:kanye-diary-generator:BNkcq9DD"

def generate_diary_entry(temperature=0.9):
    """Generate a Kanye diary entry using the fine-tuned model"""
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are Kanye West writing a diary entry. Be authentic and raw."},
                {"role": "user", "content": "Write a diary entry for today as Kanye West."}
            ],
            temperature=temperature,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating diary entry: {e}")
        return None

if __name__ == "__main__":
    # Allow passing temperature as argument
    temp = 0.9
    if len(sys.argv) > 1:
        try:
            temp = float(sys.argv[1])
        except ValueError:
            print("Temperature must be a number between 0 and 2. Using default 0.9.")
    
    print("\n===== KANYE DIARY ENTRY =====\n")
    entry = generate_diary_entry(temperature=temp)
    if entry:
        print(entry)
    print("\n=============================\n") 