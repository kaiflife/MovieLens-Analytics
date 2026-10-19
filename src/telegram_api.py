import json
import os
import urllib.error
import urllib.request
import uuid

from logger import setup_module_logger

logger = setup_module_logger("telegram_api")


def _build_multipart_body(fields: dict, file_field: str, file_path: str):
    """Helper to build multipart/form-data body for urllib."""
    boundary = uuid.uuid4().hex
    body = bytearray()

    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(f"{value}\r\n".encode())

    filename = os.path.basename(file_path)
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode()
    )
    body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
    with open(file_path, "rb") as f:
        body.extend(f.read())
    body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())
    return bytes(body), boundary


class TelegramNotifier:
    """Class for sending Telegram notifications."""

    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id

    def send_notification(self, success: bool) -> None:
        """Sends a text message to Telegram based on the success flag."""
        if success:
            text: str = "Привет, отчёт создан"
        else:
            text = "The report hasn't been created due to an error."

        url: str = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload: dict[str, str] = {"chat_id": self.chat_id, "text": text}
        data: bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )

        logger.info(f"Attempting to send Telegram notification (success={success})")

        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                logger.info("Bot successfully sent a message")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            logger.error(f"Telegram API Error {e.code}: {error_body}")
        except urllib.error.URLError as e:
            logger.error(f"Telegram notification failed: network error ({e.reason})")

    def send_document(self, file_path: str, caption: str = "") -> None:
        """Sends a file to Telegram."""
        url: str = f"https://api.telegram.org/bot{self.token}/sendDocument"
        fields = {"chat_id": self.chat_id, "caption": caption}
        body, boundary = _build_multipart_body(fields, "document", file_path)

        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )

        logger.info(f"Attempting to send document: {file_path}")

        try:
            with urllib.request.urlopen(req, timeout=30.0) as response:
                logger.info("Bot successfully sent the document")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            logger.error(f"Telegram API Error (sendDocument) {e.code}: {error_body}")
        except urllib.error.URLError as e:
            logger.error(f"Telegram document send failed: network error ({e.reason})")
