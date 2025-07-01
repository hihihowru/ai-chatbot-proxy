# 自選股摘要功能

## 功能概述

自選股摘要功能可以為用戶的自選股清單產生完整的分析報告，包含四個主要區塊：

1. **產業分布統計** - 統計自選股的產業分布
2. **股價摘要** - 計算各股票的報酬率並以表格呈現
3. **報酬率統計分析** - 分析整體報酬率統計資料
4. **異動焦點個股** - 搜尋每檔股票的最新消息並產生摘要

## 架構說明

### 後端架構

```
ai-chatbot-proxy/
├── langgraph_app/nodes/
│   ├── generate_section_industry_distribution.py    # 產業分布統計
│   ├── generate_section_price_summary.py           # 股價摘要
│   ├── generate_section_return_analysis.py         # 報酬率統計分析
│   ├── generate_section_focus_stocks.py            # 異動焦點個股
│   └── generate_watchlist_summary_pipeline.py      # 整合 Pipeline
├── routes/answer.py                                # API 路由
└── schemas.py                                      # 資料結構定義
```

### 前端架構

```
ai_chat_twstock/
├── app/
│   ├── watchlist/page.tsx                          # 自選股摘要頁面
│   ├── api/watchlist-summary/route.ts              # 前端 API 路由
│   └── components/
│       └── WatchlistSummaryCard.tsx                # 自選股摘要組件
```

## API 使用方式

### 後端 API

**端點：** `POST /watchlist-summary`

**請求格式：**
```json
{
  "stock_list": [2303, 2330, 2610, 2376, 2317],
  "userId": "user123"
}
```

**回應格式：**
```json
{
  "success": true,
  "sections": [
    {
      "title": "產業分布統計",
      "content": "🏷️ 產業分布統計\n\t•\t電子（半導體、PC）：5 檔\n\t•\t生技醫療：2 檔",
      "cards": [...],
      "sources": [...]
    },
    ...
  ],
  "logs": ["步驟 1: 產生產業分布統計", "步驟 2: 產生股價摘要", ...]
}
```

### 前端 API

**端點：** `POST /api/watchlist-summary`

**使用方式：**
```javascript
const response = await fetch('/api/watchlist-summary', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    stock_list: [2303, 2330, 2610],
    userId: 'user123'
  }),
});

const data = await response.json();
```

## 功能特色

### 1. 產業分布統計
- 從 Finlab 取得公司基本資訊
- 統計自選股的產業分布
- 顯示各產業的股票數量

### 2. 股價摘要
- 計算 1日、5日、20日、60日、240日報酬率
- 以表格形式呈現，支援顏色標示
- 正數報酬率顯示紅色，負數顯示綠色

### 3. 報酬率統計分析
- 統計上漲/下跌家數
- 計算平均報酬率
- 找出最大漲幅股票

### 4. 異動焦點個股
- 使用 Serper API 搜尋每檔股票最新消息
- 智能分析搜尋結果，提取主題
- 結合報酬率資訊產生摘要
- 為避免 API 效能問題，只處理前 5 檔股票

## 部署說明

### 1. 後端部署
```bash
cd ai-chatbot-proxy
python main.py
```

### 2. 前端部署
```bash
cd ai_chat_twstock
npm run dev
```

### 3. 環境變數
確保以下環境變數已設定：
- `OPENAI_API_KEY` - OpenAI API 金鑰
- `SERPER_API_KEY` - Serper API 金鑰
- Finlab 登入資訊

## 測試

### 1. 測試 Pipeline
```bash
cd ai-chatbot-proxy
python test_watchlist.py
```

### 2. 測試完整流程
```bash
cd ai-chatbot-proxy
python test_watchlist_complete.py
```

## 注意事項

1. **Finlab 登入**：需要先登入 Finlab 才能取得資料
2. **API 限制**：異動焦點個股功能會呼叫 Serper API，有次數限制
3. **資料來源**：所有資料來源都會在報告中標示
4. **錯誤處理**：各步驟都有錯誤處理機制，單一步驟失敗不會影響整體流程

## 未來改進

1. **快取機制**：加入資料快取，減少重複 API 呼叫
2. **更多分析**：加入技術分析、籌碼分析等
3. **自訂時間範圍**：讓用戶可以自訂分析的時間範圍
4. **匯出功能**：支援 PDF 或 Excel 匯出
5. **即時更新**：支援即時資料更新 