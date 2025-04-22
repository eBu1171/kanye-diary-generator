import os
import openai
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key from environment
api_key = os.environ.get("OPENAI_API_KEY") 
client = openai.OpenAI(api_key=api_key)

# Job ID from create_kanye_model_fixed.py
job_id = "ftjob-AHHTwrQrc7HsCdifIIYtHwPW"

# Check the status
try:
    response = client.fine_tuning.jobs.retrieve(job_id)
    print("Status:", response.status)
    print("Fine-tuned model:", response.fine_tuned_model)  # Will be None until the job is completed
    print("Created at:", time.ctime(response.created_at))

    if response.status == "succeeded":
        print("\nFine-tuning completed successfully!")
        print("Fine-tuned model ID:", response.fine_tuned_model)
        print("You can now use this model for generating Kanye-style diary entries.")
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
except Exception as e:
    print(f"Error: {e}")
    print("Make sure to update the job_id variable with the ID returned from create_kanye_model_fixed.py") 