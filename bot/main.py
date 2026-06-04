import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher


sys.path.append(str(Path(__file__).parent.parent))
from src.init import redis_conn
from src.database import async_session_maker
from src.config import settings

from bot.app.handlers import router
from bot.middleware import DbMiddleware


bot = Bot(token=settings.TG_ACCESS_TOKEN)
dp = Dispatcher()

dp.update.middleware(DbMiddleware(session_factory=async_session_maker))

async def main():
    dp.include_router(router)
    await redis_conn.connect()
    try:
        await dp.start_polling(bot)
    finally:
        await redis_conn.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
