from fastapi import APIRouter

router = APIRouter()

@router.get("/profile")
def get_profile():
    return {"message": "agent profile: TODO"}

@router.put("/profile")
def update_profile():
    return {"message": "update profile: TODO"}

@router.post("/verification")
def submit_verification():
    return {"message": "submit verification: TODO"}

@router.get("/verification/status")
def verification_status():
    return {"message": "verification status: TODO"}
