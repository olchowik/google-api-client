"""Gmail API usage examples using direct service calls."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import connect

gmail, drive = connect()

# List labels
print("=== Labels ===")
results = gmail.users().labels().list(userId="me").execute()
for label in results.get("labels", []):
    print(f"  {label['name']}")

# Search recent messages
print("\n=== Recent messages ===")
results = gmail.users().messages().list(userId="me", q="newer_than:3d", maxResults=5).execute()
for msg_stub in results.get("messages", []):
    msg = gmail.users().messages().get(userId="me", id=msg_stub["id"], format="metadata").execute()
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    print(f"  From: {headers.get('From', '')}")
    print(f"  Subject: {headers.get('Subject', '')}")
    print()

# Create a label
# gmail.users().labels().create(userId="me", body={"name": "MyNewLabel"}).execute()

# Trash a message
# gmail.users().messages().trash(userId="me", id="<message_id>").execute()
