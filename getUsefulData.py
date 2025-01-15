import json

with open("message.json", "r") as file:
    messagesList = json.load(file)
    
newStore = []

for message in messagesList:
    messageStore = {}
    
    messageStore["id"] = message["id"]
    messageStore["snippet"] = message.get("snippet", None)
    
    headers = message["payload"]["headers"]
    
    for info in headers:
        if info["name"] == "From":
            messageStore["Sender"] = info["value"].strip()
        
        elif info["name"] == "Subject":
            messageStore["Subject"] = info["value"].strip()
    newStore.append(messageStore)
    print(messageStore)
    
# print(newStore)
    