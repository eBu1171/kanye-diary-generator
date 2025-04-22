import os
import openai

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

# When the fine-tuning is complete, the fine_tuned_model field will contain the model name
# For now, we'll use a placeholder that you can replace later
fine_tuned_model = "ft:gpt-3.5-turbo-0125:org-zVOBqPzoM0Z6J286rekVkHmW:ftjob-7o4frbbFp5UvvB8wWRGsEr1n"  # Replace with your actual model name

# Example support ticket issues
issues = [
    "User can't login to the mobile app",
    "Customer reporting slow website performance",
    "User needs to change their email address",
    "Customer lost access to their account after password reset",
    "User experiencing checkout errors during payment"
]

# Generate support tickets
for issue in issues:
    response = client.chat.completions.create(
        model=fine_tuned_model,
        messages=[{"role": "user", "content": issue}]
    )
    
    print(f"\nIssue: {issue}")
    print("Generated Support Ticket:")
    print(response.choices[0].message.content)
    print("-" * 50) 