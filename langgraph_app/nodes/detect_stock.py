import json
import os
import re
from typing import List, Optional

# 新的資料路徑，指向 ai-chatbot-proxy/data/stock_alias_dict.json
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/stock_alias_dict.json')

# 載入 stock alias dict 並建立 alias -> stock_id 的反查表
with open(DATA_PATH, encoding='utf-8') as f:
    stock_dict = json.load(f)

alias_to_id = {}
for stock_id, aliases in stock_dict.items():
    for alias in aliases:
        alias_to_id[alias] = stock_id

def detect_stock(text: str) -> Optional[str]:
    """
    輸入一句話，回傳偵測到的 stock id（若無則回傳 None）
    保持向後相容性
    """
    stocks = detect_stocks(text)
    return stocks[0] if stocks else None

def detect_stocks(text: str) -> List[str]:
    """
    輸入一句話，回傳偵測到的所有 stock id 列表
    """
    detected_stocks = []
    
    # 先檢查是否有數字格式的股票代號 (4位數字)
    stock_codes = re.findall(r'\b\d{4}\b', text)
    for code in stock_codes:
        if code in stock_dict:
            detected_stocks.append(code)
    
    # 再檢查別名
    for alias, stock_id in alias_to_id.items():
        if alias in text and stock_id not in detected_stocks:
            detected_stocks.append(stock_id)
    
    return detected_stocks

# 測試用
if __name__ == "__main__":
    test_cases = [
        "我想查台積電的技術線圖",
        "請給我2330的法人買賣超",
        "亞泥最近怎麼樣？",
        "請查詢1301的新聞",
        "台積電和聯發科哪個比較好？",
        "2330、2454、2317這三檔股票"
    ]
    for case in test_cases:
        stocks = detect_stocks(case)
        print(f"輸入: {case} -> 偵測: {stocks}") 