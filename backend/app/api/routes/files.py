from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse

from app.core.auth_deps import require_admin
from app.core.config import settings
from app.models.user import User

router = APIRouter()


@router.get("/files")
def get_file(
    path: str = Query(..., description="Relative path inside UPLOAD_DIR, e.g. licenses/xxx.pdf"),
    admin: User = Depends(require_admin),
):
    """
    Admin-only: serves uploaded files from UPLOAD_DIR safely.
    Example: /admin/files?path=licenses/abc.pdf
    """
    base = Path(settings.UPLOAD_DIR).resolve()

    # Normalize provided path (must be relative)
    requested = Path(path)

    if requested.is_absolute():
        raise HTTPException(status_code=400, detail="Absolute paths are not allowed")

    full_path = (base / requested).resolve()

    # Prevent path traversal outside upload dir
    if base not in full_path.parents and full_path != base:
        raise HTTPException(status_code=403, detail="Access denied")

    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=str(full_path), filename=full_path.name)
