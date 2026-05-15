from pydantic import BaseModel, EmailStr, Field, ConfigDict
from src.models.user import Role


class UserAddRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    role: Role

class User(BaseModel):
    id: int
    email: EmailStr
    role: Role
    model_config = ConfigDict(from_attributes=True)

class UserHashedPassword(User):
    hashed_password: str

class UserRole(BaseModel):
    role: Role