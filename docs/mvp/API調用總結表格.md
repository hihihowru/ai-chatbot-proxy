# API 調用總結表格

## 個股分析流程 API 調用詳解

| 階段 | 架構位置 | OpenAI API 次數 | Serper API 次數 | 目的 | 節點名稱 |
|------|----------|-----------------|-----------------|------|----------|
| **前段 - 語意分析** | 問題理解 | 1 次 | - | 意圖分類與資訊提取 | `classify_and_extract` |
| **中段 - 資料庫調用** | 新聞搜尋 | - | 8-12 次 | 相關新聞搜尋 | `search_news` |
| **後段 - 摘要回覆** | 新聞摘要 | 1 次 | - | 搜尋結果摘要 | `summarize_results` |
| **後段 - 摘要回覆** | 投資策略建議 | 1 次 | - | 不同投資型態策略 | `generate_section_strategy` |
| **後段 - 摘要回覆** | 資料來源整理 | 1 次 | - | 分析結論資料來源 | `summarize_results` (資料來源) |
| **後段 - 摘要回覆** | 報告生成 | 1 次 | - | 最終分析報告 | `generate_report` |
| **總計** | **完整流程** | **5 次** | **8-12 次** | **完整分析流程** | **6 個節點** |

### 個股分析詳細說明

**前段 - 語意分析階段**
- **節點**: `classify_and_extract`
- **OpenAI API**: 1 次
- **目的**: 理解用戶問題，提取股票代號、公司名稱、時間資訊
- **輸出**: 結構化分類結果

**中段 - 資料庫調用階段**
- **節點**: `search_news`
- **Serper API**: 8-12 次
- **目的**: 搜尋相關新聞和市場資訊
- **策略**: 每個關鍵字調用 1 次 API
- **關鍵字範例**: "台積電 2330 財報", "台積電 外資買賣", "2330 法人動向"

**後段 - 摘要回覆階段**
- **節點1**: `summarize_results` (1 次 OpenAI API) - 新聞摘要
- **節點2**: `generate_section_strategy` (1 次 OpenAI API) - 投資策略建議
- **節點3**: `summarize_results` (1 次 OpenAI API) - 資料來源整理
- **節點4**: `generate_report` (1 次 OpenAI API) - 最終分析報告

---

## 自選股摘要分析流程 API 調用詳解

| 階段 | 架構位置 | OpenAI API 次數 | Serper API 次數 | 目的 | 節點名稱 |
|------|----------|-----------------|-----------------|------|----------|
| **前段 - 語意分析** | 產業分布統計 | 1 次 | - | 產業分布分析 | `generate_section_industry_distribution` |
| **前段 - 語意分析** | 產業比較分析 | 1 次 | - | 產業表現比較 | `generate_section_industry_comparison` |
| **中段 - 資料庫調用** | 股價摘要分析 | 1 次 | - | 報酬率統計分析 | `generate_section_price_summary` |
| **中段 - 資料庫調用** | 報酬率統計 | 1 次 | - | 整體報酬率分析 | `generate_section_return_analysis` |
| **中段 - 資料庫調用** | 新聞搜尋 | - | 8-12 次 | 相關新聞搜尋 | `search_news` |
| **後段 - 摘要回覆** | 焦點個股分析 | 2-3 次 | - | 重點股票分析 | `generate_section_focus_stocks` |
| **後段 - 摘要回覆** | 資料來源整理 | 1 次 | - | 分析結論資料來源 | `generate_watchlist_summary_pipeline` |
| **總計** | **完整流程** | **7-8 次** | **8-12 次** | **完整分析流程** | **8 個節點** |

### 自選股摘要詳細說明

**前段 - 語意分析階段**
- **節點1**: `generate_section_industry_distribution` (1 次 OpenAI API)
- **節點2**: `generate_section_industry_comparison` (1 次 OpenAI API)
- **目的**: 分析自選股的產業分布和比較

**中段 - 資料庫調用階段**
- **節點1**: `generate_section_price_summary` (1 次 OpenAI API) - 股價摘要
- **節點2**: `generate_section_return_analysis` (1 次 OpenAI API) - 報酬率統計
- **節點3**: `search_news` (8-12 次 Serper API) - 新聞搜尋

**後段 - 摘要回覆階段**
- **節點1**: `generate_section_focus_stocks` (2-3 次 OpenAI API) - 焦點個股分析
- **節點2**: `generate_watchlist_summary_pipeline` (1 次 OpenAI API) - 資料來源整理

---

## 成本分析總結

### 個股分析流程成本
- **OpenAI API**: 5 次 × $0.01 = **$0.05**
- **Serper API**: 10 次 × $0.001 = **$0.01**
- **總成本**: **$0.06/次**
- **執行時間**: 15-20 秒

### 自選股摘要分析流程成本
- **OpenAI API**: 7.5 次 × $0.01 = **$0.075**
- **Serper API**: 10 次 × $0.001 = **$0.01**
- **總成本**: **$0.085/次**
- **執行時間**: 30-40 秒

### 成本效益分析
- **個股分析**: 高性價比，適合快速查詢
- **自選股摘要**: 深度分析，適合投資組合管理
- **建議**: 根據用戶需求智能路由，避免不必要的 API 調用

---

## 優化建議

### 1. 快取機制
- 實施 Redis 快取，減少重複 API 調用
- 快取時間：新聞資料 1 小時，股價資料 5 分鐘

### 2. 並行處理
- 將獨立的 API 調用並行執行
- 預估可縮短 30-40% 執行時間

### 3. 智能路由
- 根據問題複雜度調整 API 調用次數
- 簡單問題跳過部分分析步驟

### 4. 批次處理
- 自選股分析可批次處理多檔股票
- 減少重複的產業分析調用 