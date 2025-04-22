import os
import json
import random
import time
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
import config

# Initialize OpenAI client with API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# The ID of the fine-tuned model from the successful job
fine_tuned_model = config.SUPPORT_TICKET_MODEL_ID

# Base issue templates to generate variations from
base_issues = [
    "User can't {action} {item}.",
    "Customer {verb} {issue} with {product}.",
    "User reports {problem} when {activity}.",
    "App {verb} during {action}.",
    "{item} not {state} properly.",
    "Error message appears when {activity}.",
    "Customer wants to {action} their {item}.",
    "{product} shows incorrect {attribute}.",
    "User unable to access {feature}.",
    "{item} missing from {location}."
]

# Word lists for template filling
actions = ["login to", "access", "update", "reset", "verify", "change", "cancel", "view", "download", "upload"]
items = ["account", "password", "email address", "profile", "settings", "subscription", "payment method", "order history", "files", "content"]
verbs = ["experiences", "reports", "encounters", "notices", "complains about", "has issue with", "is having trouble with"]
issues = ["problem", "error", "difficulty", "confusion", "trouble", "issue"]
products = ["website", "mobile app", "desktop application", "account page", "checkout process", "login screen", "dashboard"]
problems = ["slow loading", "error message", "crash", "freezing", "unexpected behavior", "incorrect information", "missing data"]
activities = ["logging in", "making a purchase", "updating information", "browsing products", "submitting a form", "uploading files"]
states = ["working", "loading", "displaying", "functioning", "responding", "updating", "connecting"]
features = ["shopping cart", "account settings", "order history", "saved items", "search function", "help center"]
locations = ["cart", "profile", "dashboard", "order confirmation", "account summary", "receipt"]
attributes = ["price", "quantity", "description", "availability", "information", "status"]

# Function to generate a random issue from templates
def generate_random_issue():
    template = random.choice(base_issues)
    
    if "{action}" in template:
        template = template.replace("{action}", random.choice(actions))
    if "{item}" in template:
        template = template.replace("{item}", random.choice(items))
    if "{verb}" in template:
        template = template.replace("{verb}", random.choice(verbs))
    if "{issue}" in template:
        template = template.replace("{issue}", random.choice(issues))
    if "{product}" in template:
        template = template.replace("{product}", random.choice(products))
    if "{problem}" in template:
        template = template.replace("{problem}", random.choice(problems))
    if "{activity}" in template:
        template = template.replace("{activity}", random.choice(activities))
    if "{state}" in template:
        template = template.replace("{state}", random.choice(states))
    if "{feature}" in template:
        template = template.replace("{feature}", random.choice(features))
    if "{location}" in template:
        template = template.replace("{location}", random.choice(locations))
    if "{attribute}" in template:
        template = template.replace("{attribute}", random.choice(attributes))
        
    return template

# Generate a specified number of support tickets
def generate_tickets(count):
    tickets = []
    
    print(f"Generating {count} synthetic support tickets...")
    for i in range(count):
        issue = generate_random_issue()
        print(f"Generated issue: {issue}")
        
        # Call the fine-tuned model
        try:
            response = client.chat.completions.create(
                model=fine_tuned_model,
                messages=[
                    {"role": "system", "content": "You are a structured support ticket generator."},
                    {"role": "user", "content": issue}
                ]
            )
            
            # Extract the generated ticket
            ticket_text = response.choices[0].message.content
            print(f"Generated ticket: \n{ticket_text}\n")
            
            # Parse the ticket into a structured format
            ticket_lines = ticket_text.strip().split('\n')
            ticket_data = {
                "original_issue": issue,
                "generated_ticket": ticket_text,
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to parse the structured parts
            try:
                for line in ticket_lines:
                    if line.startswith("Issue:"):
                        ticket_data["issue_type"] = line.replace("Issue:", "").strip()
                    elif line.startswith("User:"):
                        ticket_data["user_type"] = line.replace("User:", "").strip()
                    elif line.startswith("Device:"):
                        ticket_data["device"] = line.replace("Device:", "").strip()
                    elif line.startswith("Summary:"):
                        ticket_data["summary"] = line.replace("Summary:", "").strip()
            except Exception as e:
                print(f"Warning: Could not fully parse ticket {i+1}: {e}")
            
            tickets.append(ticket_data)
            
            # Print progress
            print(f"Generated {i + 1}/{count} tickets")
                
            # Add a short delay to avoid rate limits
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error generating ticket {i+1}: {e}")
            time.sleep(5)  # Longer delay after an error
    
    return tickets

# Main function
if __name__ == "__main__":
    # Number of tickets to generate (reduced for testing)
    num_tickets = 1
    
    # Generate the tickets
    tickets = generate_tickets(num_tickets)
    
    # # Save to a JSON file
    # output_file = f"synthetic_tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    # with open(output_file, 'w') as f:
    #     json.dump(tickets, f, indent=2)
    
    # print(f"Generated {len(tickets)} tickets and saved to {output_file}") 
    print(f"Generated {len(tickets)} tickets") 