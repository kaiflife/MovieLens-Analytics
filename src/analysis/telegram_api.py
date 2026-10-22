import os
import urllib.error
import urllib.request
import uuid

import config
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

    def __init__(self) -> None:
        self.token = config.telegram_token
        self.chat_id = config.telegram_chat_id

    def send_document(self) -> None:
        """Sends a file to Telegram."""
        file_path = "src/movielens_report.ipynb"
        url: str = f"https://api.telegram.org/bot{self.token}/sendDocument"
        fields = {"chat_id": self.chat_id, "caption": "Отчёт группового проекта"}
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
