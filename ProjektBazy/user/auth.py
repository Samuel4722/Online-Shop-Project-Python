from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from .model import User

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LEN = 72

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = await User.filter(login=credentials.username).first()
    if not user or not pwd_context.verify(credentials.password[:MAX_BCRYPT_LEN], user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowe dane logowania",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

async def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak uprawnień administratora"
        )
    return user
