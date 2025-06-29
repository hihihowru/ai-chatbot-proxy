# 搜尋功能更新說明

## 📋 更新概述

本次更新針對搜尋功能進行了重大改進，主要包括：

1. **限制來源網站**：只從指定的台股財經網站抓取內容
2. **精準關鍵字生成**：使用 AI 生成更精準的搜尋關鍵字組合
3. **詳細日誌記錄**：記錄網站名稱、新聞標題、日期等有用資訊
4. **智能過濾機制**：自動過濾不符合條件的搜尋結果
5. **分組搜尋功能**：將關鍵字分組執行，提高搜尋品質和覆蓋率

## 🎯 允許的來源網站

系統現在只會從以下網站抓取內容：

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

## 🔍 分組搜尋功能

### 功能特點

1. **智能分組**：將生成的關鍵字平均分配到 4 個搜尋組
2. **提高品質**：每組專注於特定網站，避免結果被稀釋
3. **增加覆蓋率**：充分利用所有允許的網站
4. **去重機制**：自動去除重複的搜尋結果

### 分組邏輯

```
原始關鍵字 (12個) → 分組 (4組) → 每組3個關鍵字
├── 第1組: Yahoo奇摩股市、鉅亨網、MoneyDJ
├── 第2組: CMoney、經濟日報、工商時報  
├── 第3組: ETtoday、Goodinfo、財經M平方
└── 第4組: Smart智富、科技新報、Nownews
```

### 使用方式

```python
# 使用分組搜尋（推薦）
result = search_news_smart(
    company_name="台積電",
    stock_id="2330", 
    intent="個股分析",
    keywords=["財報", "EPS"],
    use_grouped=True  # 啟用分組搜尋
)

# 使用傳統搜尋
result = search_news_smart(
    company_name="台積電",
    stock_id="2330",
    intent="個股分析", 
    keywords=["財報", "EPS"],
    use_grouped=False  # 使用傳統搜尋
)
```

## 📊 關鍵字生成改進

### 生成數量
- **之前**：3-5 個關鍵字
- **現在**：8-12 個關鍵字

### 網站覆蓋
- **之前**：主要使用 3-4 個網站
- **現在**：充分利用所有 17 個允許網站

### 範例關鍵字

```
台積電 2330 財報 site:tw.finance.yahoo.com
台積電 外資買賣 site:cnyes.com
2330 法人動向 site:moneydj.com
台積電 EPS 分析 site:cmoney.tw
台積電 財經新聞 site:money.udn.com
2330 工商時報 site:ctee.com.tw
台積電 財經報導 site:finance.ettoday.net
台積電 基本面 site:goodinfo.tw
台積電 總體經濟 site:macromicro.me
台積電 投資理財 site:smart.businessweekly.com.tw
台積電 科技新聞 site:technews.tw
台積電 即時新聞 site:nownews.com
```

## 📝 日誌記錄功能

### 記錄內容
- 搜尋關鍵字列表
- 分組資訊和執行狀態
- 網站過濾統計
- 每個結果的詳細資訊

### 日誌範例

```
🔍 分組搜尋 - 總關鍵字數: 12
📊 分組數量: 4
   第1組 (3個): ['台積電 2330 財報 site:tw.finance.yahoo.com', ...]
   第2組 (3個): ['台積電 EPS 分析 site:cmoney.tw', ...]
   第3組 (3個): ['台積電 財經報導 site:finance.ettoday.net', ...]
   第4組 (3個): ['台積電 投資理財 site:smart.businessweekly.com.tw', ...]

🔍 執行第1組搜尋...
✅ 第1組搜尋成功，獲得 8 個結果
🔍 執行第2組搜尋...
✅ 第2組搜尋成功，獲得 6 個結果
🔍 執行第3組搜尋...
✅ 第3組搜尋成功，獲得 7 個結果
🔍 執行第4組搜尋...
✅ 第4組搜尋成功，獲得 5 個結果

📊 分組搜尋完成:
   總搜尋關鍵字: 12
   總結果數: 26
   去重後結果數: 22
```

## 🔧 技術實現

### 新增函數

1. **`group_search_keywords()`**：關鍵字分組
2. **`search_news_grouped()`**：分組搜尋執行
3. **`search_news_single_group()`**：單組搜尋
4. **`search_news_smart()`**：智能搜尋選擇
5. **`remove_duplicate_results()`**：結果去重

### 檔案更新

- `langgraph_app/nodes/search_news.py`：新增分組搜尋功能
- `langgraph_app/main.py`：更新搜尋調用
- `test_grouped_search.py`：新增測試腳本

## 📈 效能提升

### 搜尋品質
- **覆蓋率**：從 3-4 個網站提升到 17 個網站
- **精準度**：分組搜尋提高每個關鍵字的搜尋效果
- **多樣性**：避免單一網站結果過多

### 結果數量
- **之前**：通常 2-5 個結果
- **現在**：通常 15-25 個結果（去重後）

### 網站分布
- **之前**：集中在 2-3 個主要網站
- **現在**：平均分布在所有允許網站

## 🧪 測試

### 測試腳本

```bash
# 測試分組搜尋功能
python3 test_grouped_search.py

# 測試一般搜尋功能
python3 test_new_search.py
```

### 測試結果

```
✅ 分組搜尋成功!
📊 分組數量: 4
📊 搜尋關鍵字數量: 12
📊 結果數量: 22
📝 前5個結果:
   1. [tw.finance.yahoo.com] 台積電 股價分析
   2. [cnyes.com] 台積電 財報分析
   3. [moneydj.com] 台積電 法人動向
   4. [cmoney.tw] 台積電 EPS 分析
   5. [money.udn.com] 台積電 財經新聞
```

## 🚀 使用建議

1. **預設使用分組搜尋**：`use_grouped=True`
2. **調整分組數量**：可根據需要調整 `group_count` 參數
3. **監控日誌**：關注分組執行狀態和結果分布
4. **定期測試**：使用測試腳本驗證功能正常

## 📋 更新日誌

- **2025-01-15**：新增分組搜尋功能
- **2025-01-15**：擴展關鍵字生成數量
- **2025-01-15**：完善日誌記錄功能
- **2025-01-15**：新增測試腳本

## 📝 注意事項

1. **API Key 需求**：需要設定 `SERPER_API_KEY` 環境變數
2. **網站限制**：只會返回指定網站的新聞
3. **關鍵字數量**：限制為 3-5 個關鍵字組合
4. **結果數量**：最多返回 15 個過濾後的結果

## 🤝 貢獻

如需修改允許的網站列表或調整搜尋邏輯，請編輯 `langgraph_app/nodes/search_news.py` 檔案中的 `ALLOWED_SITES` 常數和相關函數。 