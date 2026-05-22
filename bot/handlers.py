from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.ai.orchestrator import orchestrator

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer("Im your AI assistant")

@router.message()
async def message_to_ai(message: Message):
    answer = await orchestrator.ask(message.text)
    await message.answer(answer)
