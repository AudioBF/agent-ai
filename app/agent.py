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
            "description": "Check the math expression and calculate the result. Use for any math expression, calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to calculate. For example: 2 + 2, sqrt(144), log(100, 10), (10*3)/2"
                    }
                },
                "required": ["expression"]
            },
        },
    }
]

def calculate(expression: str) -> str:
    """Calculate the result of a math expression."""
    try:
       import sympy
       result = sympy.sympify(expression)       
       return str(result)
    except Exception as e:
        logger.warning(f"Error calculating expression '{expression}': {e}")
        return f"Error calculating expression."
    
TOOL_MAP = {
    "calculate": calculate,

}

def run_agent(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can perform calculations using the provided tools. Use the tools when necessary to answer user questions.",
        },
        {
            "role": "user",
            "content": user_message
        },
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