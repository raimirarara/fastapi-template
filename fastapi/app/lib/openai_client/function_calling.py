import asyncio
import json
import os
import logging
from pyexpat import model
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI
import time

logger = logging.getLogger()

# azure_client = AsyncAzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
# )
# deployment_id = os.getenv("AZURE_DEPLOYMENT_ID")
# host = os.getenv("AZURE_OPENAI_API_HOST")

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_info",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock symbol (4-character alphanumeric code) followed by a slash and the exchange code (e.g., '6501/T')",
                    }
                },
                "required": ["symbol"],
            },
            "description": "Get the current stock info for a domestic stock. The stock symbol must be a 4-character alphanumeric code followed by a slash and an exchange code. The exchange codes are as follows:\n- T: Tokyo Stock Exchange\n- M: Nagoya Stock Exchange\n- FK: Fukuoka Stock Exchange\n- S: Sapporo Stock Exchange\n\nFor example, '6501/T' represents the stock symbol '6501' on the Tokyo Stock Exchange. The stock symbol should consist of half-width numbers or half-width uppercase letters.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_domestic_key_indicators",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Comma-separated list of domestic key indicator symbols (3-character alphanumeric codes), up to a maximum of 5 indicators",
                    }
                },
                "required": ["symbol"],
            },
            "description": "Get the current domestic key indicators. Specify the indicator codes for domestic key indicators. Multiple indicators can be specified by separating them with commas (','), up to a maximum of 5 indicator codes, such as '101,101.1,151,179,178'.",
        },
    },
]


async def call_function_calling(content: str):
    messages = [
        {"role": "user", "content": content},
    ]
    model_type = os.getenv("LLM_MODEL_TYPE")
    if model_type == "openai":
        logger.info("Using OpenAI API")
        response = await openai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=messages,
            tools=tools,
        )
    else:
        logger.info("Using Azure API")
        # response = await azure_client.chat.completions.create(
        #     model=deployment_id,
        #     messages=messages,
        #     tools=tools,
        # )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            logger.info(f"Function name: {function_name}")
            function_args = json.loads(tool_call.function.arguments)
            symbol: str = function_args.get("symbol")
            logger.info(f"Symbol: {symbol}")
            return {
                "function_name": function_name,
                "symbol": symbol,
            }
    return ""
