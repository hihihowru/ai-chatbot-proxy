# generate_section_social_sentiment.py

## 功能說明

本模組負責分析股票在社群媒體和討論區的輿情，透過爬取 CMoney 同學會討論區的貼文，結合 OpenAI GPT 進行情感分析，為投資決策提供社群輿情參考。支援多種情感分析策略，包括正面、負面、中立情感分類，以及熱門話題識別。

## 主要功能

### 核心流程
1. **社群爬取** - 爬取 CMoney 同學會討論區貼文
2. **內容解析** - 解析貼文標題、內容、時間、留言數
3. **情感分析** - 使用 OpenAI GPT 分析貼文情感傾向
4. **熱門話題** - 識別討論熱度高的話題
5. **輿情總結** - 生成社群輿情分析報告

## 主要函數

### `generate_social_sentiment_section(company_name: str, stock_id: str) -> Dict`

**功能**: 主要的社群情感分析函數

**參數**:
- `company_name`: 公司名稱
- `stock_id`: 股票代碼

**回傳值**:
```python
{
    "success": bool,
    "section_title": str,
    "section_content": str,
    "sentiment_summary": Dict,
    "hot_topics": List[str],
    "error": str
}
```

### `crawl_cmoney_forum(stock_id: str, company_name: str = "台積電") -> Dict`

**功能**: 爬取 CMoney 同學會討論區貼文

**特色**:
- 支援多種 HTML 選擇器
- 自動過濾無效內容
- 提取貼文詳細資訊
- 模擬瀏覽器行為

### `analyze_sentiment(text: str) -> str`

**功能**: 使用 OpenAI GPT 分析文字情感

**回傳值**:
- `"positive"` - 正面情感
- `"negative"` - 負面情感  
- `"neutral"` - 中立情感

## 社群平台支援

### CMoney 同學會討論區
- **URL 格式**: `https://www.cmoney.tw/forum/stock/{stock_id}`
- **內容類型**: 股票討論、投資心得、技術分析
- **資料結構**: 標題、內容、時間、留言數

### 爬取策略
```python
# 多種選擇器策略
selectors = [
    '.article-item',      # 文章項目
    '.post-item',         # 貼文項目
    '.discussion-item',   # 討論項目
    '.forum-post',        # 論壇貼文
    '.thread-item',       # 討論串項目
    'article',            # 文章標籤
    '.content-item',      # 內容項目
    '.post',              # 貼文
    '.discussion',        # 討論
]
```

## 情感分析

### OpenAI Prompt 設計
```python
PROMPT = '''請分析以下股票相關討論的情感傾向，並回傳以下其中一個答案：
- positive (正面/樂觀)
- negative (負面/悲觀)  
- neutral (中立/中性)

請根據以下內容進行判斷：
標題：{title}
內容：{content}

分析重點：
1. 投資者對該股票的態度
2. 對未來走勢的預期
3. 對公司基本面的看法
4. 技術分析的觀點

請只回傳一個英文單字：positive、negative 或 neutral'''
```

### 情感分析範例
```python
# 輸入
title = "台積電基本面分析"
content = "台積電的財報看起來不錯，營收成長穩定，長期投資應該有機會。"

# 輸出
"positive"

# 輸入
title = "台積電技術面觀察"
content = "從技術面來看，台積電目前處於整理階段，建議觀望一下再決定。"

# 輸出
"neutral"
```

## 資料結構

### 貼文結構
```python
{
    "title": str,           # 貼文標題
    "content": str,         # 貼文內容
    "time": str,            # 發布時間
    "reply_count": int,     # 留言數量
    "sentiment": str        # 情感分析結果
}
```

### 情感統計
```python
{
    "positive_count": int,  # 正面貼文數量
    "negative_count": int,  # 負面貼文數量
    "neutral_count": int,   # 中立貼文數量
    "total_posts": int,     # 總貼文數量
    "sentiment_ratio": float # 情感比例
}
```

## 輸出格式

### 完整回應結構
```python
{
    "success": True,
    "section_title": "社群輿情分析",
    "section_content": "根據 CMoney 同學會討論區的分析...",
    "sentiment_summary": {
        "positive_count": 5,
        "negative_count": 2,
        "neutral_count": 3,
        "total_posts": 10,
        "sentiment_ratio": 0.3
    },
    "hot_topics": [
        "基本面分析",
        "技術面觀察",
        "長期投資"
    ]
}
```

## 輸入/輸出範例

### 輸入範例
```python
company_name = "台積電"
stock_id = "2330"
```

### 輸出範例
```python
{
    "success": True,
    "section_title": "社群輿情分析",
    "section_content": """
## 社群輿情分析

根據 CMoney 同學會討論區的最新討論，台積電(2330)的社群輿情分析如下：

### 情感分布
- **正面情感**: 5 篇 (50%)
- **負面情感**: 2 篇 (20%)  
- **中立情感**: 3 篇 (30%)

### 熱門討論話題
1. **基本面分析** - 投資者關注財報表現和營收成長
2. **技術面觀察** - 討論股價走勢和技術指標
3. **長期投資** - 探討長期投資價值和策略

### 輿情總結
整體而言，社群對台積電持正面看法，主要關注基本面表現和長期投資價值。投資者普遍認為公司基本面穩健，適合長期持有。
    """,
    "sentiment_summary": {
        "positive_count": 5,
        "negative_count": 2,
        "neutral_count": 3,
        "total_posts": 10,
        "sentiment_ratio": 0.3
    },
    "hot_topics": [
        "基本面分析",
        "技術面觀察", 
        "長期投資"
    ]
}
```

## 錯誤處理

### 常見錯誤
1. **網路連線失敗**
   - 原因: 網路連線問題或網站無法存取
   - 處理: 使用模擬資料確保功能正常

2. **網站結構變更**
   - 原因: CMoney 網站 HTML 結構更新
   - 處理: 使用多種選擇器策略

3. **OpenAI API 失敗**
   - 原因: API 金鑰無效或網路問題
   - 處理: 使用預設情感分類

### 錯誤回應範例
```python
{
    "success": False,
    "section_title": "社群輿情分析",
    "section_content": "無法取得社群輿情資料",
    "sentiment_summary": {},
    "hot_topics": [],
    "error": "網路連線失敗"
}
```

## 效能考量

### 執行時間
- **一般情況**: 10-15 秒
- **主要耗時**: 網路爬取和 OpenAI API 呼叫
- **優化策略**: 限制貼文數量和並行處理

### API 限制
- **OpenAI API**: 有呼叫次數和速率限制
- **網站爬取**: 需要控制請求頻率
- **建議使用**: 合理控制分析頻率

## 擴展性

### 可能的擴展功能
1. **更多平台** - 加入其他社群平台
2. **即時監控** - 建立輿情監控系統
3. **情感趨勢** - 分析情感變化趨勢
4. **影響力分析** - 識別影響力較大的貼文

### 擴展範例
```python
# 加入更多社群平台
def crawl_multiple_platforms(stock_id: str) -> Dict:
    """爬取多個社群平台的討論"""
    platforms = {
        "cmoney": crawl_cmoney_forum,
        "ptt": crawl_ptt_stock,
        "facebook": crawl_facebook_groups
    }
    
    all_posts = []
    for platform_name, crawl_func in platforms.items():
        try:
            posts = crawl_func(stock_id)
            all_posts.extend(posts)
        except Exception as e:
            print(f"爬取 {platform_name} 失敗: {e}")
    
    return all_posts
```

## 測試

### 單元測試
```python
def test_social_sentiment():
    result = generate_social_sentiment_section("台積電", "2330")
    
    assert result["success"] == True
    assert "section_content" in result
    assert "sentiment_summary" in result
    assert "hot_topics" in result
```

### 整合測試
```python
# 測試完整流程
python test_watchlist.py
```

## 相關模組

### 依賴模組
- `requests` - HTTP 請求
- `beautifulsoup4` - HTML 解析
- `openai` - OpenAI API 客戶端
- `re` - 正則表達式

### 使用模組
- `generate_watchlist_summary_pipeline.py` - 投資組合摘要 (使用社群輿情分析)

## 設計原則

### 1. 資料品質
- 多種選擇器確保資料提取
- 自動過濾無效內容
- 模擬資料備用機制

### 2. 情感分析
- 使用 AI 進行智能分析
- 支援多種情感分類
- 詳細的分析邏輯

### 3. 效能優化
- 限制處理數量
- 並行處理策略
- 有效的錯誤處理

### 4. 可擴展性
- 模組化的設計
- 支援多平台擴展
- 彈性的分析策略 