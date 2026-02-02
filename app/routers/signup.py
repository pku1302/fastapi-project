from fastapi import APIRouter, Query, HTTPException, Path
from app.schemas.user_signup_schema import UserResponse, UserSignup
from app.database.database import SessionDep
from app.services.user_signup import signup_user, UserAlreadyExists, EmailAlreadyExists

router = APIRouter(prefix="/signup", tags=["signup"])

@router.post("/", response_model=UserResponse)
def signup(data: UserSignup, session: SessionDep) -> UserResponse:
    try:
        user = signup_user(session, data)
        
    except UserAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="ID already exists"
        )
    except EmailAlreadyExists:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return user