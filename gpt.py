import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
with open("cleanedMessages.json", "r") as file:
    messages = json.load(file)
    
GPT_API_KEY = os.getenv('GPT_API_KEY')
client = OpenAI(api_key = GPT_API_KEY)

prompt = f"""
I am giving you a list of dictionaries representing emails from a Gmail account.
Each email dictionary has the following structure:
{{
  'id': 'A unique ID for the email (you do not need to process this field)',
  'snippet': 'A snippet from the email body',
  'Sender': 'The sender of the email',
  'Subject': 'The subject of the email'
}}

Your task is to return a JSON list (valid JSON) of email dictionaries in the same format,
but only include emails that are relevant to job applications. Specifically, include 
emails that either confirm an application, indicate a rejection, or signal progression in the 
hiring process. Determine relevance solely by analyzing the snippet, sender, and subject
using your natural language understanding of job application communications. If no emails match these 
criteria, return an empty list.

This is your input: {messages}
"""


        
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[ 
    {"role": "user", "content": prompt}
    ]
)
result = completion.choices[0].message.content.strip()


if result.startswith("```"):
    result = result.split("```")[1].strip()
    index = result.find("[")
    result = result[index:]
if result.endswith("```"):
    result = result.split("```")[0].strip()
    
result = json.loads(result)

with open("relevantMessages.json", "w") as file:
    json.dump(result, file, indent=4)
print(result)