import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Request, Depends, HTTPException, status
from passlib.context import CryptContext
from main.db import get_session
from config import settings

sha512_hash = CryptContext(schemes=["sha512_crypt"])
useradmin = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="useradmin/token")


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    key = settings.SECRET_KEY
    data = jwt.decode(token, key, algorithms="HS256")
    user = data["data"]

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
