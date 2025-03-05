import json
import re

with open("metadata.json", "r") as file:
    messagesList = json.load(file)
    
newStore = []
pattern = r'[\u200b\u200c\u200d\u200e\u200f\ufeff\u034f]'
for message in messagesList:
    messageStore = {}
    
    messageStore["id"] = message["id"]
    messageStore["snippet"] = re.sub(pattern, '', message.get("snippet", None)).strip()
    
    
    headers = message["payload"]["headers"]
    
    for info in headers:
        if info["name"] == "From":
            messageStore["Sender"] = info["value"].strip()
        
        elif info["name"] == "Subject":
            messageStore["Subject"] = info["value"].strip()
    newStore.append(messageStore)
    

with open("cleanedMessages.json", "w") as file:
    json.dump(newStore, file, indent=4) 
# print(newStore)
    