# Fine-Tuned Support Ticket Generator

This project demonstrates how to fine-tune an OpenAI GPT model to generate structured support tickets. It's an example of using fine-tuning for synthetic data generation with a consistent format.

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv finetune_env
   source finetune_env/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install openai
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```
   Or directly in your script:
   ```python
   client = openai.OpenAI(api_key="your-api-key")
   ```

## Files

- `support_ticket_data.jsonl`: Training data in the required format for fine-tuning a support ticket generator
- `create_support_ticket_model.py`: Script to create a fine-tuning job for the support ticket generator
- `check_support_ticket_model.py`: Script to check the status of a fine-tuning job
- `generate_tickets.py` and `generate_tickets_fixed.py`: Scripts to use the fine-tuned model

## Usage

1. Prepare your training data in the correct format in a JSONL file. Each example should follow this structure:
   ```json
   {"messages":[{"role":"system","content":"You are a structured support ticket generator."},{"role":"user","content":"User can't reset password."},{"role":"assistant","content":"Issue: Password Reset\nUser: Random User\nDevice: Unknown\nSummary: The user cannot reset their password using the email recovery link."}]}
   ```

2. Upload your training file and create a fine-tuning job:
   ```bash
   python create_support_ticket_model.py
   ```

3. Check the status of your fine-tuning job:
   ```bash
   python check_support_ticket_model.py
   ```

4. Once the fine-tuning job is complete, use your fine-tuned model:
   ```bash
   python generate_tickets_fixed.py
   ```

## Generated Output Format

The fine-tuned model will generate support tickets with a consistent structure:

```
Issue: [Issue Type]
User: [User Description]
Device: [Device Type or N/A]
Summary: [Detailed description of the issue]
```

## Benefits of Fine-Tuning for Synthetic Data

- **Consistent Format**: Every generated ticket follows the same structure
- **No Need for Complex Prompting**: The model has learned the required format
- **Efficiency**: Generate thousands of realistic support tickets quickly
- **Customization**: You can tailor the model to your specific needs
- **Better Control**: Less random variation than using standard models

## Practical Applications

1. Training data for support ticket classification systems
2. Testing customer service automation
3. Simulating customer interactions
4. Creating realistic datasets for analytics 