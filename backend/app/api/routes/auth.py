from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.auth_service import register_user, authenticate_user
from app.core.jwt import create_access_token

router = APIRouter()


@router.post("/register")
def register(payload: dict, db: Session = Depends(get_db)):
    user = register_user(
        db=db,
        email=payload["email"],
        password=payload["password"],
        first_name=payload["first_name"],
        last_name=payload["last_name"],
    )

    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    user = authenticate_user(
        db=db,
        email=payload["email"],
        password=payload["password"],
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}
