import os
import openai
import time

# The API key should be set as an environment variable
client = openai.OpenAI()  # This will use the OPENAI_API_KEY environment variable

# Replace with your fine-tuning job ID
job_id = "ftjob-jPqVSvQG8t9K5drEB9ZexRYU"

# Check the status
response = client.fine_tuning.jobs.retrieve(job_id)
print("Status:", response.status)
print("Fine-tuned model:", response.fine_tuned_model)  # Will be None until the job is completed
print("Created at:", time.ctime(response.created_at))

if response.status == "succeeded":
    print("\nFine-tuning completed successfully!")
    print("Fine-tuned model ID:", response.fine_tuned_model)
    print("You can now use this model for inference.")
elif response.status == "failed":
    print("\nFine-tuning failed.")
    if response.error:
        print("Error code:", response.error.code)
        print("Error message:", response.error.message)
else:
    # Print estimated time remaining if available
    if response.estimated_finish:
        finish_time = time.ctime(response.estimated_finish)
        print("Estimated completion time:", finish_time)
    
    print("\nFine-tuning is still in progress.")
    print("Check back later for updates.")

print("\nFull response:")
print(response) 