import os
import openai

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

# When the fine-tuning is complete, the fine_tuned_model field will contain the model name
# For now, we'll use a placeholder that you can replace later
fine_tuned_model = "ft:gpt-3.5-turbo-0125:org-zVOBqPzoM0Z6J286rekVkHmW:ftjob-7o4frbbFp5UvvB8wWRGsEr1n"  # Replace with your actual model name

# Example usage
response = client.chat.completions.create(
    model=fine_tuned_model,
    messages=[
        {"role": "user", "content": "What are the key differences between supervised and unsupervised learning?"}
    ]
)

print("Response:", response.choices[0].message.content)
print(response) 