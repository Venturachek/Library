from datetime import timedelta, timezone, datetime
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.config import  settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            tok = jwt.decode(token, settings.JWT_KEY, algorithms=settings.ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return tok
        
