import os
import openai

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

# First, upload the support ticket data file
print("Uploading support ticket data file...")
file_response = client.files.create(
    file=open("support_ticket_data.jsonl", "rb"),
    purpose="fine-tune"
)

file_id = file_response.id
print(f"File uploaded with ID: {file_id}")

# Create a fine-tuning job
print("Creating fine-tuning job...")
response = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo",
    suffix="support-ticket-generator"  # This will appear in the model name
)

print("Fine-tuning job created with ID:", response.id)
print("Status:", response.status)
print(response) 