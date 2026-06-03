from functools import wraps

from src.database import async_session_maker
from src.utils.dbmanager import DBManager


def db_dec(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with DBManager(session_factory=async_session_maker) as db:
            return await func(self, *args, db=db, **kwargs)
    return wrapper
