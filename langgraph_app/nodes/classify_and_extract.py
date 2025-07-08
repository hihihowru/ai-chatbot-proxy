import openai
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from utils.token_tracker import track_openai_call

# 載入 stock alias dict
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/stock_alias_dict.json')
with open(DATA_PATH, encoding='utf-8') as f:
    stock_dict = json.load(f)

alias_to_id = {}
for stock_id, aliases in stock_dict.items():
    for alias in aliases:
        alias_to_id[alias] = stock_id

PROMPT = '''你是一個投資問題理解模組。

請針對以下提問，判斷：
1️⃣ 提問的目的（分析股價原因 / 基本面查詢 / 投資建議等）
2️⃣ 提取關鍵字（公司名稱、股票代號、時間、事件類型）
3️⃣ 投資面向（可複選：基本面、技術面、籌碼面、沒有特別）

📂 問題大分類（擇一）與其對應子分類（可複選）如下：

1. 個股分析  
　▸ 公司介紹  
　▸ 基本面分析（財務指標、營收獲利、產業地位等）
　▸ 籌碼面分析（法人動向、大戶散戶、股權分散等）
　▸ 技術面分析（K線、均線、技術指標、價量關係等）
　▸ 個股資訊查找（EPS、股價、營收、財報等單一指標查詢）
　▸ 價格評論（漲跌原因、建議買賣）

2. 選股建議  
　▸ 篩選條件選股  
　▸ 法人追蹤選股
    ▸ 籌碼追蹤選股  
　▸ 強勢股 / 起漲股 / 題材熱股

3. 盤勢分析  
　▸ 大盤走勢分析  
　▸ 類股輪動 / 熱門族群  
　▸ 產業
　▸ 國際股市
　▸ 美股
　▸ 期貨
　▸ 總經

4. 比較分析  
　▸ 個股比較  
　▸ 類股比較  
　▸ 同產業走勢比較

5. 金融知識詢問  
　▸ 制度說明  
　▸ 指標定義（如 RSI, 周轉率等）

6. 複雜查詢任務  
　▸ 多層條件查詢  
　▸ 結構化資料對照  
　▸ 模擬選股 / 假設回測問題

7. 無效問題（不需處理）  
　▸ 無明確投資內容  
　▸ 預測性問題（未來股價等）  
　▸ ChatGPT 自由發揮 / 幽默提問

請以 JSON 格式輸出：
{
  "category": "個股分析|選股建議|盤勢分析|比較分析|金融知識詢問|複雜查詢任務|無效問題",
  "subcategory": ["子分類1", "子分類2"],
  "view_type": ["基本面", "技術面", "籌碼面", "沒有特別"],
  "keywords": ["關鍵字1", "關鍵字2", "關鍵字3", "關鍵字4", "關鍵字5"],
  "company_name": "公司名稱",
  "stock_id": "股票代號",
  "time_info": "時間表達",
  "event_type": "漲停|跌停|上漲|下跌|財報|法說會|新聞|其他"
}

注意事項：
- keywords 請盡量提取 5 個相關關鍵字
- 包含：公司名稱、股票代號、時間詞、事件類型、產業相關詞、財務指標等
- 例如：["台積電", "2330", "財報", "營收", "獲利"]
- view_type 可複選，如果問題沒有特別偏向某個面向，請選擇 "沒有特別"
- 當問題是詢問單一指標（如"EPS多少？"、"股價多少？"）時，選擇"個股資訊查找"
- 當問題是綜合性分析（如"表現怎麼樣？"、"可以買嗎？"）時，根據內容選擇對應的分析面向

使用者問題：
{{ user_input }}
'''

def detect_stocks(text: str) -> List[str]:
    """偵測股票代號"""
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

def detect_time(question: str) -> str:
    """從問題中偵測時間表達"""
    time_patterns = {
        r'今天|今日|本日': 'today',
        r'昨天|昨日': 'yesterday', 
        r'明天|明日': 'tomorrow',
        r'前天': 'day_before_yesterday',
        r'上週|上周': 'last_week',
        r'本週|本周|這週|这周': 'this_week',
        r'下週|下周': 'next_week',
        r'上個月|上月': 'last_month',
        r'這個月|这個月|本月': 'this_month',
        r'下個月|下月': 'next_month',
        r'上季|上一季': 'last_quarter',
        r'本季|這一季|这一季': 'this_quarter',
        r'下季|下一季': 'next_quarter',
        r'去年': 'last_year',
        r'今年': 'this_year',
        r'明年': 'next_year',
        r'最近(\d+)天': 'recent_days',
        r'最近(\d+)週': 'recent_weeks',
        r'最近(\d+)個月': 'recent_months',
        r'最近(\d+)年': 'recent_years',
    }
    
    # 檢查每個時間模式
    for pattern, time_type in time_patterns.items():
        match = re.search(pattern, question)
        if match:
            if time_type.startswith('recent_'):
                number = int(match.group(1))
                return f"{time_type}_{number}"
            else:
                return time_type
    
    return "recent_5_days"

def classify_and_extract(user_input: str, model: str = "gpt-3.5-turbo") -> Dict:
    """
    整合的股票偵測、時間偵測和意圖分類
    """
    try:
        # 1. 偵測股票代號
        stock_ids = detect_stocks(user_input)
        stock_id = stock_ids[0] if stock_ids else ""
        
        # 2. 偵測時間
        time_info = detect_time(user_input)
        
        # 3. 使用 OpenAI 進行意圖分類和關鍵字提取
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = PROMPT.replace("{{ user_input }}", user_input)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        # 🔢 追蹤 token 使用量
        track_openai_call(
            node_name="classify_and_extract",
            response=response,
            user_input=user_input,
            stock_id=stock_id
        )
        
        # 解析 JSON 回應
        try:
            result = json.loads(response.choices[0].message.content.strip())
            
            # 添加調試信息
            print(f"🔍 DEBUG - OpenAI 原始回應: {response.choices[0].message.content.strip()}")
            print(f"🔍 DEBUG - 解析後的 result: {result}")
            print(f"🔍 DEBUG - keywords 長度: {len(result.get('keywords', []))}")
            
            # 補充股票代號資訊
            if stock_id and not result.get("stock_id"):
                result["stock_id"] = stock_id
            
            # 補充時間資訊
            if time_info and not result.get("time_info"):
                result["time_info"] = time_info
            
            return result
            
        except json.JSONDecodeError:
            # 如果 JSON 解析失敗，返回基本資訊
            return {
                "category": "個股分析",
                "subcategory": ["綜合分析"],
                "view_type": ["沒有特別"],
                "keywords": [],
                "company_name": "",
                "stock_id": stock_id,
                "time_info": time_info,
                "event_type": "其他"
            }
            
    except Exception as e:
        print(f"[classify_and_extract ERROR] {e}")
        # 🔢 記錄錯誤的 API 調用
        track_openai_call(
            node_name="classify_and_extract",
            response=None,
            user_input=user_input,
            stock_id=stock_id,
            success=False,
            error_message=str(e)
        )
        return {
            "category": "個股分析",
            "subcategory": ["綜合分析"],
            "view_type": ["沒有特別"],
            "keywords": [],
            "company_name": "",
            "stock_id": "",
            "time_info": "recent_5_days",
            "event_type": "其他",
            "error": str(e)
        }

# 測試用
if __name__ == "__main__":
    test_cases = [
        "華碩前天漲停板但今天下跌，是什麼原因",
        "台積電這季財報怎麼樣？",
        "請給我2330的法人買賣超"
    ]
    for case in test_cases:
        result = classify_and_extract(case)
        print(f"輸入: {case}")
        print(f"結果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print("---") 