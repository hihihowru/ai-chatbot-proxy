# search_news.py

## 功能說明

`search_news.py` 是智能新聞搜尋模組，專門用於搜尋台股相關的財經新聞和資訊。此模組具有以下特色：

1. **限制來源網站**：只從指定的 17 個台股財經網站抓取內容
2. **智能關鍵字生成**：使用 AI 生成精準的搜尋關鍵字組合
3. **分組搜尋功能**：將關鍵字分組執行，提高搜尋品質和覆蓋率
4. **結果過濾與去重**：自動過濾不符合條件的搜尋結果並去除重複
5. **詳細日誌記錄**：記錄搜尋過程和結果統計

## 允許的來源網站

系統只會從以下網站抓取內容：

| 網站名稱 | 網址 | 說明 |
|---------|------|------|
| Yahoo奇摩股市 | tw.finance.yahoo.com | 台股即時資訊 |
| 鉅亨網 | cnyes.com | 財經新聞與分析 |
| MoneyDJ 理財網 | moneydj.com | 投資理財資訊 |
| CMoney | cmoney.tw | 台股資料平台 |
| 經濟日報 | money.udn.com | 財經新聞 |
| 工商時報 | ctee.com.tw | 商業新聞 |
| ETtoday 財經 | finance.ettoday.net | 財經新聞 |
| Goodinfo | goodinfo.tw | 台股資訊網 |
| 財經M平方 | macromicro.me | 總體經濟分析 |
| Smart智富 | smart.businessweekly.com.tw | 投資理財雜誌 |
| 科技新報 | technews.tw | 科技產業新聞 |
| Nownews | nownews.com | 即時新聞 |
| MoneyLink 富聯網 | moneylink.com.tw | 財經資訊 |
| 股感 StockFeel | stockfeel.com.tw | 投資理財平台 |
| 商業周刊 | businessweekly.com.tw | 商業雜誌 |
| 今周刊 | businesstoday.com.tw | 財經雜誌 |
| PChome 股市頻道 | pchome.com.tw | 股市資訊 |

## 主要函數

### `generate_search_keywords(company_name, stock_id, intent, keywords, event_type, time_info) -> List[str]`
- **功能**：使用 OpenAI 生成精準的搜尋關鍵字
- **參數**：
  - `company_name`: 公司名稱
  - `stock_id`: 股票代號
  - `intent`: 問題意圖
  - `keywords`: 關鍵字列表
  - `event_type`: 事件類型
  - `time_info`: 時間資訊
- **返回**：8-12 個搜尋關鍵字

### `generate_fallback_keywords(...) -> List[str]`
- **功能**：生成備用的搜尋關鍵字（當 AI 生成失敗時使用）
- **邏輯**：充分利用所有允許的網站，根據意圖添加特定關鍵字

### `filter_results_by_site(results: List[Dict]) -> List[Dict]`
- **功能**：過濾搜尋結果，只保留允許的網站
- **返回**：過濾後的結果列表

### `group_search_keywords(keywords: List[str], group_count: int = 4) -> List[List[str]]`
- **功能**：將關鍵字分組，提高搜尋效率
- **邏輯**：將關鍵字平均分配到指定數量的組別

### `search_news_grouped(...) -> Dict`
- **功能**：執行分組搜尋
- **特色**：每組專注於特定網站，避免結果被稀釋

### `search_news_single_group(...) -> Dict`
- **功能**：執行單組搜尋
- **用途**：分組搜尋的子函數

### `remove_duplicate_results(results: List[Dict]) -> List[Dict]`
- **功能**：去除重複的搜尋結果
- **邏輯**：根據標題和網址進行去重

### `search_news_smart(...) -> Dict`
- **功能**：智能搜尋選擇器
- **參數**：`use_grouped=True` 使用分組搜尋，`use_grouped=False` 使用傳統搜尋

## Prompt 設計

### 搜尋關鍵字生成 Prompt
系統使用 OpenAI 生成 8-12 組具代表性的搜尋關鍵字組合，涵蓋：

- **財報數據**：EPS、營收、毛利率
- **股價異動解釋**：漲跌原因分析
- **法人籌碼**：投信、外資動態
- **分點主力動向**：主力買賣超
- **最新新聞事件**：即時新聞
- **ETF、產業輪動**：題材發酵
- **分析師預估**：目標價、評等

### 輸出格式
```json
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

## Input/Output 範例

### 輸入範例
```python
company_name = "台積電"
stock_id = "2330"
intent = "個股分析"
keywords = ["財報", "EPS"]
event_type = "財報"
time_info = "recent_5_days"
```

### 輸出範例
```json
{
  "success": true,
  "search_keywords": [
    "台積電 2330 財報 site:tw.finance.yahoo.com",
    "台積電 外資買賣 site:cnyes.com",
    "2330 法人動向 site:moneydj.com",
    "台積電 EPS 分析 site:cmoney.tw"
  ],
  "results": [
    {
      "title": "台積電 2024 年第四季財報分析",
      "link": "https://tw.finance.yahoo.com/news/...",
      "snippet": "台積電公布 2024 年第四季財報...",
      "site_name": "tw.finance.yahoo.com",
      "filtered": true
    }
  ],
  "total_results": 15,
  "filtered_results": 12,
  "logs": [
    "🔍 分組搜尋 - 總關鍵字數: 12",
    "📊 分組數量: 4",
    "✅ 第1組搜尋成功，獲得 8 個結果"
  ]
}
```

## 分組搜尋邏輯

### 分組策略
```
原始關鍵字 (12個) → 分組 (4組) → 每組3個關鍵字
├── 第1組: Yahoo奇摩股市、鉅亨網、MoneyDJ
├── 第2組: CMoney、經濟日報、工商時報  
├── 第3組: ETtoday、Goodinfo、財經M平方
└── 第4組: Smart智富、科技新報、Nownews
```

### 效能提升
- **覆蓋率**：從 3-4 個網站提升到 17 個網站
- **精準度**：分組搜尋提高每個關鍵字的搜尋效果
- **多樣性**：避免單一網站結果過多
- **結果數量**：通常 15-25 個結果（去重後）

## 使用建議

1. **預設使用分組搜尋**：`use_grouped=True`
2. **調整分組數量**：可根據需要調整 `group_count` 參數
3. **監控日誌**：關注分組執行狀態和結果分布
4. **API 限制**：注意 Serper API 的使用次數限制

## 錯誤處理

- **AI 生成失敗**：自動使用備用關鍵字生成
- **API 錯誤**：記錄錯誤並返回空結果
- **JSON 解析失敗**：使用正則表達式提取關鍵字

## 擴充性

- 可新增更多允許的網站
- 可調整關鍵字生成策略
- 可自訂分組邏輯
- 可擴充結果過濾規則 