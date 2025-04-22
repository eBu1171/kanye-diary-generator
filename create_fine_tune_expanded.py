import os
import openai

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

# First, upload the expanded data file
print("Uploading expanded data file...")
file_response = client.files.create(
    file=open("data_expanded.jsonl", "rb"),
    purpose="fine-tune"
)

file_id = file_response.id
print(f"File uploaded with ID: {file_id}")

# Create a fine-tuning job
print("Creating fine-tuning job...")
response = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo"
)

print("Fine-tuning job created with ID:", response.id)
print("Status:", response.status)
print(response) 