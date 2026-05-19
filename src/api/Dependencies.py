from typing import Annotated
from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel
from src.database import async_session_maker
from src.models.user import Role
from src.services.auth import Auth
from src.utils.dbmanager import DBManager


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Access Token is required")
    return token

def get_current_user(token: str = Depends(get_token)):
    data = Auth().decode_token(token)
    return data["user_id"]

async def get_user_by_id(user_id: int = Depends(get_current_user)):
    async with DBManager(session_factory=async_session_maker) as db:
        return await db.user.get_filter_by(id=user_id)

def get_role(role: Role):
    def checker(user = Depends(get_user_by_id)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
        return user
    return checker

UserIDDep = Annotated[int, Depends(get_current_user)]


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
