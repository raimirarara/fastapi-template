import os
import sys
from datetime import datetime
import uuid
import random
import io
import time
import json


from fastapi import Body, Request, FastAPI, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse, RedirectResponse, StreamingResponse

import logging
import json

from pydantic import BaseModel

from lib.openai_client import call_function_calling
from lib.quick_client.domestic_key_indicators import get_domestic_key_indicators
from lib.openai_client.chat_completion import call_chat_completion
from lib.openai_client.system_prompt import create_chat_system_prompt
from .lib.quick_client.stock_info import get_stock_info


# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# ロガーを取得
logger = logging.getLogger()

logger.info("Starting FastAPI server")

app = FastAPI()


@app.get("/check")
async def check():
    return "OK"


@app.post("/chat")
async def chat(req: Request):
    body = await req.body()
    body = body.decode("utf-8")
    data = json.loads(body)  # JSON文字列をPythonの辞書に変換
    text = data.get("text", "おはよう")
    function_calling_result = await call_function_calling(text)
    stock_data = ""
    if function_calling_result:
        function_name = function_calling_result.get("function_name")
        symbol = function_calling_result.get("symbol")
        # 国内主要指標を取得
        if function_name == "get_domestic_key_indicators":
            if symbol:
                stock_data = get_domestic_key_indicators(symbol)
                if not stock_data:
                    return Response(content="銘柄が指定されていないか、存在しません。", media_type="text/plain")
        if function_name == "get_stock_info":
            if symbol:
                stock_data = get_stock_info(symbol)
                if not stock_data:
                    return Response(content="銘柄が指定されていないか、存在しません。", media_type="text/plain")

    chat_system_prompt = create_chat_system_prompt(stock_data)
    assistant_response = await call_chat_completion(chat_system_prompt, text)

    return Response(content=assistant_response, media_type="text/plain")
