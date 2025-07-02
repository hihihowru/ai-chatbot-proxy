# generate_watchlist_summary_pipeline.py

## 功能說明

`generate_watchlist_summary_pipeline.py` 是自選股摘要功能的整合 Pipeline，負責協調各個分析模組，產生完整的自選股分析報告。此模組能夠：

1. **整合多個分析模組**：協調產業分布、股價摘要、報酬率分析、焦點個股等模組
2. **資料流管理**：確保各模組間的資料正確傳遞
3. **錯誤處理**：單一模組失敗不影響整體流程
4. **日誌記錄**：詳細記錄每個步驟的執行狀況
5. **標準化輸出**：統一所有模組的輸出格式

## 主要函數

### `generate_watchlist_summary_pipeline(stock_list: List[int]) -> Dict[str, Any]`
- **功能**：產生自選股摘要的完整 pipeline
- **參數**：
  - `stock_list`: 自選股清單（數字列表）
- **返回**：包含 success、sections、logs 的字典

## 處理流程

### 步驟 1：產生產業分布統計
- **模組**：`generate_industry_distribution_section`
- **功能**：統計自選股的產業分布
- **輸出**：產業分布統計 section

### 步驟 1.5：產生自選股 vs 同產業指數表現
- **模組**：`generate_industry_comparison_section`
- **功能**：比較自選股與同產業指數的表現
- **輸出**：產業比較 section

### 步驟 2：產生股價摘要
- **模組**：`generate_price_summary_section`
- **功能**：計算各股票的報酬率並以表格呈現
- **輸出**：股價摘要 section + 股價資料（供後續使用）

### 步驟 3：產生報酬率統計分析
- **模組**：`generate_return_analysis_section`
- **功能**：分析整體報酬率統計資料
- **輸入**：步驟 2 的股價資料
- **輸出**：報酬率統計分析 section

### 步驟 4：產生異動焦點個股
- **模組**：`generate_focus_stocks_section`
- **功能**：搜尋每檔股票的最新消息並產生摘要
- **輸入**：股票清單 + 股價資料
- **輸出**：異動焦點個股 section

### 步驟 5：添加資料來源
- **功能**：添加資料來源說明
- **內容**：Finlab 台股資料庫、Serper API 等

### 步驟 6：添加免責聲明
- **功能**：添加投資免責聲明
- **內容**：標準的投資風險提醒

## 資料流設計

```
股票清單 → 產業分布統計
         → 產業比較分析
         → 股價摘要 → 股價資料
                   → 報酬率統計分析
         → 異動焦點個股
         → 資料來源
         → 免責聲明
```

## Input/Output 範例

### 輸入範例
```python
stock_list = [2303, 2330, 2610, 2376, 2317]
```

### 輸出範例
```json
{
  "success": true,
  "sections": [
    {
      "title": "產業分布統計",
      "content": "🏷️ 產業分布統計\n\t•\t電子（半導體、PC）：5 檔",
      "cards": [...],
      "sources": [...]
    },
    {
      "title": "自選股 vs 同產業指數表現",
      "content": "📊 自選股與同產業指數比較...",
      "cards": [...],
      "sources": [...]
    },
    {
      "title": "股價摘要",
      "content": "📈 股價摘要\n股票代號\t收盤價\t漲跌幅...",
      "cards": [...],
      "sources": [...]
    },
    {
      "title": "報酬率統計分析",
      "content": "📊 報酬率統計\n上漲家數：3 檔...",
      "cards": [...],
      "sources": [...]
    },
    {
      "title": "異動焦點個股",
      "content": "🎯 異動焦點個股\n台積電 (2330)...",
      "cards": [...],
      "sources": [...]
    },
    {
      "title": "資料來源",
      "content": "本報告資料來源包括：\n• Finlab 台股資料庫\n• Serper API 搜尋結果",
      "cards": [...],
      "sources": [...]
    },
    {
      "title": "免責聲明",
      "content": "本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險。",
      "cards": [...],
      "sources": []
    }
  ],
  "logs": [
    "步驟 1: 產生產業分布統計",
    "步驟 1.5: 產生自選股 vs 同產業指數表現",
    "步驟 2: 產生股價摘要",
    "步驟 3: 產生報酬率統計分析",
    "步驟 4: 產生異動焦點個股",
    "步驟 5: 添加資料來源",
    "步驟 6: 添加免責聲明"
  ]
}
```

## 錯誤處理機制

### 單一模組失敗
- 記錄錯誤訊息到 logs
- 繼續執行後續模組
- 不影響整體流程

### 資料依賴處理
- 股價摘要失敗時，跳過報酬率統計分析
- 確保資料正確傳遞給後續模組

### 異常處理
- 捕獲所有異常並記錄
- 返回錯誤訊息和已完成的 sections

## 模組依賴關係

```
generate_industry_distribution_section
    ↓
generate_industry_comparison_section
    ↓
generate_price_summary_section → price_data
    ↓
generate_return_analysis_section (需要 price_data)
    ↓
generate_focus_stocks_section (需要 price_data)
    ↓
資料來源 + 免責聲明
```

## 擴充性設計

### 新增分析模組
1. 在對應位置添加新的模組調用
2. 確保輸出格式符合 section 標準
3. 更新日誌記錄

### 調整執行順序
- 可根據需要調整步驟順序
- 注意資料依賴關係

### 自訂輸出格式
- 所有 section 都遵循統一的格式
- 包含 title、content、cards、sources

## 測試

### 測試腳本
```python
test_stock_list = [2303, 2330, 2610, 2376, 2317]
result = generate_watchlist_summary_pipeline(test_stock_list)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 測試重點
- 各模組是否正確執行
- 資料流是否正確傳遞
- 錯誤處理是否有效
- 輸出格式是否標準化 