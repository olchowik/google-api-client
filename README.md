# Google API Client

Lightweight Python authentication for Gmail and Google Drive APIs. Handles OAuth2 flow and token caching — then gives you direct access to the full API.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select an existing one)
3. Enable **Gmail API** and **Google Drive API**
4. Go to **Credentials > Create Credentials > OAuth 2.0 Client ID**
5. Select **Desktop app**, create, and download the JSON
6. Save it as `credentials/credentials.json`

### 3. First run

On the first run, a browser window opens for OAuth consent. After that, the token is cached automatically.

## Usage

```python
from src.auth import connect

gmail, drive = connect()
```

That's it. `gmail` and `drive` are standard Google API service objects with access to every method.

### Gmail examples

```python
# List labels
gmail.users().labels().list(userId="me").execute()

# Search messages
gmail.users().messages().list(userId="me", q="has:attachment newer_than:7d").execute()

# Get a message
gmail.users().messages().get(userId="me", id="<msg_id>", format="full").execute()

# Create a label (folder)
gmail.users().labels().create(userId="me", body={"name": "My Label"}).execute()

# Trash a message
gmail.users().messages().trash(userId="me", id="<msg_id>").execute()

# Download attachment
att = gmail.users().messages().attachments().get(
    userId="me", messageId="<msg_id>", id="<attachment_id>"
).execute()
```

Full reference: https://developers.google.com/gmail/api/reference/rest

### Drive examples

```python
# List files
drive.files().list(pageSize=10, fields="files(id, name, mimeType)").execute()

# Search files
drive.files().list(q="mimeType='application/pdf'", fields="files(id, name)").execute()

# Create a folder
drive.files().create(
    body={"name": "My Folder", "mimeType": "application/vnd.google-apps.folder"}
).execute()

# Upload a file
from googleapiclient.http import MediaFileUpload
media = MediaFileUpload("./report.pdf", resumable=True)
drive.files().create(body={"name": "report.pdf"}, media_body=media).execute()

# Download a file
from googleapiclient.http import MediaIoBaseDownload
request = drive.files().get_media(fileId="<file_id>")
with open("./file.pdf", "wb") as f:
    downloader = MediaIoBaseDownload(f, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

# Export Google Doc as PDF
request = drive.files().export_media(fileId="<doc_id>", mimeType="application/pdf")
```

Full reference: https://developers.google.com/drive/api/reference/rest/v3

## Project structure

```
google-api-client/
├── credentials/      # OAuth credentials (gitignored)
├── src/
│   └── auth.py       # OAuth2 auth + connect()
├── examples/
│   ├── gmail_example.py
│   └── drive_example.py
├── requirements.txt
└── .gitignore
```
