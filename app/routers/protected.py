from fastapi import APIRouter, Depends
from app.models.user import User
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/protected")

@router.get("/")
def protected(
    user: User = Depends(get_current_user)
):
    return {"user_id": user.id}