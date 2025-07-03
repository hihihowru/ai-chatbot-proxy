# 台股投資分析系統 - 自選股摘要功能文檔

## 概述

本系統是一個基於 AI 的台股投資分析平台，提供智能化的股票分析、自選股摘要、新聞搜尋等功能。系統採用前後端分離架構，後端使用 FastAPI + Python，前端使用 Next.js + TypeScript。

## 主要功能

### 1. 自選股摘要 (Watchlist Summary)
- **功能描述**: 為用戶的自選股清單產生完整的分析報告
- **核心特色**: 
  - 產業分布統計
  - 股價摘要與報酬率分析
  - 異動焦點個股分析
  - 智能新聞搜尋與摘要
  - 產業比較分析

### 2. 智能問答系統
- **功能描述**: 基於 LLM 的股票投資問題解答
- **支援類型**: 個股分析、選股建議、盤勢分析、比較分析等

### 3. 新聞搜尋與分析
- **功能描述**: 智能搜尋股票相關新聞並產生摘要
- **資料來源**: Serper API、CMoney 財經資料

## 系統架構

### 後端架構 (ai-chatbot-proxy)
```
├── main.py                          # FastAPI 應用程式入口
├── routes/
│   └── answer.py                    # API 路由定義
├── langgraph_app/nodes/             # 核心業務邏輯模組
│   ├── generate_watchlist_summary_pipeline.py    # 自選股摘要主流程
│   ├── generate_section_*.py        # 各分析區塊生成器
│   ├── detect_*.py                  # 意圖偵測與分類
│   └── search_*.py                  # 搜尋相關功能
├── schemas.py                       # 資料結構定義
└── utils/                           # 工具函數
```

### 前端架構 (ai_chat_twstock)
```
├── app/
│   ├── page.tsx                     # 主頁面
│   ├── watchlist/                   # 自選股頁面
│   ├── chat/                        # 聊天頁面
│   ├── api/                         # 前端 API 路由
│   └── components/                  # React 組件
│       └── WatchlistSummaryCard.tsx # 自選股摘要卡片組件
```

## 技術棧

### 後端
- **框架**: FastAPI
- **語言**: Python 3.8+
- **AI/ML**: OpenAI GPT-3.5/4, LangGraph
- **資料庫**: Finlab API (台股資料)
- **搜尋**: Serper API (新聞搜尋)

### 前端
- **框架**: Next.js 14
- **語言**: TypeScript
- **UI 庫**: Tailwind CSS, Lucide React
- **狀態管理**: React Hooks
- **API 通訊**: Fetch API

## 快速開始

### 1. 環境設定
```bash
# 後端
cd ai-chatbot-proxy
pip install -r requirements.txt

# 前端
cd ai_chat_twstock
npm install
```

### 2. 環境變數
```bash
# 後端 (.env)
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key

# 前端 (.env.local)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 3. 啟動服務
```bash
# 後端
cd ai-chatbot-proxy
python main.py

# 前端
cd ai_chat_twstock
npm run dev
```

## API 文檔

### 自選股摘要 API
- **端點**: `POST /watchlist-summary`
- **功能**: 產生自選股分析報告
- **詳細文檔**: [API 文檔](./api/watchlist-summary.md)

### 智能問答 API
- **端點**: `POST /answer`
- **功能**: 回答股票投資相關問題
- **詳細文檔**: [API 文檔](./api/answer.md)

## 模組文檔

### 後端節點模組
- [detect_intent.md](./nodes/detect_intent.md) - 意圖偵測
- [classify_and_extract.md](./nodes/classify_and_extract.md) - 分類與提取
- [generate_watchlist_summary_pipeline.md](./nodes/generate_watchlist_summary_pipeline.md) - 自選股摘要主流程
- [generate_section_industry_distribution.md](./nodes/generate_section_industry_distribution.md) - 產業分布統計
- [generate_section_price_summary.md](./nodes/generate_section_price_summary.md) - 股價摘要
- [generate_section_return_analysis.md](./nodes/generate_section_return_analysis.md) - 報酬率分析
- [generate_section_focus_stocks.md](./nodes/generate_section_focus_stocks.md) - 異動焦點個股
- [generate_section_industry_comparison.md](./nodes/generate_section_industry_comparison.md) - 產業比較
- [search_news.md](./nodes/search_news.md) - 新聞搜尋

### 前端組件
- [WatchlistSummaryCard.md](./components/WatchlistSummaryCard.md) - 自選股摘要卡片組件

## 測試

### 後端測試
```bash
cd ai-chatbot-proxy
python test_watchlist.py
python test_watchlist_flow.py
```

### 前端測試
```bash
cd ai_chat_twstock
npm test
```

## 部署

### 後端部署
```bash
# 使用 Docker
docker build -t ai-chatbot-proxy .
docker run -p 8000:8000 ai-chatbot-proxy

# 或直接部署
python main.py
```

### 前端部署
```bash
# 建置
npm run build

# 部署到 Vercel
vercel --prod
```

## 貢獻指南

1. Fork 專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 聯絡資訊

如有問題或建議，請透過以下方式聯絡：
- 專案 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 電子郵件: your-email@example.com 