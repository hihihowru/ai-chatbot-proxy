# classify_and_extract.py

## 功能說明

`classify_and_extract.py` 是問題分類與資訊提取模組，專門用於分析用戶的投資問題，並提取關鍵資訊。此模組能夠：

1. **問題分類**：將投資問題分類為7大類別和對應子分類
2. **股票偵測**：自動識別問題中的股票代號和公司名稱
3. **時間偵測**：提取問題中的時間表達
4. **關鍵字提取**：識別問題中的關鍵詞彙
5. **投資面向分析**：判斷問題涉及基本面、技術面、籌碼面等
6. **事件類型識別**：識別漲停、跌停、財報等事件類型

## 主要函數

### `classify_and_extract(user_input: str, model: str = "gpt-3.5-turbo") -> Dict`
- **功能**：整合的股票偵測、時間偵測和意圖分類
- **邏輯**：
  1. 偵測股票代號
  2. 偵測時間表達
  3. 使用 OpenAI 進行意圖分類和關鍵字提取
  4. 整合所有資訊並返回結果
- **返回**：包含分類結果和提取資訊的字典

### `detect_stocks(text: str) -> List[str]`
- **功能**：偵測文本中的股票代號
- **邏輯**：
  1. 先檢查4位數字格式的股票代號
  2. 再檢查公司別名匹配
  3. 返回所有偵測到的股票代號
- **返回**：股票代號列表

### `detect_time(question: str) -> str`
- **功能**：從問題中偵測時間表達
- **邏輯**：
  1. 使用正則表達式匹配時間關鍵字
  2. 提取數字參數（如「最近5天」中的5）
  3. 返回標準化的時間表達
- **返回**：標準化的時間表達字串

## 問題分類系統

### 1. 個股分析
- **公司介紹**：公司基本資訊、產業地位
- **基本面分析**：財務指標、營收獲利、產業地位等
- **籌碼面分析**：法人動向、大戶散戶、股權分散等
- **技術面分析**：K線、均線、技術指標、價量關係等
- **個股資訊查找**：EPS、股價、營收、財報等單一指標查詢
- **價格評論**：漲跌原因、建議買賣

### 2. 選股建議
- **篩選條件選股**：根據條件篩選股票
- **法人追蹤選股**：追蹤法人動向選股
- **籌碼追蹤選股**：追蹤籌碼面選股
- **強勢股/起漲股/題材熱股**：特定類型股票推薦

### 3. 盤勢分析
- **大盤走勢分析**：整體市場分析
- **類股輪動/熱門族群**：產業輪動分析
- **產業**：特定產業分析
- **國際股市**：國際市場分析
- **美股**：美國股市分析
- **期貨**：期貨市場分析
- **總經**：總體經濟分析

### 4. 比較分析
- **個股比較**：多檔股票比較
- **類股比較**：不同類股比較
- **同產業走勢比較**：同業比較

### 5. 金融知識詢問
- **制度說明**：交易制度、法規說明
- **指標定義**：如 RSI、周轉率等技術指標

### 6. 複雜查詢任務
- **多層條件查詢**：複雜條件組合查詢
- **結構化資料對照**：多維度資料分析
- **模擬選股/假設回測問題**：假設性分析

### 7. 無效問題（不需處理）
- **無明確投資內容**：非投資相關問題
- **預測性問題**：未來股價等預測
- **ChatGPT 自由發揮/幽默提問**：非正式問題

## 投資面向分析

### 支援的面向
- **基本面**：財務指標、營收獲利、產業地位
- **技術面**：K線、均線、技術指標、價量關係
- **籌碼面**：法人動向、大戶散戶、股權分散
- **沒有特別**：綜合性分析或無特定偏向

## 事件類型識別

### 支援的事件類型
- **漲停**：股價漲停相關
- **跌停**：股價跌停相關
- **上漲**：股價上漲相關
- **下跌**：股價下跌相關
- **財報**：財報公布相關
- **法說會**：法說會相關
- **新聞**：新聞事件相關
- **其他**：其他類型事件

## 提示詞設計

### 核心提示詞
```python
PROMPT = '''你是一個投資問題理解模組。

請針對以下提問，判斷：
1️⃣ 提問的目的（分析股價原因 / 基本面查詢 / 投資建議等）
2️⃣ 提取關鍵字（公司名稱、股票代號、時間、事件類型）
3️⃣ 投資面向（可複選：基本面、技術面、籌碼面、沒有特別）

📂 問題大分類（擇一）與其對應子分類（可複選）如下：
[分類系統詳細說明...]

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

使用者問題：
{{ user_input }}
'''
```

### 提示詞特點
1. **詳細分類系統**：提供7大類別和對應子分類
2. **明確輸出格式**：要求JSON格式輸出
3. **多維度分析**：涵蓋分類、面向、關鍵字等多個維度
4. **實用導向**：針對實際投資問題設計

## Input/Output 範例

### 輸入範例
```python
test_cases = [
    "華碩前天漲停板但今天下跌，是什麼原因",
    "台積電這季財報怎麼樣？",
    "請給我2330的法人買賣超",
    "大盤最近走勢如何？",
    "台積電和聯發科哪個比較好？"
]
```

### 輸出範例

#### 個股分析案例
```python
# 輸入: "華碩前天漲停板但今天下跌，是什麼原因"
{
  "category": "個股分析",
  "subcategory": ["價格評論", "籌碼面分析"],
  "view_type": ["籌碼面", "技術面"],
  "keywords": ["華碩", "2357", "漲停", "下跌", "原因"],
  "company_name": "華碩",
  "stock_id": "2357",
  "time_info": "day_before_yesterday",
  "event_type": "漲停"
}
```

#### 基本面查詢案例
```python
# 輸入: "台積電這季財報怎麼樣？"
{
  "category": "個股分析",
  "subcategory": ["基本面分析", "個股資訊查找"],
  "view_type": ["基本面"],
  "keywords": ["台積電", "2330", "財報", "這季", "營收"],
  "company_name": "台積電",
  "stock_id": "2330",
  "time_info": "this_quarter",
  "event_type": "財報"
}
```

#### 籌碼面查詢案例
```python
# 輸入: "請給我2330的法人買賣超"
{
  "category": "個股分析",
  "subcategory": ["籌碼面分析", "個股資訊查找"],
  "view_type": ["籌碼面"],
  "keywords": ["2330", "台積電", "法人", "買賣超", "外資"],
  "company_name": "台積電",
  "stock_id": "2330",
  "time_info": "recent_5_days",
  "event_type": "其他"
}
```

#### 盤勢分析案例
```python
# 輸入: "大盤最近走勢如何？"
{
  "category": "盤勢分析",
  "subcategory": ["大盤走勢分析"],
  "view_type": ["技術面"],
  "keywords": ["大盤", "走勢", "最近", "指數", "趨勢"],
  "company_name": "",
  "stock_id": "",
  "time_info": "recent_5_days",
  "event_type": "其他"
}
```

#### 比較分析案例
```python
# 輸入: "台積電和聯發科哪個比較好？"
{
  "category": "比較分析",
  "subcategory": ["個股比較"],
  "view_type": ["基本面", "技術面"],
  "keywords": ["台積電", "2330", "聯發科", "2454", "比較"],
  "company_name": "台積電",
  "stock_id": "2330",
  "time_info": "recent_5_days",
  "event_type": "其他"
}
```

### 完整測試範例
```python
# 測試問題分類
test_question = "華碩前天漲停板但今天下跌，是什麼原因"
result = classify_and_extract(test_question)

print(f"問題: {test_question}")
print(f"分類: {result['category']}")
print(f"子分類: {result['subcategory']}")
print(f"投資面向: {result['view_type']}")
print(f"關鍵字: {result['keywords']}")
print(f"公司名稱: {result['company_name']}")
print(f"股票代號: {result['stock_id']}")
print(f"時間資訊: {result['time_info']}")
print(f"事件類型: {result['event_type']}")
```

## 股票偵測邏輯

### 1. 數字格式偵測
```python
# 使用正則表達式匹配 4 位數字
stock_codes = re.findall(r'\b\d{4}\b', text)
for code in stock_codes:
    if code in stock_dict:
        detected_stocks.append(code)
```

### 2. 別名匹配
```python
# 檢查公司別名
for alias, stock_id in alias_to_id.items():
    if alias in text and stock_id not in detected_stocks:
        detected_stocks.append(stock_id)
```

### 3. 股票別名字典
- **檔案路徑**：`data/stock_alias_dict.json`
- **格式**：`{"2330": ["台積電", "TSMC", "2330"]}`
- **反查表**：建立 `alias_to_id` 映射

## 時間偵測邏輯

### 支援的時間模式
```python
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
```

### 預設時間
- 當未偵測到時間表達時，預設為 `"recent_5_days"`

## 錯誤處理

### 1. OpenAI API 調用失敗
```python
try:
    response = client.chat.completions.create(...)
    result = json.loads(response.choices[0].message.content.strip())
except Exception as e:
    print(f"[classify_and_extract ERROR] {e}")
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
```

### 2. JSON 解析失敗
```python
try:
    result = json.loads(response.choices[0].message.content.strip())
except json.JSONDecodeError:
    # 返回基本資訊
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
```

### 3. 資訊補充
- 自動補充股票代號資訊
- 自動補充時間資訊
- 提供合理的預設值

## 效能優化

### 1. 股票別名預載入
- 模組載入時一次性讀取股票別名字典
- 建立反查表提高查詢效率
- 避免重複檔案讀取

### 2. 正則表達式優化
- 使用編譯後的正則表達式
- 優化匹配順序
- 最小化重複計算

### 3. API 調用優化
- 使用較低的 temperature 值（0）
- 提供明確的輸出格式要求
- 實作錯誤重試機制

## 擴充性

### 1. 新增問題類別
- 在提示詞中新增分類定義
- 支援更細緻的子分類
- 保持向後相容性

### 2. 自訂偵測規則
- 可擴充股票偵測邏輯
- 支援更多時間表達
- 可新增關鍵字提取規則

### 3. 多語言支援
- 支援其他語言的問題分類
- 可擴充多語言股票別名
- 保持一致的API介面

## 使用場景

### 1. 智能問答系統
- 自動理解用戶問題意圖
- 提供精準的回答方向
- 支援多種問題類型

### 2. 投資分析平台
- 自動分類投資問題
- 提供對應的分析工具
- 支援個性化服務

### 3. 研究報告生成
- 根據問題類型生成對應報告
- 提供結構化的分析內容
- 支援多維度分析

### 4. 決策支援系統
- 理解投資決策需求
- 提供相關的決策資訊
- 支援不同投資策略 