from math import e
import requests
import logging
import json

logger = logging.getLogger()


def get_domestic_key_indicators(symbol: str):
    try:
        if len(symbol) != 3 or not symbol.isalnum():
            logger.warning(f"Invalid symbol format: {symbol}. Symbol must be a 3-character alphanumeric code.")
            return None
        logger.info(f"Getting get_domestic_key_indicators for {symbol}")
        url = "https://ut003.qhit.net/rdemo/qdata_api/c5118c1d2256ed6d85351f532feb127b16f1e54012daa35d11808823f240a764/quickdata.aspx"
        params = {"F": "ja_mkt_idx_lst", "callback": "", "quote": symbol}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            # レスポンスボディからJavaScriptコードを取得
            # JSONデータを解析
            data = response.json()
            logger.info(f"Data: {data}")

            stock_data_json = data["section1"]["data"][symbol]
            stock_data = json.dumps(stock_data_json, ensure_ascii=False)
            return stock_data
        else:
            print("リクエストが失敗しました。ステータスコード:", response.status_code)
            return None
    except Exception:
        logger.error(f"Failed to get_domestic_key_indicators data: {e}")
        return None
