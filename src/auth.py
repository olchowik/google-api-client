import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_DIR = os.path.join(BASE_DIR, "credentials")
CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, "credentials.json")
TOKEN_FILE = os.path.join(CREDENTIALS_DIR, "token.json")


def get_credentials() -> Credentials:
    """Authenticate and return credentials for Gmail + Drive.

    On first run, opens a browser for OAuth consent.
    Subsequent runs use the cached token, refreshing if expired.
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                raise FileNotFoundError(
                    f"Missing {CLIENT_SECRET_FILE}. Download OAuth credentials "
                    "from Google Cloud Console and place them in the credentials/ folder."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds


def connect():
    """Authenticate and return Gmail and Drive service objects.

    Returns:
        (gmail, drive) tuple of authenticated API service objects.

    Usage:
        gmail, drive = connect()

        # Gmail - full API: https://developers.google.com/gmail/api/reference/rest
        gmail.users().labels().list(userId="me").execute()
        gmail.users().messages().list(userId="me", q="has:attachment").execute()
        gmail.users().labels().create(userId="me", body={"name": "My Label"}).execute()

        # Drive - full API: https://developers.google.com/drive/api/reference/rest/v3
        drive.files().list(pageSize=10).execute()
        drive.files().create(body={"name": "folder", "mimeType": "application/vnd.google-apps.folder"}).execute()
    """
    creds = get_credentials()
    gmail = build("gmail", "v1", credentials=creds)
    drive = build("drive", "v3", credentials=creds)
    return gmail, drive
