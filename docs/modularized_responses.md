# 模組化回覆功能說明

## 概述
本系統採用模組化架構設計回覆功能，將複雜的 AI 回應拆解為獨立可重用的模組，提升開發效率與維護性。

## 已模組化的回覆功能

### 1. 自選股摘要 (Watchlist Summary)
**模組化架構**：`generate_watchlist_summary_pipeline`
- **整合模組**：6 個核心功能模組
- **執行順序**：產業分布 → 產業比較 → 股價摘要 → 報酬統計 → 異動焦點 → 智能新聞
- **輸出格式**：WatchlistResponse (包含多個 sections)
- **檔案位置**：`langgraph_app/nodes/generate_watchlist_summary_pipeline.py`

**子模組**：
- `generate_section_industry_distribution.py` - 產業分布統計
- `generate_section_industry_comparison.py` - 產業比較分析
- `generate_section_price_summary.py` - 股價摘要表格
- `generate_section_return_analysis.py` - 報酬率統計分析
- `generate_section_focus_stocks.py` - 異動焦點個股
- `search_news.py` - 智能新聞搜尋與摘要

### 2. 個股分析 (Stock Analysis)
**模組化架構**：`investment_analysis_graph`
- **整合模組**：多個分析節點
- **功能範圍**：技術分析、基本面分析、新聞分析
- **輸出格式**：結構化分析報告
- **檔案位置**：`langgraph_app/graphs/investment_analysis_graph.py`

### 3. 投資摘要 (Investment Summary)
**模組化架構**：`investment_summary_graph`
- **整合模組**：摘要生成節點
- **功能範圍**：投資建議摘要、風險評估
- **輸出格式**：摘要報告
- **檔案位置**：`langgraph_app/graphs/investment_summary_graph.py`

## 模組化優勢

### 1. 可重用性
- 每個模組可獨立使用
- 支援不同組合配置
- 便於功能擴展

### 2. 維護性
- 單一模組故障不影響整體
- 易於除錯與更新
- 清晰的職責分離

### 3. 擴展性
- 新增功能只需添加模組
- 支援動態組合
- 便於 A/B 測試

### 4. 測試性
- 單元測試友好
- 模組間解耦
- 易於 mock 測試

## 模組化設計原則

### 1. 單一職責
- 每個模組專注單一功能
- 避免功能重疊
- 清晰的輸入輸出

### 2. 標準化介面
- 統一的資料格式
- 一致的錯誤處理
- 標準化的回應結構

### 3. 可配置性
- 支援參數調整
- 動態功能開關
- 靈活的組合方式

## 未來擴展方向

### 1. 新增模組類型
- 技術指標分析模組
- 法人籌碼分析模組
- 產業輪動分析模組

### 2. 智能組合
- AI 驅動的模組選擇
- 根據問題類型動態組合
- 個性化回應配置

### 3. 效能優化
- 並行執行模組
- 快取機制
- 資源管理優化 