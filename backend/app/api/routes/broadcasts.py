from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_broadcasts():
    return {"message": "list broadcasts: TODO"}

@router.post("")
def create_broadcast():
    return {"message": "create broadcast: TODO"}

@router.get("/{broadcast_id}")
def get_broadcast(broadcast_id: str):
    return {"message": f"get broadcast {broadcast_id}: TODO"}

@router.post("/{broadcast_id}/responses")
def respond_broadcast(broadcast_id: str):
    return {"message": f"respond broadcast {broadcast_id}: TODO"}
