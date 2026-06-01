from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.ai.orchestrator import get_orchestrator
from src.services.telegram import TelegramService

router = Router()



@router.message(CommandStart())
async def command_start(message: Message, db):
    parts = message.text.split()
    code = parts[1]

    tg_id = message.from_user.id

    await TelegramService(db).add_tg_user(code, tg_id)


@router.message()
async def handle_message(message: Message):
    tg_id = message.from_user.id
    text = message.text

    orchestrator = get_orchestrator(tg_id)
    response = await orchestrator.ask(text)

    await message.answer(response)