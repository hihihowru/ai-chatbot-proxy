# generate_report.py

## 功能說明

`generate_report.py` 是報告生成模組，專門用於根據股票分析資料生成結構化的投資分析報告。此模組能夠：

1. **結構化報告**：生成包含多個章節的完整分析報告
2. **智能內容生成**：使用 OpenAI API 生成專業的分析內容
3. **多維度分析**：涵蓋股價異動、財務狀況、分析師預估等
4. **投資策略建議**：提供不同時間週期的投資建議
5. **標準化輸出**：確保報告格式的一致性和完整性

## 主要函數

### `generate_report(company_name: str, stock_id: str, intent: str = "", time_info: str = "", news_summary: str = "", chart_info: dict = None, news_sources: list = None, financial_sources: list = None) -> dict`
- **功能**：生成完整的股票分析報告
- **參數**：
  - `company_name`: 公司名稱
  - `stock_id`: 股票代號
  - `intent`: 用戶意圖/問題
  - `time_info`: 時間資訊
  - `news_summary`: 新聞摘要
  - `chart_info`: 圖表分析資料
  - `news_sources`: 新聞來源
  - `financial_sources`: 財務資料來源
- **邏輯**：
  1. 自動補全公司名稱（如果為空）
  2. 調用報告生成管道
  3. 處理成功/失敗結果
  4. 返回標準化報告格式
- **返回**：包含報告內容的字典

## 報告結構

### 1. 股價異動總結
```json
{
  "section": "股價異動總結",
  "cards": [
    { "title": "近期漲跌主因", "content": "..." },
    { "title": "法人動向", "content": "..." },
    { "title": "技術面觀察", "content": "..." }
  ]
}
```

### 2. 財務狀況分析
```json
{
  "section": "財務狀況分析",
  "cards": [
    { "title": "EPS", "content": "...", "table": [ ... ] },
    { "title": "營收", "content": "...", "table": [ ... ] },
    { "title": "毛利率", "content": "...", "table": [ ... ] },
    { "title": "負債比率", "content": "...", "table": [ ... ] }
  ]
}
```

### 3. 分析師預估
```json
{
  "section": "分析師預估",
  "eps_median": "...",
  "eps_high": "...",
  "eps_low": "...",
  "eps_avg": "...",
  "target_price": "...",
  "analyst_count": ...,
  "note": "..."
}
```

### 4. 投資策略建議
```json
{
  "section": "投資策略建議",
  "cards": [
    { "title": "日內交易", "suggestion": "...", "bullets": ["...", "..."] },
    { "title": "短線交易", "suggestion": "...", "bullets": ["...", "..."] },
    { "title": "中線投資", "suggestion": "...", "bullets": ["...", "..."] },
    { "title": "長線投資", "suggestion": "...", "bullets": ["...", "..."] }
  ],
  "summary_table": [
    {"period": "1天", "suggestion": "...", "confidence": "...", "reason": "..."},
    {"period": "1週", "suggestion": "...", "confidence": "...", "reason": "..."},
    {"period": "1個月", "suggestion": "...", "confidence": "...", "reason": "..."},
    {"period": "1季+", "suggestion": "...", "confidence": "...", "reason": "..."}
  ]
}
```

### 5. 操作注意事項
```json
{
  "section": "操作注意事項",
  "bullets": ["...", "..."]
}
```

### 6. 資料來源
```json
{
  "section": "資料來源",
  "sources": ["...", "..."]
}
```

### 7. 免責聲明
```json
{
  "section": "免責聲明",
  "disclaimer": "..."
}
```

## 提示詞設計

### 核心提示詞
```python
PROMPT = '''你是一位只能回傳 JSON 的 API，請根據下列資訊，產生結構化個股分析報告，**只回傳 JSON 陣列，每個 section 格式如下**：

[報告結構...]

**重要：你必須嚴格回傳上述 JSON 陣列格式，每個 section 只允許出現一次，且內容必須完整！**
**不要有任何說明、不要有 markdown、不要有多餘的文字，只能回傳 JSON 陣列！**

【輸入資料】
- 公司名稱：{{ company_name }}
- 股票代號：{{ stock_id }}
- 使用者問題：{{ user_input }}
- 資料摘要整理：{{ summary_points }}
'''
```

### 提示詞特點
1. **嚴格格式要求**：明確要求只回傳 JSON 格式
2. **完整結構定義**：詳細定義每個章節的格式
3. **輸入資料模板**：使用變數模板化輸入資料
4. **錯誤防護**：強調格式要求和內容完整性

## Input/Output 範例

### 輸入範例
```python
# 基本參數
company_name = "華碩"
stock_id = "2357"
intent = "華碩前幾天漲停後隔天又大跌，是為什麼呢？"

# 新聞摘要
news_summary = [
    "1. 📰 消息面分析：華碩受惠於AI PC需求成長，股價表現強勁",
    "2. 📊 財務數據：EPS成長15%，營收創新高",
    "3. 🎯 券商觀點：分析師預估目標價上調至500元",
    "4. 🌐 產業趨勢：AI PC市場需求持續成長",
    "5. ⚠️ 風險提醒：需注意市場波動風險"
]

# 新聞來源
news_sources = [
    {"title": "華碩AI PC需求強勁", "link": "https://example.com/news1"},
    {"title": "華碩財報亮眼", "link": "https://example.com/news2"}
]
```

### 輸出範例

#### 成功案例
```python
{
  "success": True,
  "stockName": "華碩",
  "stockId": "2357",
  "sections": [
    {
      "section": "股價異動總結",
      "cards": [
        {
          "title": "近期漲跌主因",
          "content": "華碩受惠於AI PC需求成長，市場預期看好，但隔日因獲利了結賣壓出現回檔。"
        },
        {
          "title": "法人動向",
          "content": "外資持續買超，投信也跟進加碼，法人動向偏多。"
        }
      ]
    },
    {
      "section": "投資策略建議",
      "cards": [
        {
          "title": "短線交易",
          "suggestion": "可逢低買進",
          "bullets": ["技術面支撐強勁", "法人持續買超"]
        }
      ],
      "summary_table": [
        {
          "period": "1週",
          "suggestion": "買進",
          "confidence": "高",
          "reason": "AI PC需求成長趨勢明確"
        }
      ]
    }
  ],
  "summary": "華碩受惠AI PC需求成長，法人持續買超，建議短線可逢低買進。",
  "paraphrased_prompt": "華碩前幾天漲停後隔天又大跌，是為什麼呢？",
  "logs": ["報告生成成功", "使用OpenAI API"]
}
```

#### 失敗案例
```python
{
  "success": False,
  "error": "API 調用失敗",
  "stockName": "華碩",
  "stockId": "2357",
  "sections": [],
  "summary": "報告產生失敗",
  "paraphrased_prompt": "華碩前幾天漲停後隔天又大跌，是為什麼呢？",
  "logs": ["API 調用失敗", "網路連線異常"]
}
```

## 錯誤處理

### 1. 公司名稱自動補全
```python
# 若 company_name 為空，則自動補上中文股名
if not company_name and stock_id:
    company_name = get_stock_name_by_id(stock_id) or stock_id
```

### 2. 成功/失敗結果處理
```python
if report_result.get("success"):
    # 成功案例：返回完整報告
    return {
        "success": True,
        "stockName": report["stockName"],
        "stockId": report["stockId"],
        "sections": report["sections"],
        "summary": report["summary"],
        "paraphrased_prompt": report["paraphrased_prompt"],
        "logs": report.get("logs", [])
    }
else:
    # 失敗案例：返回錯誤資訊
    return {
        "success": False,
        "error": report_result.get("error", "未知錯誤"),
        "stockName": company_name,
        "stockId": stock_id,
        "sections": [],
        "summary": "報告產生失敗",
        "paraphrased_prompt": intent,
        "logs": report_result.get("report", {}).get("logs", [])
    }
```

### 3. 日誌記錄
- 記錄報告生成過程
- 追蹤 API 調用狀態
- 保存錯誤資訊

## 效能優化

### 1. API 調用優化
- 使用非同步調用
- 實作重試機制
- 優化提示詞長度

### 2. 快取機制
- 快取常用報告模板
- 避免重複 API 調用
- 實作報告快取

### 3. 並發處理
- 支援多個報告同時生成
- 實作請求佇列
- 控制並發數量

## 擴充性

### 1. 新增報告章節
```python
# 在提示詞中新增章節定義
{
  "section": "新章節名稱",
  "content": "..."
}
```

### 2. 自訂報告格式
- 支援不同的報告模板
- 可自訂章節順序
- 支援多語言報告

### 3. 資料來源整合
- 整合更多資料來源
- 支援即時資料更新
- 實作資料驗證機制

## 使用場景

### 1. 投資分析
- 提供完整的股票分析報告
- 支援不同投資策略建議
- 涵蓋多維度分析內容

### 2. 研究報告
- 生成專業的研究報告
- 提供詳細的財務分析
- 支援比較分析功能

### 3. 決策支援
- 提供投資決策建議
- 分析風險和機會
- 支援不同時間週期

### 4. 教育用途
- 提供學習用的分析報告
- 解釋投資概念
- 支援教學需求

## 測試策略

### 1. 單元測試
```python
def test_generate_report():
    result = generate_report("華碩", "2357", "股價分析")
    assert result["success"] == True
    assert result["stockName"] == "華碩"
    assert len(result["sections"]) > 0
```

### 2. 整合測試
- 測試完整的報告生成流程
- 驗證報告內容的準確性
- 測試錯誤處理機制

### 3. 效能測試
- 測試 API 調用效能
- 驗證並發處理能力
- 測試記憶體使用情況

## 未來發展

### 1. 智能報告
- 使用更先進的 AI 模型
- 實作個性化報告
- 支援動態內容生成

### 2. 即時報告
- 支援即時資料更新
- 提供動態報告內容
- 實作推播功能

### 3. 互動式報告
- 支援用戶自訂內容
- 提供報告反饋機制
- 實作報告評分系統 