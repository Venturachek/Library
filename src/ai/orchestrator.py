import json

from src.ai.ai_client import client
from src.ai.registry import TOOLS_MAP
from src.ai.tools_schema import BOOK_TOOLS

SYSTEM_PROMPT = """
YOU ARE LIBRARY ASSISTANT. USE TOOLS WHEN NEEDED
"""

class AIOrchestrator:
    async def ask(self, text: str):
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ]
        response = await client.chat.completions.create(
            model="z-ai/glm-4.5-air:free",
            messages=messages,
            tools=BOOK_TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        result = await TOOLS_MAP[function_name](**arguments)

        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

        final_response = await client.chat.completions.create(
            model="z-ai/glm-4.5-air:free",
            messages=messages
        )
        return final_response.choices[0].message.content

orchestrator = AIOrchestrator()