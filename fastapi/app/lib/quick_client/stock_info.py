import requests
import logging
import json
import re

logger = logging.getLogger()


def get_stock_info(symbol: str):
    try:
        logger.info(f"Getting stock info for {symbol}")
        if not re.match(r"^[A-Z0-9]{4}/[TFKSM]$", symbol):
            logger.warning(
                f"Invalid symbol format: {symbol}. Symbol must be a 4-character alphanumeric code followed by /T, /FK, /S, or /M."
            )
            return None

        url = "https://ut003.qhit.net/rdemo/qdata_api/c5118c1d2256ed6d85351f532feb127b16f1e54012daa35d11808823f240a764/quickdata.aspx"
        params = {"F": "ja_stk_dtl_base", "callback": "", "quote": symbol}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Data: {data}")

            stock_data_json = data["section1"]["data"][symbol]
            stock_data = json.dumps(stock_data_json, ensure_ascii=False)
            return stock_data
        else:
            print("リクエストが失敗しました。ステータスコード:", response.status_code)
            return None
    except Exception as e:
        logger.error(f"Failed to get_stock_info data: {e}")
        return None
