import io
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .auth import get_credentials


class DriveClient:
    def __init__(self):
        creds = get_credentials()
        self.service = build("drive", "v3", credentials=creds)

    def list_files(self, query: str | None = None, page_size: int = 10) -> list[dict]:
        """List files in Drive. Optionally filter with a query (Drive query syntax).

        Examples:
            query="mimeType='application/pdf'"
            query="name contains 'report'"
            query="'<folder_id>' in parents"
        """
        params = {
            "pageSize": page_size,
            "fields": "files(id, name, mimeType, size, modifiedTime, parents)",
        }
        if query:
            params["q"] = query
        results = self.service.files().list(**params).execute()
        return results.get("files", [])

    def download_file(self, file_id: str, save_path: str) -> str:
        """Download a file by ID to a local path. Returns the save path."""
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        request = self.service.files().get_media(fileId=file_id)
        with open(save_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        return save_path

    def upload_file(
        self,
        file_path: str,
        folder_id: str | None = None,
        mime_type: str | None = None,
    ) -> dict:
        """Upload a local file to Drive. Optionally specify a target folder.

        Returns the created file metadata (id, name, etc.).
        """
        file_name = os.path.basename(file_path)
        metadata = {"name": file_name}
        if folder_id:
            metadata["parents"] = [folder_id]

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        created = (
            self.service.files()
            .create(body=metadata, media_body=media, fields="id, name, mimeType, size")
            .execute()
        )
        return created

    def create_folder(self, name: str, parent_id: str | None = None) -> dict:
        """Create a folder in Drive. Returns the created folder metadata."""
        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            metadata["parents"] = [parent_id]

        folder = (
            self.service.files()
            .create(body=metadata, fields="id, name")
            .execute()
        )
        return folder

    def export_google_doc(self, file_id: str, mime_type: str, save_path: str) -> str:
        """Export a Google Workspace file (Docs, Sheets, Slides) to a given format.

        Args:
            file_id: The Google file ID.
            mime_type: Export format, e.g.:
                - "application/pdf"
                - "text/csv" (Sheets)
                - "application/vnd.openxmlformats-officedocument.wordprocessingml.document" (Docs -> docx)
            save_path: Local path to save the exported file.
        """
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        request = self.service.files().export_media(fileId=file_id, mimeType=mime_type)
        with open(save_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        return save_path
