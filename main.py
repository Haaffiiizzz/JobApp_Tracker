import requests
import json
import base64
from bs4 import BeautifulSoup
with open("apikey.txt", "r") as file:
    key = file.read()

with open("token.json", "r") as file:
    token = json.loads(file.read())["token"] 

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json',
}

profile = requests.get(
    f'https://gmail.googleapis.com/gmail/v1/users/dadaabdulhafiz0306%40gmail.com/profile?key={key}',
    headers=headers,
)

messages = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/dadaabdulhafiz0306%40gmail.com/messages?q=after:2024/06/01 before:2025/01/14&key={key}&maxResults=500",
                        headers=headers) #get all messages within a time frame. could add sender here to by adding with f string from:({sender_emails}) which is a string of emails with OR separating each.
print(messages.json())
# for message in messages.json():
 
messageIds = [messageDict["id"] for messageDict in messages.json()["messages"]]
with open("messageIdList.json", "w") as file:
    json.dump(messageIds, file, indent=4)



# for message in messages.json()["messages"][0:20]:
#     message = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/dadaabdulhafiz0306%40gmail.com/messages/{message['id']}?format=full&key={key}",
#                         headers=headers)
#     # with open(f"{count}.json", "w") as file:
#     #     json.dump(message.json(), file, indent=10)
#     # print(message.json()["payload"]["body"]["data"])
    
#     encoded_body = message.json().get("payload", {}).get("body", {}).get("data", "")

#     # Decode the Base64 data
#     decoded_bytes = base64.urlsafe_b64decode(encoded_body)
#     decoded_content = decoded_bytes.decode("utf-8")

#     # Check if the content is HTML
#     mime_type = message.json().get("payload", {}).get("mimeType", "")
#     if mime_type == "text/html":
#         # Parse the HTML content
#         soup = BeautifulSoup(decoded_content, "html.parser")
#         readable_content = soup.get_text()
#         print("HTML Content (Readable):")
#         print(readable_content)
    
#     print("\n")
    
# https://www.googleapis.com/gmail/v1/users/me/messages?q=in:sent after:2014/01/01 before:2014/02/01