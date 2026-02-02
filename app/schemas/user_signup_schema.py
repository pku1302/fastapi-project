from sqlmodel import SQLModel
from pydantic import Field, EmailStr
from datetime import datetime

class UserSignup(SQLModel):
    id: str = Field(
        min_length=4,
        max_length=20,
        pattern=r"^[a-z0-9_]+$"
    )

    password: str = Field(
        min_length=8,
        max_length=64
    )

    email: EmailStr | None = None

class UserResponse(SQLModel):
    id: str
    email: str | None
    created_at: datetime | None

