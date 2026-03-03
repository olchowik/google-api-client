# Google API Client

Python client for Gmail and Google Drive APIs. Search and read emails, send messages with attachments, download email attachments, and manage files on Google Drive.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select an existing one)
3. Navigate to **APIs & Services > Library** and enable:
   - **Gmail API**
   - **Google Drive API**
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > OAuth 2.0 Client ID**
6. Select **Desktop app** as the application type
7. Download the JSON file and save it as `credentials/credentials.json`

### 3. Authenticate

On the first run, a browser window will open for OAuth consent. After granting access, a token is cached in `credentials/token.json` and reused automatically.

## Usage

### Gmail

```python
from src.gmail_client import GmailClient

gmail = GmailClient()

# Search messages
messages = gmail.search_messages("from:user@example.com newer_than:7d")

# Read a message
msg = gmail.get_message(messages[0]["id"])
print(msg["subject"], msg["from"], msg["body"])

# Download attachments
gmail.download_attachments(messages[0]["id"], save_dir="./downloads")

# Send an email
gmail.send_message(
    to="recipient@example.com",
    subject="Hello",
    body="Message body here",
)

# Send with attachments
gmail.send_message(
    to="recipient@example.com",
    subject="Report",
    body="See attached.",
    attachments=["./report.pdf", "./data.csv"],
)

# List labels
labels = gmail.list_labels()
```

#### Gmail search query examples

| Query | Description |
|-------|-------------|
| `from:user@example.com` | Messages from a specific sender |
| `has:attachment` | Messages with attachments |
| `newer_than:7d` | Messages from the last 7 days |
| `subject:invoice` | Messages with "invoice" in the subject |
| `is:unread` | Unread messages |
| `label:INBOX` | Messages in inbox |

Full query syntax: [Gmail search operators](https://support.google.com/mail/answer/7190)

### Google Drive

```python
from src.drive_client import DriveClient

drive = DriveClient()

# List files
files = drive.list_files(page_size=10)
for f in files:
    print(f["name"], f["mimeType"], f["id"])

# Search files
pdfs = drive.list_files(query="mimeType='application/pdf'")
by_name = drive.list_files(query="name contains 'report'")

# Download a file
drive.download_file(file_id="<file_id>", save_path="./downloads/file.pdf")

# Upload a file
result = drive.upload_file("./report.pdf")
print(result["id"], result["name"])

# Upload to a specific folder
drive.upload_file("./report.pdf", folder_id="<folder_id>")

# Create a folder
folder = drive.create_folder("My Folder")
print(folder["id"])

# Export a Google Doc as PDF
drive.export_google_doc(
    file_id="<doc_id>",
    mime_type="application/pdf",
    save_path="./exports/document.pdf",
)
```

#### Export formats for Google Workspace files

| File type | mime_type |
|-----------|-----------|
| Google Docs → PDF | `application/pdf` |
| Google Docs → DOCX | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Google Sheets → CSV | `text/csv` |
| Google Sheets → XLSX | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Google Slides → PDF | `application/pdf` |
| Google Slides → PPTX | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |

## Running examples

```bash
python examples/gmail_example.py
python examples/drive_example.py
```

## Project structure

```
google-api-client/
├── credentials/          # OAuth credentials (gitignored)
├── src/
│   ├── auth.py           # Shared OAuth2 authentication
│   ├── gmail_client.py   # GmailClient class
│   └── drive_client.py   # DriveClient class
├── examples/
│   ├── gmail_example.py
│   └── drive_example.py
├── requirements.txt
└── .gitignore
```
