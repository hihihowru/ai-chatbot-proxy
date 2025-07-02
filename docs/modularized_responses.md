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
**模組化架構**：`investment_analysis_graph` + `generate_report_pipeline`
- **整合模組**：4 個核心節點 + 6 個 section 生成模組
- **功能範圍**：技術分析、基本面分析、新聞分析、投資策略
- **輸出格式**：結構化分析報告
- **檔案位置**：`langgraph_app/graphs/investment_analysis_graph.py`

**核心節點**：
- `classify_and_extract_node` - 問題理解與分類
- `search_news_node` - 新聞搜尋
- `summarize_results_node` - 結果摘要
- `generate_report_node` - 報告生成

**Section 生成模組**：
- `generate_section_price_movement.py` - 股價異動分析
- `generate_section_financial.py` - 財務狀況分析
- `generate_section_strategy.py` - 投資策略建議
- `generate_section_notice.py` - 投資注意事項
- `generate_section_sources.py` - 資料來源說明
- `generate_section_disclaimer.py` - 免責聲明

### 3. 投資摘要 (Investment Summary)
**模組化架構**：`investment_summary_graph`
- **整合模組**：摘要生成節點
- **功能範圍**：投資建議摘要、風險評估
- **輸出格式**：摘要報告
- **檔案位置**：`langgraph_app/graphs/investment_summary_graph.py`

## 未來回覆模組盤點計劃

### 第一階段：現有功能模組化盤點
**目標**：將現有的回覆功能完全模組化，建立標準化的架構

#### 1. 自選股摘要模組化 ✅
- [x] 產業分布統計
- [x] 產業比較分析
- [x] 股價摘要表格
- [x] 報酬率統計分析
- [x] 異動焦點個股
- [x] 智能新聞搜尋

#### 2. 個股分析模組化 ✅
- [x] 問題理解與分類
- [x] 新聞搜尋與摘要
- [x] 股價異動分析
- [x] 財務狀況分析
- [x] 投資策略建議
- [x] 投資注意事項

#### 3. 投資摘要模組化 ✅
- [x] 摘要生成節點
- [x] 風險評估模組

### 第二階段：新增功能模組化
**目標**：開發新的回覆功能並採用模組化架構

#### 1. 技術分析模組
- [ ] 技術指標計算
- [ ] 支撐壓力分析
- [ ] 趨勢線分析
- [ ] 成交量分析

#### 2. 法人籌碼分析模組
- [ ] 外資動向分析
- [ ] 投信動向分析
- [ ] 自營商動向分析
- [ ] 大戶籌碼分析

#### 3. 產業輪動分析模組
- [ ] 產業強弱分析
- [ ] 資金流向分析
- [ ] 題材發酵分析
- [ ] 輪動時機判斷

#### 4. 財報分析模組
- [ ] 季度財報分析
- [ ] 年度財報分析
- [ ] 財務比率分析
- [ ] 成長性分析

### 第三階段：智能組合與優化
**目標**：實現 AI 驅動的模組選擇與組合

#### 1. 智能模組選擇
- [ ] 根據問題類型自動選擇模組
- [ ] 動態組合不同模組
- [ ] 個性化回應配置

#### 2. 效能優化
- [ ] 並行執行模組
- [ ] 快取機制
- [ ] 資源管理優化

#### 3. 品質提升
- [ ] 模組間一致性檢查
- [ ] 回應品質評估
- [ ] 自動化測試

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

## 實施進度追蹤

### 已完成 ✅
- 自選股摘要：6 個子模組
- 個股分析：4 個核心節點 + 6 個 section 模組
- 投資摘要：1 個摘要模組

### 進行中 🔄
- 模組化架構優化
- 文件標準化
- 測試覆蓋率提升

### 計劃中 📋
- 技術分析模組
- 法人籌碼分析模組
- 產業輪動分析模組
- 智能組合系統 