# 投資分析系統 - Serper API 整合

這是一個基於 LangGraph 的投資分析系統，整合了 Serper API 進行新聞搜尋，並生成專業的投資分析報告。

## 系統架構 系統架構

### Node 1: classify_and_extract
- **功能**: 問題理解與分類
- **輸入**: 使用者問題
- **輸出**: 意圖分類、股票代號、時間資訊、關鍵字等
- **整合**: 股票偵測 + 時間偵測 + 意圖分類

### Node 2: search_news  
- **功能**: 新聞搜尋
- **輸入**: 公司名稱、股票代號、意圖、關鍵字
- **輸出**: 搜尋關鍵詞、搜尋結果
- **API**: Serper API (Google 搜尋)

### Node 3: summarize_results
- **功能**: 結果摘要
- **輸入**: 搜尋結果
- **輸出**: 結構化摘要（消息面、財務數據、券商觀點等）

### Node 4: generate_report
- **功能**: 報告生成
- **輸入**: 摘要結果
- **輸出**: 專業投資分析報告

##  快速開始

### 1. 安裝依賴

```bash
cd ai-chatbot-proxy/langgraph_app
pip install -r requirements.txt
```

### 2. 設定環境變數

```bash
export SERPER_API_KEY="your_serper_api_key_here"
```

### 3. 啟動服務

```bash
cd ai-chatbot-proxy/langgraph_app
python main.py
```

服務將在 `http://localhost:8000` 啟動

## 📡 API 端點

### 1. 投資分析 API

**POST** `/api/investment-analysis`

```json
{
  "question": "華碩前天漲停板但今天下跌，是什麼原因",
  "serper_api_key": "optional_serper_api_key"
}
```

**回應**:
```json
{
  "success": true,
  "user_input": "華碩前天漲停板但今天下跌，是什麼原因",
  "intent": "股價分析",
  "company_name": "華碩",
  "stock_id": "2357",
  "time_info": "day_before_yesterday",
  "event_type": "漲停",
  "search_keywords": ["華碩 漲停 下跌 原因", "2357 股價分析"],
  "search_results": [...],
  "summary": "1. 📰 消息面分析：...",
  "summary_points": [...],
  "report": "1. 📌 問題簡述與事件背景...",
  "report_sections": [...],
  "logs": ["🔍 開始問題理解與分類...", " 問題理解完成：..."]
}
```

### 2. SSE 投資分析 API

**GET** `/api/investment-analysis-sse?question=問題&serper_api_key=可選`

使用 Server-Sent Events 即時顯示分析進度

## 🧪 測試

### 執行測試腳本

```bash
cd ai-chatbot-proxy
python test_investment_analysis.py
```

### 測試個別節點

```python
from langgraph_app.nodes.classify_and_extract import classify_and_extract
from langgraph_app.nodes.search_news import search_news
from langgraph_app.nodes.summarize_results import summarize_results
from langgraph_app.nodes.generate_report import generate_report

# 測試問題理解
result = classify_and_extract("華碩前天漲停板但今天下跌，是什麼原因")
print(result)

# 測試新聞搜尋
search_result = search_news("華碩", "2357", "股價分析", ["漲停", "下跌"])
print(search_result)
```

## 📊 報告格式

生成的投資分析報告包含以下結構：

1. **📌 問題簡述與事件背景**
   - 總結用戶提問重點

2. **📉 股價異動說明**
   - 消息面、籌碼面、技術面分析

3. **📊 財務狀況分析**
   - EPS、營收成長、分析師預估

4. **🌐 產業與市場環境分析**
   - AI/PC/總經背景

5. **💡 投資策略建議**
   - 根據持有時間：1日/1週/1月/1季+

6. **⚠ 投資風險提醒**
   - 2-3項主要風險

##  自訂設定

### 修改 Prompt

每個節點的 prompt 都可以在對應的 `.py` 檔案中修改：

- `langgraph_app/nodes/classify_and_extract.py`
- `langgraph_app/nodes/search_news.py`
- `langgraph_app/nodes/summarize_results.py`
- `langgraph_app/nodes/generate_report.py`

### 調整搜尋參數

在 `search_news.py` 中可以調整：
- 搜尋結果數量
- 搜尋關鍵詞生成邏輯
- Serper API 參數

### 自訂報告格式

在 `generate_report.py` 中可以修改報告的結構和格式。

## 🌐 前端整合

### React 前端範例

```javascript
// 使用 SSE 即時顯示分析進度
const eventSource = new EventSource('/api/investment-analysis-sse?question=華碩前天漲停板但今天下跌，是什麼原因');

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  if (data.log) {
    console.log('進度:', data.log);
  } else if (data.result) {
    console.log('分析完成:', data.result);
    eventSource.close();
  }
};
```

### 使用 Fetch API

```javascript
const response = await fetch('/api/investment-analysis', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: '華碩前天漲停板但今天下跌，是什麼原因'
  })
});

const result = await response.json();
console.log('分析結果:', result);
```

## 🔑 Serper API 設定

1. 註冊 [Serper API](https://serper.dev/)
2. 取得 API Key
3. 設定環境變數或在請求中提供

```bash
export SERPER_API_KEY="your_api_key_here"
```

##  日誌系統

系統會記錄每個節點的執行狀態：

- 🔍 開始問題理解與分類...
-  問題理解完成：股價分析 | 華碩(2357)
- 🔎 開始搜尋相關新聞...
-  新聞搜尋完成：找到 8 個結果
-  開始摘要搜尋結果...
-  結果摘要完成
- 📊 開始生成投資分析報告...
-  投資分析報告生成完成

## 🚨 錯誤處理

系統包含完整的錯誤處理機制：

- API 請求失敗
- JSON 解析錯誤
- OpenAI API 錯誤
- 網路連線問題

所有錯誤都會記錄在 `logs` 中並返回適當的錯誤訊息。

## 📈 效能優化

- 使用 LangGraph 進行並行處理
- 快取搜尋結果
- 非同步 API 請求
- 模組化設計便於擴展

## 🔮 未來擴展

- 整合更多資料來源
- 支援多股票比較分析
- 加入技術分析指標
- 實時股價資料整合
- 情感分析功能 