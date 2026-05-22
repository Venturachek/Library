import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher


sys.path.append(str(Path(__file__).parent.parent))

from bot.handlers import router
from src.config import settings

bot = Bot(token=settings.TG_ACCESS_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
