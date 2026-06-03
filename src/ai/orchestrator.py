import json
from src.init import redis_conn as r
from src.ai.ai_client import client
from src.ai.registry import TOOLS_MAP
from src.ai.tools_schema import BOOK_TOOLS


SYSTEM_PROMPT = """
YOU ARE LIBRARY ASSISTANT. USE TOOLS WHEN NEEDED
"""

class AIOrchestrator:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.key = f"chat:{tg_id}"

    async def get_messages(self) -> list:
        data = await r.get(self.key)
        if not data:
            return [{"role": "system", "content": SYSTEM_PROMPT}]
        return json.loads(data)

    async def save_messages(self, messages: list):
        await r.set(self.key, json.dumps(messages, ensure_ascii=False), ex=60*60*24)

    async def ask(self, text: str):
        messages = await self.get_messages()
        messages.append({"role": "user", "content": text})

        while True:
            response = await client.chat.completions.create(
                model="z-ai/glm-4.5-air:free",
                messages=messages,
                tools=BOOK_TOOLS,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if not message.tool_calls:
                messages.append({"role": "assistant", "content": message.content})
                await self.save_messages(messages)
                return message.content

            messages.append(message.model_dump())

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if function_name == "get_loans":
                    try:
                        result = await TOOLS_MAP[function_name](tg_id=self.tg_id, **arguments)
                    except Exception as e:
                        result = {"error": str(e)}
                else:
                    try:
                        result = await TOOLS_MAP[function_name](**arguments)
                    except Exception as e:
                        result = {"error": str(e)}

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

def get_orchestrator(tg_id: int) -> AIOrchestrator:
    return AIOrchestrator(tg_id)