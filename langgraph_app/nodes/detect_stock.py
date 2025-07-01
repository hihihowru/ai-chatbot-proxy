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
    先做 alias 完全等於比對，再做包含比對。
    """
    lowered = text.strip().lower()
    # 完全等於優先
    for alias, stock_id in alias_to_id.items():
        if lowered == alias.lower():
            return stock_id
    # 再做包含
    for alias, stock_id in alias_to_id.items():
        if alias.lower() in lowered:
            return stock_id
    return None

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
    
    # 再檢查別名，優先匹配更長的別名
    matched_positions = []
    for alias, stock_id in sorted(alias_to_id.items(), key=lambda x: -len(x[0])):
        if alias in text and stock_id not in detected_stocks:
            # 記錄匹配位置，用於後續排序
            start_pos = text.find(alias)
            matched_positions.append((start_pos, len(alias), stock_id))
    
    # 按照匹配長度排序（長度優先），然後按照位置排序
    matched_positions.sort(key=lambda x: (-x[1], x[0]))
    
    # 添加排序後的股票代號，避免重複
    seen_stocks = set(detected_stocks)
    for _, _, stock_id in matched_positions:
        if stock_id not in seen_stocks:
            detected_stocks.append(stock_id)
            seen_stocks.add(stock_id)
    
    return detected_stocks

def get_stock_name_by_id(stock_id: str) -> Optional[str]:
    """
    根據股票代號回傳中文股名（取 stock_alias_dict.json 中該代號的第一個非數字 alias）
    """
    aliases = stock_dict.get(stock_id, [])
    for alias in aliases:
        if not alias.isdigit():
            return alias
    return None

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