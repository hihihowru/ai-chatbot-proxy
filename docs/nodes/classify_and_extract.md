# classify_and_extract

**用途**：
- 將使用者輸入的問題進行分類、關鍵字提取、投資面向判斷，並輸出結構化資訊。

**輸入**：
- 使用者問題（自然語言）

**輸出**：
```json
{
  "category": "...",
  "subcategory": [...],
  "view_type": [...],
  "keywords": [...],
  "company_name": "...",
  "stock_id": "...",
  "time_info": "...",
  "event_type": "..."
}
```

**主要邏輯**：
- 解析問題意圖（如股價分析、基本面查詢、投資建議等）
- 提取公司名稱、股票代號、時間、事件類型等關鍵字
- 判斷投資面向（基本面、技術面、籌碼面、沒有特別）

**Prompt 摘要**：
- 請針對提問判斷目的、提取關鍵字、分類投資面向，並以 JSON 格式輸出。
- 詳細 prompt 請參考原始碼 nodes/classify_and_extract.py 內 PROMPT 變數。 