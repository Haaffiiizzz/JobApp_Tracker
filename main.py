import requests
import json
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
import os.path
import urllib.parse
import time

def getMessageId() -> list:
    
    """
    Here I am making a call to get the a list of dicts containing message ids
    and thread ids over a time frame having specific keywords. Other filters/ queries can be added including
    where message is from (f string from:({sender_emails})). A list of the message Ids
    is returned.
    """
    with open("apikey.txt", "r") as file:
        key = file.read()

    with open("token.json", "r") as file:
        token = json.loads(file.read())["token"] 

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }
    query = 'after:2024/06/01 before:2025/01/14 "application OR applying OR applied OR rejection OR rejected"'
    query = urllib.parse.quote(query)
    
    url = f'https://gmail.googleapis.com/gmail/v1/users/dadaabdulhafiz0306%40gmail.com/messages?q={query}&key={key}&maxResults=20'

    response = requests.get(url, headers=headers)
    print(response.json())
    messageIds = [messageDict["id"] for messageDict in response.json()["messages"]]
    
    return messageIds
    
def getMessageBatch(messageIds: list) -> list:
    
    """
    Given a list of messageIds, this function attempts to get the message infos
    in batches. Each batch is limited to 100 retrievals. It'd make sense to send
    a messageIds list with size 100.After authentication, a list of message dicts is returned.
    """
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
                

    service = build('gmail', 'v1', credentials=creds)
    messages = []
    
    # Callback function to process responses
    def handleResponse(request_id, response, exception):
        if exception is not None:
            print(f"An error occurred for request {request_id}: {exception}")
        else:
            messages.append(response)


    batch = BatchHttpRequest(callback=handleResponse, batch_uri='https://gmail.googleapis.com/batch')

    for message_id in messageIds:
        request = service.users().messages().get(userId='me', id=message_id, format='metadata')
        batch.add(request)

    batch.execute()

    return messages

def main():
    messageIds = getMessageId()
    with open("messageid.json", "w") as file:
        json.dump(messageIds, file, indent=4)
        
    metadataList = []
    
    for i in range(0, len(messageIds), 10):
        IdSection = messageIds[i:i+10]
        sectionMetadata = getMessageBatch(IdSection)
        
        for metadata in sectionMetadata:
            metadataList.append(metadata)
        metadataList.extend(sectionMetadata)
        print(f"Section {i} done")
        
        time.sleep(2)
        
    with open("messages.json", "w") as file:
        
        json.dump(metadataList, file, indent=4)
    print(metadataList)
        
        
if __name__ == "__main__":
    main()
