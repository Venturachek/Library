from aiogram import BaseMiddleware
from src.utils.dbmanager import DBManager


class DbMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with DBManager(session_factory=self.session_factory) as db:
            data["db"] = db
            return await handler(event, data)