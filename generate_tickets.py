import os
import openai

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

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
        messages=[{"role": "user", "content": issue}]
    )
    
    print(f"\nIssue: {issue}")
    print("Generated Support Ticket:")
    print(response.choices[0].message.content)
    print("-" * 50) 