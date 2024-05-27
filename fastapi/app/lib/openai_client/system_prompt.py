def create_chat_system_prompt(stock_data: str):
    return f"""あなたは、AIオペレーターです。以下の情報を元に、株価に関する質問に答えることができます。
{stock_data}"""
