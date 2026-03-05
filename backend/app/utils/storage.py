import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def save_upload(file: UploadFile, subdir: str = "licenses") -> str:
    """
    Saves uploaded file to local disk and returns a RELATIVE path inside UPLOAD_DIR.
    Example return: "licenses/abc123.pdf"
    """
    base = Path(settings.UPLOAD_DIR) / subdir
    os.makedirs(base, exist_ok=True)

    ext = Path(file.filename or "").suffix.lower()
    safe_ext = ext if ext in ALLOWED_EXTENSIONS else ""

    filename = f"{uuid.uuid4().hex}{safe_ext}"
    full_path = base / filename

    with open(full_path, "wb") as f:
        f.write(file.file.read())

    # Return RELATIVE path (inside UPLOAD_DIR)
    return f"{subdir}/{filename}"
