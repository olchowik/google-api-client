"""Google Drive API usage examples using direct service calls."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import connect

gmail, drive = connect()

# List files
print("=== Recent Drive files ===")
results = drive.files().list(pageSize=10, fields="files(id, name, mimeType, size)").execute()
for f in results.get("files", []):
    print(f"  {f['name']}  (type: {f['mimeType']}, size: {f.get('size', 'N/A')})")

# Create a folder
# drive.files().create(body={"name": "MyFolder", "mimeType": "application/vnd.google-apps.folder"}).execute()

# Upload a file
# from googleapiclient.http import MediaFileUpload
# media = MediaFileUpload("./myfile.pdf", resumable=True)
# drive.files().create(body={"name": "myfile.pdf"}, media_body=media).execute()

# Download a file
# from googleapiclient.http import MediaIoBaseDownload
# request = drive.files().get_media(fileId="<file_id>")
# with open("./downloaded.pdf", "wb") as f:
#     downloader = MediaIoBaseDownload(f, request)
#     done = False
#     while not done:
#         _, done = downloader.next_chunk()
