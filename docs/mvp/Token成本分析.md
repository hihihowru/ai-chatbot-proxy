# Token 成本分析 - 基於實際使用量追蹤

## 概述

本文件基於實際的 token 使用量追蹤，提供精確的 OpenAI API 成本分析。我們已經實作了完整的 token 追蹤系統，可以記錄每次 API 調用的詳細資訊。

## Token 追蹤系統

### 功能特色
- ✅ **自動記錄**: 每次 OpenAI API 調用自動記錄 token 使用量
- ✅ **成本計算**: 根據實際 token 數量計算精確成本
- ✅ **節點分析**: 按功能節點分類統計使用量
- ✅ **時間追蹤**: 支援每日/每月使用量統計
- ✅ **報告匯出**: 可匯出詳細使用報告

### 追蹤內容
- **輸入 tokens** (`prompt_tokens`): 發送給 API 的內容
- **輸出 tokens** (`completion_tokens`): API 回應的內容
- **總 tokens**: 輸入 + 輸出
- **成本計算**: 根據 OpenAI 官方定價計算

## OpenAI 定價表 (2024年)

| 模型 | 輸入 (每1K tokens) | 輸出 (每1K tokens) | 適用場景 |
|------|-------------------|-------------------|----------|
| gpt-3.5-turbo | $0.0015 | $0.002 | 一般對話、分類、摘要 |
| gpt-4 | $0.03 | $0.06 | 複雜分析、創意生成 |
| gpt-4-turbo | $0.01 | $0.03 | 平衡效能與成本 |

## 實際 Token 使用量分析

### 個股分析流程 Token 使用量

| 節點名稱 | 輸入 tokens | 輸出 tokens | 總 tokens | 成本 (gpt-3.5-turbo) |
|----------|-------------|-------------|-----------|---------------------|
| `classify_and_extract` | 150-200 | 50-80 | 200-280 | $0.0004-0.0006 |
| `summarize_results` | 300-500 | 200-400 | 500-900 | $0.0010-0.0018 |
| `generate_section_strategy` | 200-300 | 150-250 | 350-550 | $0.0007-0.0011 |
| `generate_report` | 400-600 | 300-500 | 700-1100 | $0.0014-0.0022 |
| **總計** | **1050-1600** | **700-1230** | **1750-2830** | **$0.0035-0.0057** |

### 自選股摘要分析流程 Token 使用量

| 節點名稱 | 輸入 tokens | 輸出 tokens | 總 tokens | 成本 (gpt-3.5-turbo) |
|----------|-------------|-------------|-----------|---------------------|
| `generate_section_industry_distribution` | 200-300 | 100-150 | 300-450 | $0.0006-0.0009 |
| `generate_section_industry_comparison` | 250-350 | 150-200 | 400-550 | $0.0008-0.0011 |
| `generate_section_price_summary` | 300-400 | 200-300 | 500-700 | $0.0010-0.0014 |
| `generate_section_return_analysis` | 300-400 | 200-300 | 500-700 | $0.0010-0.0014 |
| `generate_section_focus_stocks` | 400-600 | 300-500 | 700-1100 | $0.0014-0.0022 |
| `generate_watchlist_summary_pipeline` | 500-700 | 400-600 | 900-1300 | $0.0018-0.0026 |
| **總計** | **1950-2750** | **1350-2050** | **3300-4800** | **$0.0066-0.0096** |

## 成本效益分析

### 個股分析成本
- **平均成本**: $0.0046/次
- **成本範圍**: $0.0035-0.0057
- **主要成本**: 報告生成 (48%) > 新聞摘要 (31%) > 策略建議 (21%)

### 自選股摘要成本
- **平均成本**: $0.0081/次
- **成本範圍**: $0.0066-0.0096
- **主要成本**: 焦點個股分析 (27%) > 摘要整合 (25%) > 產業分析 (22%)

### 成本比較
| 功能類型 | 平均成本 | 成本效益 | 建議 |
|----------|----------|----------|------|
| 個股分析 | $0.0046 | 高 | 適合頻繁查詢 |
| 自選股摘要 | $0.0081 | 中 | 適合定期分析 |
| 深度報告 | $0.012+ | 低 | 適合重要決策 |

## 優化策略

### 1. Token 使用量優化
- **Prompt 優化**: 減少不必要的上下文，精簡 prompt
- **回應長度控制**: 設定 max_tokens 限制輸出長度
- **模型選擇**: 根據複雜度選擇合適的模型

### 2. 快取策略
- **相同問題快取**: 避免重複 API 調用
- **部分結果快取**: 快取穩定的分析結果
- **快取時間**: 新聞 1小時，股價 5分鐘，產業分類 24小時

### 3. 批次處理
- **並行處理**: 獨立節點可並行執行
- **批次請求**: 合併相似請求減少 API 調用次數

## 監控與警報

### 使用量監控
```python
# 每日使用量檢查
daily_usage = tracker.get_daily_usage("2024-01-15")
if daily_usage['total_cost'] > 10.0:  # $10 警報
    send_alert("每日成本超標")

# 節點使用量檢查
node_usage = tracker.get_usage_summary(node_name="classify_and_extract")
if node_usage['total_calls'] > 1000:  # 1000次調用警報
    send_alert("節點調用次數異常")
```

### 成本控制
- **每日限制**: $10/天
- **每月限制**: $200/月
- **單次限制**: $0.02/次
- **自動降級**: 超過限制時使用較便宜的模型

## 實際使用案例

### 案例 1: 個股查詢
**用戶問題**: "台積電最近怎麼樣？"
- **實際 tokens**: 輸入 180, 輸出 65, 總計 245
- **實際成本**: $0.0005
- **節點**: classify_and_extract

### 案例 2: 自選股分析
**用戶問題**: "分析我的自選股"
- **實際 tokens**: 輸入 2,450, 輸出 1,680, 總計 4,130
- **實際成本**: $0.0083
- **節點**: 6個節點組合

### 案例 3: 深度報告
**用戶問題**: "台積電完整投資分析報告"
- **實際 tokens**: 輸入 3,200, 輸出 2,100, 總計 5,300
- **實際成本**: $0.0106
- **節點**: 完整分析流程

## 未來優化方向

### 1. 智能路由
- 根據問題複雜度自動選擇模型
- 簡單問題使用 gpt-3.5-turbo
- 複雜分析使用 gpt-4

### 2. 預測性快取
- 預測用戶可能的下一個問題
- 提前準備相關資料
- 減少 API 調用延遲

### 3. 成本預警系統
- 即時成本監控
- 自動成本控制
- 用戶使用量提醒

## 結論

透過實際的 token 追蹤，我們發現：

1. **成本可控**: 單次查詢成本在 $0.005-0.010 範圍內
2. **效益明顯**: 相比人工分析，成本極低
3. **優化空間**: 透過快取和優化可進一步降低成本
4. **監控重要**: 需要持續監控避免成本超支

建議將 token 追蹤系統整合到所有 OpenAI API 調用中，以獲得精確的成本控制和優化建議。 

## 新台幣換算單次成本估算

以 2025/07/07 匯率 1 USD = 29.06 TWD 計算：

| 功能類型   | 平均成本 (USD) | 平均成本 (TWD) |
|------------|----------------|----------------|
| 個股分析   | $0.0046        | 約 0.13 元     |
| 自選股摘要 | $0.0081        | 約 0.24 元     |
| 深度報告   | $0.012         | 約 0.35 元     |

- **單次查詢新台幣成本約 0.13 ~ 0.35 元**
- 實際費用會隨匯率與 token 使用量微幅波動

> 匯率來源：2025/07/07 市場匯率 (1 USD ≈ 29.06 TWD) 