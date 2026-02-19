import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


def save_upload(file: UploadFile, subdir: str = "licenses") -> str:
    """
    Saves uploaded file to local disk and returns a public-ish URL path (MVP).
    In production: replace with S3/GCS and return real URL.
    """
    base = Path(settings.UPLOAD_DIR) / subdir
    os.makedirs(base, exist_ok=True)

    ext = Path(file.filename or "").suffix.lower()
    safe_ext = ext if ext in [".pdf", ".png", ".jpg", ".jpeg"] else ""

    filename = f"{uuid.uuid4().hex}{safe_ext}"
    full_path = base / filename

    with open(full_path, "wb") as f:
        f.write(file.file.read())

    # Return relative path; API can later serve it or store S3 URL
    return str(full_path)
