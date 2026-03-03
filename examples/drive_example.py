"""Google Drive API usage examples."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drive_client import DriveClient


def main():
    client = DriveClient()

    # List files
    print("=== Recent Drive files ===")
    files = client.list_files(page_size=10)
    for f in files:
        size = f.get("size", "N/A")
        print(f"  {f['name']}  (type: {f['mimeType']}, size: {size}, id: {f['id']})")

    # Create a folder
    print("\n=== Creating a test folder ===")
    folder = client.create_folder("test-api-folder")
    print(f"  Created folder: {folder['name']} (id: {folder['id']})")

    # Upload a file to that folder
    # Uncomment to test:
    # print("\n=== Uploading a file ===")
    # result = client.upload_file("./some-file.txt", folder_id=folder["id"])
    # print(f"  Uploaded: {result['name']} (id: {result['id']})")

    # Download a file
    # Uncomment and set a file_id to test:
    # print("\n=== Downloading a file ===")
    # path = client.download_file("<file_id>", "./downloads/myfile.pdf")
    # print(f"  Downloaded to: {path}")


if __name__ == "__main__":
    main()
