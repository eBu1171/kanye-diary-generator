import os
import openai

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

response = client.fine_tuning.jobs.create(
    training_file="file-CNH5zFyPQwFzCUbNdKk8vL",
    model="gpt-3.5-turbo"
)

print("Fine-tuning job created with ID:", response.id)
print("Status:", response.status)
print(response) 