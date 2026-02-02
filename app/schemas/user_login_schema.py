from sqlmodel import SQLModel


class LoginRequest(SQLModel):
    id: str
    password: str

class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    