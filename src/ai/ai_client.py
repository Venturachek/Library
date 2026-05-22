from openai import AsyncOpenAI

from src.config import settings

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=settings.AI_API_KEY,
)

