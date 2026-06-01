from datetime import timedelta, timezone, datetime
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from src.config import settings
from src.exceptions import ObjectNotFoundException, UserNotFoundException, IncorrectUserDataException
from src.models.user import Role
from src.repositories.utils import generate_code
from src.schemas.telegram_link import AddTelegramLink
from src.schemas.user import UserAddRequest, UserAdd
from src.services.base import BaseService


class Auth(BaseService):
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
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Credentials expired")
        return tok

    async def add_user(self, data: UserAddRequest):
        hashed_password = self.get_password_hash(data.password)
        new_user = UserAdd(email=data.email, hashed_password=hashed_password, role=Role.USER)
        await self.db.user.add(new_user)
        await self.db.commit()

    async def login_user(self, data: UserAddRequest):
        try:
            user = await self.db.user.get_user_by_email(email=data.email)
        except ObjectNotFoundException:
            raise UserNotFoundException
        if not self.verify_password(plain_password=data.password, hashed_password=user.hashed_password):
            raise IncorrectUserDataException
        return self.create_access_token({"user_id": user.id})

    async def telegram_link(self, user: int):
        code = generate_code()
        data = AddTelegramLink(code=code, user_id=user)
        await self.db.tg.add(data)
        await self.db.commit()
        return code