# auth.py
import os
from typing import Tuple
import json

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.auth.exceptions

import const

SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

def handle_exception(e: Exception) -> Tuple[None, int]:
    if isinstance(e, google.auth.exceptions.RefreshError):
        return const.handle_refresh_error(e)
    elif isinstance(e, google.auth.exceptions.TransportError):
        return const.handle_transport_error(e)
    elif isinstance(e, google.auth.exceptions.TimeoutError):
        return const.handle_timeout_error(e)
    elif isinstance(e, google.auth.exceptions.UserAccessTokenError):
        return const.handle_user_access_token_error(e)
    else:
        return const.unexpected_error(e)

def authenticate(user_email: str = None) -> Tuple[build, int]:
    # Path to the token file
    token_path = f'tokens/{user_email}_token.json' if user_email else 'token.json'
    creds = None

    # Create the tokens directory if it doesn't exist
    os.makedirs('tokens', exist_ok=True)

    # Load credentials if they exist
    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            token_data = json.load(token_file)
            try:
                creds = google.oauth2.credentials.Credentials.from_authorized_user_info(token_data)
            except Exception as e:
                return handle_exception(e)        

    # If there are no valid credentials, the user must authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                return handle_exception(e)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            try:
                creds = flow.run_local_server(
                    port=8080, 
                    authorization_prompt_message=const.AUTORIZATION_PROMPT_MESSAGE, 
                    authorization_code_message=const.AUTORIZATION_CODE_MESSAGE)
            except Exception as e:
                return handle_exception(e)

        # Save the credentials for future use
        try:
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
        except Exception as e:
            return handle_exception(e)

    # Build the Google Photos API service
    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    return service, None
