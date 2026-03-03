"""Gmail API usage examples."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gmail_client import GmailClient


def main():
    client = GmailClient()

    # List labels
    print("=== Labels ===")
    for label in client.list_labels():
        print(f"  {label['name']} ({label['id']})")

    # Search recent messages
    print("\n=== Recent messages ===")
    messages = client.search_messages("newer_than:7d", max_results=5)
    for msg_stub in messages:
        msg = client.get_message(msg_stub["id"])
        print(f"  From: {msg['from']}")
        print(f"  Subject: {msg['subject']}")
        print(f"  Date: {msg['date']}")
        print()

    # Download attachments from first message that has them
    print("=== Searching for messages with attachments ===")
    with_att = client.search_messages("has:attachment newer_than:30d", max_results=1)
    if with_att:
        msg_id = with_att[0]["id"]
        saved = client.download_attachments(msg_id, save_dir="./downloads")
        print(f"  Saved {len(saved)} attachment(s): {saved}")
    else:
        print("  No messages with attachments found in the last 30 days.")


if __name__ == "__main__":
    main()
