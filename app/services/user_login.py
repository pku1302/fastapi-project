from app.models.user import User
from app.security.security import verify_password

def authenticate_user(session, userid: str, password: str):
    user = session.get(User, userid)

    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

