import json
import logging
import litellm
from app.config import settings
from app.tools.calculator import calculate
from app.tools.countries import get_country_info

logger = logging.getLogger(__name__)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a mathematical expression and returns the result. Use for any numerical calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '2 + 2', 'sqrt(144)', '10 ** 2'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_country_info",
            "description": "Fetches information about a country: capital, population, area, currency and language. Use for any question about a specific country.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Country name in English, e.g. 'Brazil', 'Japan', 'Germany'",
                    }
                },
                "required": ["country"],
            },
        },
    },
]

TOOL_MAP = {
    "calculate": calculate,
    "get_country_info": get_country_info,
}


def run_agent(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Always respond in the same language the user writes in.",
        },
        {"role": "user", "content": user_message},
    ]

    while True:
        response = litellm.completion(
            model="groq/llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False,
            api_key=settings.groq_api_key,
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                logger.info(f"Tool called: {tool_name} | args: {tool_args}")

                tool_fn = TOOL_MAP.get(tool_name)
                if tool_fn:
                    result = tool_fn(**tool_args)
                else:
                    result = f"Tool '{tool_name}' not found."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            return message.content