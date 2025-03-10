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

Your task is to filter emails that are relevant to job applications. Specifically, include 
emails that either:
- Confirm an application submission
- Indicate a rejection
- Signal progression in the hiring process

Determine relevance **solely** by analyzing the snippet, sender, and subject using your natural 
language understanding of job application communications.

### **Expected JSON Output Format:**  
Return a **valid JSON list** of dictionaries. Each dictionary should have:  
- A key named `'sender'` containing the sender's email address  
- A key named `'emails'` containing a **list** of relevant emails from that sender  

For example:
```json
[
  {{
    "sender": "jobs@example.com",
    "emails": [
      {{
        "id": "123abc",
        "snippet": "Thank you for applying...",
        "subject": "Application Received"
      }},
      {{
        "id": "456def",
        "snippet": "Unfortunately, we regret...",
        "subject": "Application Status Update"
      }}
    ]
  }}
]
Ensure that the output is a valid JSON structure.

Here is your input: {messages} """


        
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[ 
    {"role": "user", "content": prompt}
    ]
)
result = completion.choices[0]
#completion.choices[0].message.content.strip()
with open("completions.txt", "w") as file:
  try:
    file.write(result)
  except Exception as e:
    print(e)
    try:
      file.write(str(result))
    except Exception as e:
      print(e)
  finally:
    print(result)
# with open("rawgpt.txt", "w") as file:
#     file.write(result)
    
# print("raw from gpt", result)
# if result.startswith("```"):
#     parts = result.split("```")
#     result = parts[1] if len(parts) > 1 else result
#     result = result.replace("json", "", 1).strip()  # Remove 'json' if present

# # Find the first valid JSON structure
# index = result.find("[")
# if index != -1:
#     result = result[index:]

# # Ensure trailing code block markers are removed
# if result.endswith("```"):
#     result = result.rsplit("```", 1)[0].strip()

# # Convert to JSON
# try:
#     data = json.loads(result)
#     print("Valid JSON:", data)
# except json.JSONDecodeError:
#     print("Invalid JSON:", result)

# with open("cleanres.txt", "w") as file:
#     file.write(result)
# print("cleaned res", result)

# result = json.loads(result)

# with open("relevantMessages.json", "w") as file:
#     json.dump(result, file, indent=4)
# print(result)
# print()
# print(len(result))