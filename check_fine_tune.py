import os
import openai
import time

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

# Replace with your fine-tuning job ID
job_id = "ftjob-7o4frbbFp5UvvB8wWRGsEr1n"

# Check the status
response = client.fine_tuning.jobs.retrieve(job_id)
print("Status:", response.status)
print("Fine-tuned model:", response.fine_tuned_model)  # Will be None until the job is completed
print("Created at:", time.ctime(response.created_at))
print(response) 