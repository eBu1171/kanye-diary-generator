import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# First, upload the fixed Kanye diary data file
print("Uploading fixed Kanye diary data file...")
file_response = client.files.create(
    file=open("kanye_fixed.jsonl", "rb"),
    purpose="fine-tune"
)

file_id = file_response.id
print(f"File uploaded with ID: {file_id}")

# Create a fine-tuning job
print("Creating fine-tuning job...")
response = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="ft:gpt-3.5-turbo-0125:coworth:kanye-diary-generator:BNkcq9DD",
    suffix="kanye-diary-generator-v2"
)

print("Fine-tuning job created with ID:", response.id)
print("Status:", response.status)
print(response) 