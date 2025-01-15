message_ids = ['194692cf94443f1b', '194692a95d6a8429', '19469289dccd11a5', '194691d515420026', '194691b6dd231775', '194691b446dc450e', '1946919f3b73e3d7', '1946919874c8a9f6', '1946918f5540ccfe', '19469189b4e4284a', '194690fcb8d707c8', '194690b7bccabefe', '19468cb56e4c4a57', '194687b84ab130b0', '19468309d9a0a15f', '1946717aac925cc9', '19466fc2c0f379aa', '194665038cfa6693', '19466207cb461983', '1946607160e7328c', '1946559399347c7a', '19464dbf33de43c8', '19464c0119556574', '1946485b732631de', '1946438ce63080fe', '19463d52616f99e7', '19463d16765abf5c', '19463774f8ac07f1', '194632e579ed0435', '194632c2f3994984', '19463288e1f29e02', '194630c7214a26b5', '194629eaadddd8dd', '19461b6f15032701', '19461b3191a37023', '19461a8b06ed9e6c', '19460c03f9495f8c', '19460aeec583683f', '194609272cbb0d53', '19460153b6bf1996', '1945ff973df1093c', '1945ff8113b88378', '1945fec084053655', '1945fc2c79ae69ae', '1945f12bfd141bbf', '1945eba674379b6a', '1945e251af5960cc', '1945e18154416bc8', '1945df64376e540e', '1945de10e941f637', '1945db61a2a92c41', '1945c95e06fd064c', '1945c905f3bf6923', '1945c8dfc9f878d9', '1945bee02f5dfc63', '1945bed99f005102', '1945b7a365902d1e', '1945b4c627258858', '1945b106196b66e6', '19459884665bd5ef', '19459881ae8df220', '194593c6c75cbd00', '194584d54a2833c5', '194576c79d0bc1e0', '19456b8b55b73168', '19456b61ec534f27', '19456b5d6e902733', '19456b32cba7fe3a', '19456aa17022cf13', '1945697d1bbbdf08', '1945682950452187', '1945657f51e572e7', '1945645b3e6d1d74', '194561ca4a0dc85f', '19455e4ada882c10', '194559cf5d3bb2e5', '1945470a0047dd81', '19453f7e5f517d83', '1945355f472628ba', '194533e040f58bd8', '19452eff84d8fb86', '1945246f3814d55e', '19451e2408356af3', '19451e0c376086c3', '19451d80a3e92c0a', '194517eed8d75949', '194515db2411d481', '1945109c22227d2c', '19450fef1048cf23', '19450bafa3b991db', '1944fd5b392176fd', '1944fc1b1a6a5d91', '1944faa04dac9b57', '1944f881c6881386', '1944f865bc2d2b5e', '1944f86312600d42', '1944f861ff88ce82', '1944f7e075188100', '1944f785e349396c', '1944f595b737e00e']
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest

# Path to your credentials.json file
CREDENTIALS_FILE = 'credentials.json'  # Replace with your actual file path
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # Adjust scopes as needed

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
# # Authenticate and get credentials
# flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
# credentials = flow.run_local_server(port=0)

# Build the Gmail API service
service = build('gmail', 'v1', credentials=creds)

# List of message IDs
with open("messageIdList.json", "r") as file:
    message_ids = json.load(file)
    
message_ids = message_ids[0:95]
messages = []
# Callback function to process responses
def message_callback(request_id, response, exception):
    if exception is not None:
        print(f"An error occurred for request {request_id}: {exception}")
    else:
        messages.append(response)

# Create a BatchHttpRequest object with the correct batch URI for Gmail API
batch = BatchHttpRequest(callback=message_callback, batch_uri='https://gmail.googleapis.com/batch')

# Add each message request to the batch
for message_id in message_ids:
    request = service.users().messages().get(userId='me', id=message_id, format='full')
    batch.add(request)

# Execute the batch request
batch.execute()

with open("message.json", "w") as file:
    json.dump(messages, file, indent=4)