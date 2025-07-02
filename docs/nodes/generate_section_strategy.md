# generate_section_strategy.py

## 功能說明

本模組負責生成不同投資時期的策略建議，結合新聞摘要、財務資料和市場分析，為投資者提供日內交易、短線交易、中線投資和長線投資的具體建議。支援多種投資策略分析，包括技術面、消息面、基本面等維度的綜合評估。

## 主要功能

### 核心流程
1. **資料整合** - 整合新聞摘要、財務資料和市場資訊
2. **策略分析** - 分析四個投資時期的策略建議
3. **來源映射** - 將策略建議與實際新聞來源關聯
4. **風險評估** - 評估不同策略的風險和信心度
5. **建議生成** - 生成結構化的投資策略報告

## 主要函數

### `generate_strategy_section(company_name: str, stock_id: str, news_summary: str, financial_data: Dict = None, news_sources: List[Dict] = None) -> Dict`

**功能**: 主要的投資策略生成函數

**參數**:
- `company_name`: 公司名稱
- `stock_id`: 股票代碼
- `news_summary`: 新聞摘要
- `financial_data`: 財務資料（可選）
- `news_sources`: 新聞來源列表（可選）

**回傳值**:
```python
{
    "success": bool,
    "section": Dict  # 包含策略建議的完整結構
}
```

## 投資時期分類

### 1. 日內交易（1天內）
- **特點**: 快速進出，高頻交易
- **重點**: 技術面分析、盤勢波動、即時消息
- **風險**: 高風險，需要密切關注市場動態

### 2. 短線交易（1週內）
- **特點**: 短期持有，趨勢跟隨
- **重點**: 支撐壓力位、短期趨勢、法人動向
- **風險**: 中等風險，需要技術分析能力

### 3. 中線投資（1個月內）
- **特點**: 中期持有，產業趨勢
- **重點**: 產業發展、政策變化、基本面改善
- **風險**: 中等風險，需要產業分析能力

### 4. 長線投資（1季以上）
- **特點**: 長期持有，價值投資
- **重點**: 長期發展、基本面穩健、成長潛力
- **風險**: 相對較低，適合穩健投資者

## 分析維度

### 技術面分析
- **內容**: 股價走勢、技術指標、支撐壓力位
- **來源**: 技術分析報告、盤後分析
- **應用**: 日內交易、短線交易

### 消息面分析
- **內容**: 即時新聞、市場傳聞、法人動向
- **來源**: 財經新聞、外資報告
- **應用**: 所有投資時期

### 基本面分析
- **內容**: 財務報表、營收成長、獲利能力
- **來源**: 財報分析、產業報告
- **應用**: 中線投資、長線投資

## OpenAI Prompt 設計

### 主要 Prompt 結構
```python
prompt = f"""
你是一位專業的投資分析師，請根據以下資訊，為 {company_name}({stock_id}) 產生投資策略建議。

請分析以下四個投資時期的策略：
1. 日內交易（1天內）
2. 短線交易（1週內）
3. 中線投資（1個月內）
4. 長線投資（1季以上）

新聞摘要：
{news_summary}

財務摘要：
{financial_summary}

{source_references}

請回傳 JSON 格式如下，每個句子都要有自己的 sources 陣列：
{{
  "section": "不同投資型態的投資策略建議",
  "cards": [
    {{
      "title": "日內交易",
      "content": [
        {{
          "text": "根據技術面和消息面分析，建議日內交易時留意{company_name}({stock_id})的盤勢波動，可考慮在適當時機進行快速交易。",
          "sources": [
            {{"title": "技術面分析", "link": "https://example.com/tech"}},
            {{"title": "消息面分析", "link": "https://example.com/news"}}
          ]
        }}
      ]
    }}
  ]
}}
"""
```

### Prompt 特色
- **結構化輸出**: 要求 JSON 格式回應
- **來源關聯**: 每個建議都需標註來源
- **多維度分析**: 涵蓋技術面、消息面、基本面
- **風險提醒**: 包含風險評估和注意事項

## 資料結構

### 財務資料結構
```python
financial_data = {
    "eps": {
        "2024Q1": {
            "eps": "15.2",
            "quarterly_growth": "12.5%"
        }
    },
    "revenue": {
        "2024Q1": {
            "revenue": "500000",
            "quarterly_growth": "8.3%"
        }
    }
}
```

### 新聞來源結構
```python
news_sources = [
    {
        "title": "台積電財報亮眼",
        "link": "https://example.com/news1"
    },
    {
        "title": "外資持續買超",
        "link": "https://example.com/news2"
    }
]
```

## 輸出格式

### 完整回應結構
```python
{
    "success": True,
    "section": {
        "section": "不同投資型態的投資策略建議",
        "cards": [
            {
                "title": "日內交易",
                "content": [
                    {
                        "text": "根據技術面和消息面分析，建議日內交易時留意台積電(2330)的盤勢波動，可考慮在適當時機進行快速交易。",
                        "sources": [
                            {"title": "技術面分析", "link": "https://example.com/tech"},
                            {"title": "消息面分析", "link": "https://example.com/news"}
                        ]
                    }
                ]
            }
        ],
        "summary_table": [
            {
                "period": "1天",
                "suggestion": "根據技術面分析，快速交易",
                "confidence": "中等",
                "reason": "市場波動大"
            }
        ]
    }
}
```

## 輸入/輸出範例

### 輸入範例
```python
company_name = "台積電"
stock_id = "2330"
news_summary = "台積電公布最新財報，營收創新高，外資持續買超..."
financial_data = {
    "eps": {"2024Q1": {"eps": "15.2", "quarterly_growth": "12.5%"}},
    "revenue": {"2024Q1": {"revenue": "500000", "quarterly_growth": "8.3%"}}
}
news_sources = [
    {"title": "台積電財報亮眼", "link": "https://example.com/news1"},
    {"title": "外資持續買超", "link": "https://example.com/news2"}
]
```

### 輸出範例
```python
{
    "success": True,
    "section": {
        "section": "不同投資型態的投資策略建議",
        "cards": [
            {
                "title": "日內交易",
                "content": [
                    {
                        "text": "根據技術面和消息面分析，建議日內交易時留意台積電(2330)的盤勢波動，可考慮在適當時機進行快速交易。",
                        "sources": [
                            {"title": "台積電財報亮眼", "link": "https://example.com/news1"},
                            {"title": "外資持續買超", "link": "https://example.com/news2"}
                        ]
                    },
                    {
                        "text": "**技術面**：根據盤後分析，台積電(2330)有特定買盤介入，可能帶動盤勢波動。",
                        "sources": [
                            {"title": "盤後分析報告", "link": "https://example.com/after-hours"}
                        ]
                    }
                ]
            },
            {
                "title": "短線交易",
                "content": [
                    {
                        "text": "根據短期趨勢分析，建議短線交易時關注台積電(2330)的支撐壓力位，可考慮在適當位置進行交易。",
                        "sources": [
                            {"title": "短期趨勢分析", "link": "https://example.com/short-term"}
                        ]
                    }
                ]
            }
        ],
        "summary_table": [
            {"period": "1天", "suggestion": "根據技術面分析，快速交易", "confidence": "中等", "reason": "市場波動大"},
            {"period": "1週", "suggestion": "關注支撐壓力", "confidence": "中等", "reason": "短期趨勢"},
            {"period": "1個月", "suggestion": "分批布局", "confidence": "中等", "reason": "中期發展"},
            {"period": "1季+", "suggestion": "長期持有", "confidence": "中等", "reason": "基本面穩健"}
        ]
    }
}
```

## 錯誤處理

### 常見錯誤
1. **OpenAI API 失敗**
   - 原因: API 金鑰無效或網路連線問題
   - 處理: 回傳錯誤訊息

2. **JSON 解析失敗**
   - 原因: LLM 回傳格式不正確
   - 處理: 使用預設策略建議

3. **資料缺失**
   - 原因: 財務資料或新聞來源不足
   - 處理: 使用可用的資料生成建議

### 錯誤回應範例
```python
{
    "success": False,
    "section": {},
    "error": "OpenAI API 連線失敗"
}
```

## 效能考量

### 執行時間
- **一般情況**: 5-8 秒
- **主要耗時**: OpenAI API 呼叫
- **優化策略**: 使用 GPT-3.5-turbo 模型

### API 限制
- **OpenAI API**: 有呼叫次數和速率限制
- **建議使用**: 合理控制策略生成頻率

## 擴展性

### 可能的擴展功能
1. **更多投資時期** - 加入更多時間週期
2. **風險評分** - 量化風險評估
3. **策略回測** - 歷史策略表現分析
4. **個人化建議** - 根據投資者偏好調整

### 擴展範例
```python
# 加入風險評分
def calculate_risk_score(strategy_data: Dict) -> float:
    """計算策略風險評分"""
    risk_factors = {
        "日內交易": 0.8,
        "短線交易": 0.6,
        "中線投資": 0.4,
        "長線投資": 0.2
    }
    
    total_score = 0
    for card in strategy_data.get("cards", []):
        period = card.get("title", "")
        if period in risk_factors:
            total_score += risk_factors[period]
    
    return total_score / len(strategy_data.get("cards", []))
```

## 測試

### 單元測試
```python
def test_strategy_generation():
    result = generate_strategy_section("台積電", "2330", "測試新聞摘要")
    
    assert result["success"] == True
    assert "section" in result
    assert "cards" in result["section"]
    assert len(result["section"]["cards"]) == 4
```

### 整合測試
```python
# 測試完整流程
python test_watchlist.py
```

## 相關模組

### 依賴模組
- `openai` - OpenAI API 客戶端
- `json` - JSON 處理
- `re` - 正則表達式

### 使用模組
- `generate_watchlist_summary_pipeline.py` - 投資組合摘要 (使用策略建議)

## 設計原則

### 1. 多維度分析
- 技術面、消息面、基本面綜合評估
- 不同投資時期的差異化建議
- 風險和收益的平衡考量

### 2. 來源可追溯
- 每個建議都有明確的資料來源
- 支援來源連結和參考
- 提高建議的可信度

### 3. 結構化輸出
- 統一的 JSON 格式
- 清晰的卡片式結構
- 便於前端展示和處理

### 4. 風險管理
- 明確的風險提醒
- 不同策略的風險評估
- 適合不同風險承受度的投資者 