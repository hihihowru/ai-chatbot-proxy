# summarize.py

## 功能說明

`summarize.py` 是摘要生成模組，專門用於對股票分析資料進行智能摘要，將複雜的資料轉換為簡潔易懂的摘要內容。此模組能夠：

1. **資料摘要**：將大量的股票分析資料濃縮為關鍵資訊
2. **重點提取**：識別並突出重要的分析結果
3. **語言優化**：將技術性資料轉換為自然語言描述
4. **結構化輸出**：提供格式化的摘要內容
5. **可擴充性**：支援不同類型的資料摘要需求

## 主要函數

### `summarize(data: dict) -> dict`
- **功能**：對輸入的資料進行摘要處理
- **參數**：
  - `data`: 包含股票分析資料的字典
- **邏輯**：
  1. 接收分析資料
  2. 提取關鍵資訊
  3. 生成結構化摘要
  4. 返回摘要結果
- **返回**：包含摘要內容的字典

## 當前狀態

### 實作狀態
```python
def summarize(data: dict) -> dict:
    # TODO: Implement summarization
    return {"summary": "summary_placeholder"}
```

### 待實作功能
- 資料解析和驗證
- 關鍵資訊提取
- 摘要生成邏輯
- 語言優化處理
- 錯誤處理機制

## 設計原則

### 1. 模組化設計
- 將摘要功能獨立為單一模組
- 提供清晰的輸入輸出介面
- 支援不同資料類型的處理

### 2. 可擴充性
- 支援新增摘要類型
- 可自訂摘要長度和格式
- 支援多語言摘要生成

### 3. 效能優化
- 高效處理大量資料
- 最小化記憶體使用
- 提供快取機制

### 4. 錯誤處理
- 處理無效資料輸入
- 提供預設摘要內容
- 記錄處理錯誤

## 預期功能

### 1. 資料類型支援

#### 技術分析摘要
```python
# 輸入資料格式
{
    "chart_type": "技術分析",
    "data": {
        "indicators": ["KD", "MACD", "RSI"],
        "signals": ["買入", "賣出", "觀望"],
        "trend": "上升趨勢"
    }
}

# 預期輸出
{
    "summary": "台積電技術分析顯示上升趨勢，KD指標顯示買入信號，MACD和RSI指標中性。"
}
```

#### 籌碼分析摘要
```python
# 輸入資料格式
{
    "chart_type": "籌碼分析",
    "data": {
        "foreign_buy": 1000000,
        "foreign_sell": 500000,
        "institutional_buy": 800000,
        "institutional_sell": 300000
    }
}

# 預期輸出
{
    "summary": "外資買超100萬股，投信買超80萬股，法人動向偏多。"
}
```

#### 基本面摘要
```python
# 輸入資料格式
{
    "chart_type": "基本面",
    "data": {
        "eps": 15.2,
        "pe_ratio": 18.5,
        "revenue_growth": 0.15,
        "profit_growth": 0.12
    }
}

# 預期輸出
{
    "summary": "EPS為15.2元，本益比18.5倍，營收成長15%，獲利成長12%。"
}
```

### 2. 摘要生成策略

#### 關鍵指標提取
- 識別最重要的分析指標
- 提取數值變化趨勢
- 突出異常或重要信號

#### 語言優化
- 將技術術語轉換為易懂語言
- 使用自然語言描述趨勢
- 提供客觀的分析觀點

#### 結構化輸出
- 按重要性排序資訊
- 提供清晰的段落結構
- 支援不同長度的摘要

### 3. 自訂選項

#### 摘要長度
```python
# 短摘要（1-2句）
"台積電技術面偏多，法人買超。"

# 中摘要（3-5句）
"台積電技術分析顯示上升趨勢，KD指標顯示買入信號，外資買超100萬股，基本面穩健。"

# 長摘要（詳細分析）
"台積電技術分析顯示明確的上升趨勢，KD指標在20以下顯示超賣後反彈，MACD指標金叉向上..."
```

#### 重點方向
- 技術面重點
- 籌碼面重點
- 基本面重點
- 綜合分析重點

## 擴充性設計

### 1. 新增摘要類型
```python
# 支援新的圖表類型
SUMMARIZE_TYPES = {
    "技術分析": TechnicalSummarizer(),
    "籌碼分析": InstitutionalSummarizer(),
    "基本面": FundamentalSummarizer(),
    "新聞": NewsSummarizer(),
    "比較分析": ComparisonSummarizer(),
    "趨勢分析": TrendSummarizer()
}
```

### 2. 自訂摘要器
```python
class CustomSummarizer:
    def __init__(self, config: dict):
        self.config = config
    
    def summarize(self, data: dict) -> dict:
        # 自訂摘要邏輯
        pass
```

### 3. 多語言支援
```python
# 支援不同語言
LANGUAGE_SUPPORT = {
    "zh_TW": TraditionalChineseSummarizer(),
    "zh_CN": SimplifiedChineseSummarizer(),
    "en": EnglishSummarizer()
}
```

## 使用場景

### 1. 快速概覽
- 提供股票分析的快速摘要
- 幫助用戶快速了解重點
- 節省閱讀時間

### 2. 報告生成
- 自動生成分析報告摘要
- 提供結構化的報告內容
- 支援不同格式的輸出

### 3. 比較分析
- 多股票分析的摘要比較
- 突出差異和相似點
- 提供客觀的比較結果

### 4. 決策支援
- 提供投資決策的關鍵資訊
- 突出風險和機會
- 支援理性投資決策

## 實作建議

### 1. 第一階段實作
```python
def summarize(data: dict) -> dict:
    """基礎摘要功能"""
    try:
        chart_type = data.get("chart_type", "unknown")
        
        if chart_type == "技術分析":
            return summarize_technical(data)
        elif chart_type == "籌碼分析":
            return summarize_institutional(data)
        elif chart_type == "基本面":
            return summarize_fundamental(data)
        else:
            return {"summary": "暫無摘要"}
            
    except Exception as e:
        return {"summary": f"摘要生成失敗: {str(e)}"}
```

### 2. 第二階段實作
- 新增更多摘要類型
- 實作語言優化功能
- 加入自訂選項支援

### 3. 第三階段實作
- 實作多語言支援
- 加入機器學習摘要
- 提供進階自訂功能

## 測試策略

### 1. 單元測試
```python
def test_summarize_technical():
    data = {
        "chart_type": "技術分析",
        "data": {"trend": "上升", "signal": "買入"}
    }
    result = summarize(data)
    assert "上升" in result["summary"]
    assert "買入" in result["summary"]
```

### 2. 整合測試
- 測試不同資料類型的摘要
- 驗證摘要品質和準確性
- 測試錯誤處理機制

### 3. 效能測試
- 測試大量資料的處理效能
- 驗證記憶體使用情況
- 測試並發處理能力

## 未來發展

### 1. AI 摘要
- 使用自然語言處理技術
- 實作智能摘要生成
- 提供個性化摘要內容

### 2. 即時摘要
- 支援即時資料摘要
- 提供動態摘要更新
- 實作推播摘要功能

### 3. 互動式摘要
- 支援用戶自訂摘要重點
- 提供摘要深度調整
- 實作摘要反饋機制 