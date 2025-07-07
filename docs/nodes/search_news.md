# search_news.py

## 功能說明

本模組負責智能搜尋股票相關的最新新聞和財經資訊，透過 Serper API 和 OpenAI GPT 提供精準的新聞搜尋功能。支援多種搜尋策略，包括智能關鍵字生成、網站過濾、結果去重等，為投資分析提供高品質的新聞資料來源。

## 主要功能

### 核心流程
1. **智能關鍵字生成** - 使用 OpenAI GPT 生成精準搜尋關鍵字
2. **多網站搜尋** - 支援 18 個主要財經網站
3. **結果過濾** - 只保留可信賴的財經網站內容
4. **去重處理** - 移除重複的搜尋結果
5. **分組搜尋** - 將關鍵字分組以提高搜尋效率

## 主要函數

### `search_news(company_name: str, stock_id: str, intent: str, keywords: List[str], serper_api_key: str = None, event_type: str = '', time_info: str = '') -> Dict`

**功能**: 主要的新聞搜尋函數

**參數**:
- `company_name`: 公司名稱
- `stock_id`: 股票代碼
- `intent`: 搜尋意圖
- `keywords`: 額外關鍵字列表
- `serper_api_key`: Serper API 金鑰（可選）
- `event_type`: 事件類型（可選）
- `time_info`: 時間資訊（可選）

**回傳值**:
```python
{
    "success": bool,
    "results": List[Dict],  # 搜尋結果列表
    "total_results": int,   # 總結果數量
    "search_keywords": List[str],  # 使用的搜尋關鍵字
    "error": str            # 錯誤訊息 (可選)
}
```

### `generate_search_keywords(company_name: str, stock_id: str, intent: str, keywords: List[str], event_type: str = '', time_info: str = '') -> List[str]`

**功能**: 使用 OpenAI GPT 生成智能搜尋關鍵字

**特色**:
- 基於公司名稱、股票代碼、意圖生成關鍵字
- 支援多種財經網站
- 包含時間相關關鍵字
- 備用關鍵字機制

## 支援的財經網站

### 主要網站列表
1. **Yahoo奇摩股市** - tw.finance.yahoo.com
2. **鉅亨網** - cnyes.com
3. **MoneyDJ 理財網** - moneydj.com
4. **CMoney** - cmoney.tw
5. **經濟日報** - money.udn.com
6. **工商時報** - ctee.com.tw
7. **ETtoday 財經** - finance.ettoday.net
8. **Goodinfo** - goodinfo.tw
9. **財經M平方** - macromicro.me
10. **Smart智富** - smart.businessweekly.com.tw
11. **科技新報** - technews.tw
12. **Nownews** - nownews.com
13. **MoneyLink 富聯網** - moneylink.com.tw
14. **股感 StockFeel** - stockfeel.com.tw
15. **商業周刊** - businessweekly.com.tw
16. **今周刊** - businesstoday.com.tw
17. **PChome 股市頻道** - pchome.com.tw

## 智能關鍵字生成

### OpenAI Prompt 設計
```python
PROMPT = '''你是一個專業投資分析助理，請根據使用者輸入的問題，自動生成一組精準的搜尋關鍵字，幫助查找最新且與台股相關的財經新聞或數據資訊。

⚠限制來源：請僅從下列網站中抓取內容（出現在標題、網址或來源中才納入）：
Yahoo奇摩股市、鉅亨網 (cnyes)、MoneyDJ 理財網、CMoney、經濟日報、工商時報、ETtoday 財經、Goodinfo、財經M平方（MacroMicro）、Smart智富、科技新報、Nownews、MoneyLink 富聯網、股感 StockFeel、商業周刊、今周刊、PChome 股市頻道。

🧠使用者輸入會包含「公司名稱 / 股票代碼 + 問題」，請根據這些資訊生成具備高資訊密度的查詢組合，並試著涵蓋以下主題：
- 財報數據（例：EPS、營收、毛利率）
- 股價異動解釋
- 法人籌碼或投信、外資動態
- 分點主力動向
- 最新新聞事件
- ETF、產業輪動、題材發酵
- 分析師預估與目標價

📌請一次回傳 8-12 組具代表性的搜尋關鍵字組合，並充分利用所有允許的網站。每個網站至少生成一個關鍵字。

❗請優先產生『近一週』、『近一月』、『最新』等時間相關的新聞查詢組合，並盡量讓查詢結果聚焦於近期新聞。
'''
```

### 關鍵字生成範例
```python
# 輸入
company_name = "台積電"
stock_id = "2330"
intent = "最新消息"

# 輸出範例
[
    "台積電 2330 財報 site:tw.finance.yahoo.com",
    "台積電 外資買賣 site:cnyes.com",
    "2330 法人動向 site:moneydj.com",
    "台積電 EPS 分析 site:cmoney.tw",
    "台積電 財經新聞 site:money.udn.com",
    "2330 工商時報 site:ctee.com.tw",
    "台積電 財經報導 site:finance.ettoday.net",
    "台積電 基本面 site:goodinfo.tw",
    "台積電 總體經濟 site:macromicro.me",
    "台積電 投資理財 site:smart.businessweekly.com.tw",
    "台積電 科技新聞 site:technews.tw",
    "台積電 即時新聞 site:nownews.com"
]
```

## 搜尋策略

### 1. 分組搜尋
```python
def group_search_keywords(keywords: List[str], group_count: int = 4) -> List[List[str]]:
    """將關鍵字分組，每組最多 4 個關鍵字"""
    groups = []
    for i in range(0, len(keywords), group_count):
        group = keywords[i:i + group_count]
        groups.append(group)
    return groups
```

### 2. 結果過濾
```python
def filter_results_by_site(results: List[Dict]) -> List[Dict]:
    """過濾結果，只保留允許的網站"""
    filtered_results = []
    
    for result in results:
        link = result.get("link", "").lower()
        title = result.get("title", "").lower()
        
        # 檢查是否來自允許的網站
        is_allowed = False
        for site in ALLOWED_SITES:
            if site in link or site.replace(".", "") in link:
                is_allowed = True
                break
        
        if is_allowed:
            result["site_name"] = site
            result["filtered"] = True
            filtered_results.append(result)
    
    return filtered_results
```

### 3. 去重處理
```python
def remove_duplicate_results(results: List[Dict]) -> List[Dict]:
    """移除重複的搜尋結果"""
    seen_urls = set()
    unique_results = []
    
    for result in results:
        url = result.get("link", "").lower()
        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    return unique_results
```

## 輸出格式

### 搜尋結果結構
```python
{
    "success": True,
    "results": [
        {
            "title": "台積電AI晶片需求強勁，外資看好後市",
            "link": "https://tw.finance.yahoo.com/news/...",
            "snippet": "台積電受惠於AI晶片需求強勁，外資紛紛調高目標價...",
            "date": "2024-01-15",
            "site_name": "tw.finance.yahoo.com",
            "filtered": True
        }
    ],
    "total_results": 25,
    "search_keywords": [
        "台積電 2330 財報 site:tw.finance.yahoo.com",
        "台積電 外資買賣 site:cnyes.com"
    ]
}
```

## 輸入/輸出範例

### 輸入範例
```python
company_name = "台積電"
stock_id = "2330"
intent = "最新消息"
keywords = ["AI", "晶片"]
time_info = "近一週"
```

### 輸出範例
```python
{
    "success": True,
    "results": [
        {
            "title": "台積電AI晶片需求強勁，外資看好後市",
            "link": "https://tw.finance.yahoo.com/news/...",
            "snippet": "台積電受惠於AI晶片需求強勁...",
            "date": "2024-01-15",
            "site_name": "tw.finance.yahoo.com"
        },
        {
            "title": "台積電獲利創新高，法人持續買超",
            "link": "https://cnyes.com/news/...",
            "snippet": "台積電公布最新財報...",
            "date": "2024-01-14",
            "site_name": "cnyes.com"
        }
    ],
    "total_results": 15,
    "search_keywords": [
        "台積電 2330 財報 site:tw.finance.yahoo.com",
        "台積電 外資買賣 site:cnyes.com"
    ]
}
```

## 錯誤處理

### 常見錯誤
1. **OpenAI API 失敗**
   - 原因: API 金鑰無效或網路連線問題
   - 處理: 使用備用關鍵字生成

2. **Serper API 失敗**
   - 原因: API 金鑰無效或配額用完
   - 處理: 回傳 API 錯誤訊息

3. **搜尋結果為空**
   - 原因: 沒有找到相關新聞
   - 處理: 回傳空結果列表

### 錯誤回應範例
```python
{
    "success": False,
    "results": [],
    "total_results": 0,
    "search_keywords": [],
    "error": "Serper API 連線失敗"
}
```

## 效能考量

### 執行時間
- **一般情況**: 5-10 秒
- **主要耗時**: Serper API 搜尋和 OpenAI API 呼叫
- **優化策略**: 分組搜尋和結果快取

### API 限制
- **OpenAI API**: 有呼叫次數和速率限制
- **Serper API**: 有每日搜尋次數限制
- **建議使用**: 合理控制搜尋頻率

## 擴展性

### 可能的擴展功能
1. **更多網站支援** - 加入更多財經網站
2. **情感分析** - 分析新聞情感傾向
3. **新聞摘要** - 自動生成新聞摘要
4. **時間序列分析** - 分析新聞發布時間模式

### 擴展範例
```python
# 加入情感分析
def analyze_news_sentiment(results: List[Dict]) -> Dict:
    """分析新聞情感傾向"""
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    positive_keywords = ['利多', '看好', '成長', '突破', '創新高']
    negative_keywords = ['利空', '看壞', '下滑', '跌破', '創新低']
    
    for result in results:
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        
        if any(k in title or k in snippet for k in positive_keywords):
            positive_count += 1
        elif any(k in title or k in snippet for k in negative_keywords):
            negative_count += 1
        else:
            neutral_count += 1
    
    return {
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count,
        "sentiment_score": (positive_count - negative_count) / len(results) if results else 0
    }
```

## 測試

### 單元測試
```python
def test_search_news():
    result = search_news("台積電", "2330", "最新消息", [])
    
    assert result["success"] == True
    assert len(result["results"]) >= 0
    assert len(result["search_keywords"]) > 0
    assert all("site:" in keyword for keyword in result["search_keywords"])
```

### 整合測試
```python
# 測試完整流程
python test_watchlist.py
```

## 相關模組

### 依賴模組
- `openai` - OpenAI API 客戶端
- `requests` - HTTP 請求
- `json` - JSON 處理

### 使用模組
- `generate_section_focus_stocks.py` - 異動焦點個股 (使用新聞搜尋)

## 設計原則

### 1. 智能搜尋
- 使用 AI 生成精準關鍵字
- 支援多種搜尋策略
- 備用機制確保可靠性

### 2. 品質控制
- 只搜尋可信賴的財經網站
- 結果過濾和去重
- 詳細的錯誤處理

### 3. 效能優化
- 分組搜尋減少 API 呼叫
- 合理的結果限制
- 有效的快取策略

### 4. 可擴展性
- 模組化的設計
- 支援新增網站
- 彈性的搜尋策略 