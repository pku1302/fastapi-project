from app.schemas.user_signup_schema import UserSignup
from app.models.user import User
from app.security.security import get_password_hash
from sqlmodel import select

class UserAlreadyExists(Exception):
    pass

class EmailAlreadyExists(Exception):
    pass

def signup_user(session, data: UserSignup) -> User:
    if session.get(User, data.id):
        raise UserAlreadyExists
    
    if data.email is not None:
        user = session.exec(
            select(User).where(User.email == data.email)
        ).first()
    
        if user is not None:
            raise EmailAlreadyExists
    
    user = User(
        id=data.id,
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )

    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user