from __future__ import print_function

import base64
import os
from email.mime.text import MIMEText

from apiclient import errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

creds = None

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    """Send an email message.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def service_account_login():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    global creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if creds is None and os.path.exists('keys.json'):
        creds = Credentials.from_authorized_user_file('keys.json', SCOPES)
    if not creds:
        info = {
            "token": os.environ.get('GMAIL_TOKEN'),
            "refresh_token": os.environ.get('GMAIL_REFRESH_TOKEN'),
            "client_id": os.environ.get('GMAIL_CLIENT_ID'),
            "client_secret": os.environ.get('GMAIL_CLIENT_SECRET'),
            "token_uri": "https://oauth2.googleapis.com/token",
            "scopes": SCOPES,
            "expiry":  os.environ.get('GMAIL_TOKEN_EXPIRY')
        }
        creds = Credentials.from_authorized_user_info(info, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("creds present but expired, refreshing")
            creds.refresh(Request())

        #TODO ante credenciales no validas?

        #else:
        #flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        #creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        #file write doesn't work on vercel, so we use global object
        #with open('keys.json', 'w') as token:
        #    token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service
