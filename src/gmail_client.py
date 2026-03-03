import base64
import mimetypes
import os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from .auth import get_credentials


class GmailClient:
    def __init__(self):
        creds = get_credentials()
        self.service = build("gmail", "v1", credentials=creds)

    def list_labels(self) -> list[dict]:
        """List all Gmail labels."""
        results = self.service.users().labels().list(userId="me").execute()
        return results.get("labels", [])

    def search_messages(self, query: str, max_results: int = 10) -> list[dict]:
        """Search messages using Gmail query syntax (e.g. 'from:user@example.com has:attachment')."""
        results = (
            self.service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        return results.get("messages", [])

    def get_message(self, message_id: str) -> dict:
        """Get a full message by ID, including headers and body."""
        msg = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
        body = self._extract_body(msg["payload"])
        return {
            "id": msg["id"],
            "threadId": msg["threadId"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
            "body": body,
            "labelIds": msg.get("labelIds", []),
        }

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: list[str] | None = None,
    ) -> dict:
        """Send an email, optionally with file attachments.

        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Plain text body.
            attachments: List of file paths to attach.
        """
        if attachments:
            message = MIMEMultipart()
            message.attach(MIMEText(body, "plain"))
            for file_path in attachments:
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = "application/octet-stream"
                main_type, sub_type = content_type.split("/", 1)
                with open(file_path, "rb") as f:
                    attachment = MIMEBase(main_type, sub_type)
                    attachment.set_payload(f.read())
                attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(file_path),
                )
                message.attach(attachment)
        else:
            message = MIMEText(body, "plain")

        message["to"] = to
        message["subject"] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": raw})
            .execute()
        )

    def download_attachments(self, message_id: str, save_dir: str) -> list[str]:
        """Download all attachments from a message to save_dir. Returns list of saved file paths."""
        os.makedirs(save_dir, exist_ok=True)
        msg = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        saved = []
        for part in self._get_attachment_parts(msg["payload"]):
            filename = part.get("filename", "attachment")
            att_id = part["body"]["attachmentId"]
            att = (
                self.service.users()
                .messages()
                .attachments()
                .get(userId="me", messageId=message_id, id=att_id)
                .execute()
            )
            data = base64.urlsafe_b64decode(att["data"])
            path = os.path.join(save_dir, filename)
            with open(path, "wb") as f:
                f.write(data)
            saved.append(path)
        return saved

    def _extract_body(self, payload: dict) -> str:
        """Extract plain text body from message payload."""
        if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
        for part in payload.get("parts", []):
            result = self._extract_body(part)
            if result:
                return result
        return ""

    def _get_attachment_parts(self, payload: dict) -> list[dict]:
        """Recursively find all parts that have attachments."""
        parts = []
        if payload.get("filename") and payload.get("body", {}).get("attachmentId"):
            parts.append(payload)
        for part in payload.get("parts", []):
            parts.extend(self._get_attachment_parts(part))
        return parts
