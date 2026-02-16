from fastapi import APIRouter

router = APIRouter()

@router.get("/verification-requests")
def list_verification_requests():
    return {"message": "admin list verification requests: TODO"}

@router.post("/verification-requests/{request_id}/approve")
def approve_verification(request_id: str):
    return {"message": f"approve {request_id}: TODO"}

@router.post("/verification-requests/{request_id}/reject")
def reject_verification(request_id: str):
    return {"message": f"reject {request_id}: TODO"}
