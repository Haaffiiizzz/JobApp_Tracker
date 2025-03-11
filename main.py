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
    keywords = ("application OR applying OR applied OR rejection OR rejected OR unfortunately OR regret OR submit OR "
            "submitted OR thank OR thank you OR considered OR considering OR experience OR qualifications OR skills OR "
            "background OR eligibility OR criteria OR requirements OR consideration OR reviewed OR screening OR interview OR "
            "shortlist OR selection OR candidate OR position OR role OR opportunity OR unsuccessful OR declined OR assessment "
            "OR follow-up OR response OR update OR hiring OR offer OR accepted OR hired OR appreciate OR grateful OR regards OR "
            "sincerely OR competitive")

    query = f'after:2024/06/01 before:2025/03/11 {keywords}'
    query = urllib.parse.quote(query)
    messageIds = []
    
    url = f'https://gmail.googleapis.com/gmail/v1/users/dadaabdulhafiz0306%40gmail.com/messages?q={query}&key={key}&maxResults=500'

    response = requests.get(url, headers=headers)
    messageIds = [messageDict["id"] for messageDict in response.json()["messages"]]
    nextPageToken = response.json().get("nextPageToken", None)
    i = 1
    while nextPageToken:
        print("entered next page", i)
        time.sleep(1)
        url = f'https://gmail.googleapis.com/gmail/v1/users/dadaabdulhafiz0306%40gmail.com/messages?q={query}&key={key}&maxResults=500&pageToken={nextPageToken}'
        response = requests.get(url, headers=headers)
        nextPageToken = response.json().get("nextPageToken", None)
        
        messageIds.extend([messageDict["id"] for messageDict in response.json()["messages"]])
        i += 1
    
    
    return messageIds
    
def getMessageBatch(messageIds: list) -> list:
    
    """
    Given a list of messageIds, this function attempts to get the message infos
    in batches. Theres a limit to the number of requests that can be made at a time
    so the function is designed to handle this. The messages are returned in a list.
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

def runBatches(messageIds: list):
    """Using the message ids, I try to get the messages in batches and store them in a json file.
    """
    messageList = []
    
    for i in range(0, len(messageIds), 5):
        IdSection = messageIds[i: i+5]
        sectionMetadata = getMessageBatch(IdSection)
        
        for metadata in sectionMetadata:
            messageList.append(metadata)
        messageList.extend(sectionMetadata)
        print(f"Section {i} done")
        
        
    with open("messages.json", "w") as file:
        json.dump(messageList, file, indent=4)
        
    return messageList
    # print(messageList)

def main():
    messageIds = getMessageId()
    
    # messages = runBatches(messageIds)
    
    print(messageIds, len(messageIds))
        
        
if __name__ == "__main__":
    main()
