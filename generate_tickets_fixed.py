import os
import openai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# The ID of the fine-tuned model from the successful job
fine_tuned_model = "ft:gpt-3.5-turbo-0125:coworth:support-ticket-generator:BNXnFkcy"

# Example issues to generate support tickets for
issues = [
    "User can't verify email address.",
    "Website images not loading properly.",
    "Customer wants to cancel subscription.",
    "App freezes on startup.",
    "User reports incorrect pricing on product page."
]

# Generate support tickets
for issue in issues:
    response = client.chat.completions.create(
        model=fine_tuned_model,
        messages=[
            {"role": "system", "content": "You are a structured support ticket generator."},
            {"role": "user", "content": issue}
        ]
    )
    
    print(f"\nIssue: {issue}")
    print("Generated Support Ticket:")
    print(response.choices[0].message.content)
    print("-" * 50) 