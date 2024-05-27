import asyncio
import json
import os
import logging
from pyexpat import model
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI


logger = logging.getLogger()

# azure_client = AsyncAzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
# )
# deployment_id = os.getenv("AZURE_DEPLOYMENT_ID")
# host = os.getenv("AZURE_OPENAI_API_HOST")


openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def call_chat_completion(prompt: str, content: str):
    logger.info("start chat completion")
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": content}]
    model_type = os.getenv("LLM_MODEL_TYPE")
    if model_type == "openai":
        logger.info("Using OpenAI API")
        chat_response = await openai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=messages,
        )
    else:
        logger.info("Using Azure API")
    #     chat_response = await azure_client.chat.completions.create(
    #         model=deployment_id,
    #         messages=messages,
    #     )  # get a new response from the model where it can see the function response
    if chat_response.choices[0].message.content:
        return chat_response.choices[0].message.content
    else:
        return "I'm sorry, I don't understand."
