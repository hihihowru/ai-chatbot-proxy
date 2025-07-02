# detect_time.py

## 功能說明

`detect_time.py` 是時間偵測模組，專門用於從自然語言問題中識別時間表達，並轉換為具體的日期範圍。此模組能夠：

1. **時間表達識別**：識別中文時間關鍵字和表達方式
2. **日期範圍計算**：將時間表達轉換為具體的開始和結束日期
3. **多種時間單位**：支援天、週、月、季、年等不同時間單位
4. **相對時間處理**：處理「最近N天」等相對時間表達
5. **預設值處理**：當未偵測到時間表達時提供預設值

## 主要函數

### `detect_time(question: str) -> str`
- **功能**：從問題中偵測時間表達
- **邏輯**：
  1. 移除問題前後空白
  2. 使用正則表達式匹配時間關鍵字
  3. 提取數字參數（如「最近5天」中的5）
  4. 返回標準化的時間表達
- **返回**：標準化的時間表達字串

### `get_date_range(time_expression: str) -> tuple`
- **功能**：根據時間表達取得日期範圍
- **邏輯**：
  1. 解析時間表達類型
  2. 計算對應的開始和結束日期
  3. 格式化為 YYYYMMDD 格式
- **返回**：(開始日期, 結束日期) 元組

## 支援的時間模式

### 1. 基本時間單位

#### 天級別
```python
time_patterns = {
    r'今天|今日|本日': 'today',
    r'昨天|昨日': 'yesterday', 
    r'明天|明日': 'tomorrow',
}
```

#### 週級別
```python
time_patterns = {
    r'上週|上周': 'last_week',
    r'本週|本周|這週|这周': 'this_week',
    r'下週|下周': 'next_week',
}
```

#### 月級別
```python
time_patterns = {
    r'上個月|上月': 'last_month',
    r'這個月|这個月|本月': 'this_month',
    r'下個月|下月': 'next_month',
}
```

#### 季級別
```python
time_patterns = {
    r'上季|上一季': 'last_quarter',
    r'本季|這一季|这一季': 'this_quarter',
    r'下季|下一季': 'next_quarter',
}
```

#### 年級別
```python
time_patterns = {
    r'去年': 'last_year',
    r'今年': 'this_year',
    r'明年': 'next_year',
}
```

### 2. 相對時間表達

#### 最近N天/週/月/年
```python
time_patterns = {
    r'最近(\d+)天': 'recent_days',
    r'最近(\d+)週': 'recent_weeks',
    r'最近(\d+)個月': 'recent_months',
    r'最近(\d+)年': 'recent_years',
}
```

## 日期計算邏輯

### 1. 基本時間計算

#### 今天 (today)
```python
start_date = today
end_date = today
```

#### 昨天 (yesterday)
```python
start_date = today - timedelta(days=1)
end_date = start_date
```

#### 明天 (tomorrow)
```python
start_date = today + timedelta(days=1)
end_date = start_date
```

### 2. 週期計算

#### 本週 (this_week)
```python
# 本週開始（週一）
start_date = today - timedelta(days=today.weekday())
end_date = today
```

#### 上週 (last_week)
```python
start_date = today - timedelta(weeks=1)
end_date = today
```

#### 下週 (next_week)
```python
start_date = today
end_date = today + timedelta(weeks=1)
```

### 3. 月份計算

#### 本月 (this_month)
```python
start_date = today.replace(day=1)
end_date = today
```

#### 上個月 (last_month)
```python
if today.month == 1:
    start_date = today.replace(year=today.year-1, month=12)
else:
    start_date = today.replace(month=today.month-1)
end_date = today
```

#### 下個月 (next_month)
```python
start_date = today
if today.month == 12:
    end_date = today.replace(year=today.year+1, month=1)
else:
    end_date = today.replace(month=today.month+1)
```

### 4. 季度計算

#### 本季 (this_quarter)
```python
quarter = (today.month - 1) // 3
start_date = today.replace(month=quarter*3+1, day=1)
end_date = today
```

#### 上一季 (last_quarter)
```python
quarter = (today.month - 1) // 3
if quarter == 0:
    start_date = today.replace(year=today.year-1, month=10)
else:
    start_date = today.replace(month=(quarter-1)*3+1)
end_date = today
```

### 5. 年度計算

#### 今年 (this_year)
```python
start_date = today.replace(month=1, day=1)
end_date = today
```

#### 去年 (last_year)
```python
start_date = today.replace(year=today.year-1)
end_date = today
```

### 6. 相對時間計算

#### 最近N天 (recent_days_N)
```python
days = int(time_expression.split('_')[-1])
start_date = today - timedelta(days=days)
end_date = today
```

#### 最近N週 (recent_weeks_N)
```python
weeks = int(time_expression.split('_')[-1])
start_date = today - timedelta(weeks=weeks)
end_date = today
```

#### 最近N個月 (recent_months_N)
```python
months = int(time_expression.split('_')[-1])
# 簡化處理，每個月算30天
start_date = today - timedelta(days=months*30)
end_date = today
```

#### 最近N年 (recent_years_N)
```python
years = int(time_expression.split('_')[-1])
start_date = today.replace(year=today.year-years)
end_date = today
```

## Input/Output 範例

### 輸入範例
```python
test_questions = [
    "今天台積電的股價如何？",
    "昨天的新聞有哪些？",
    "本週的法人買賣超",
    "上個月的營收報告",
    "最近5天的技術分析",
    "今年第一季的財報"
]
```

### 輸出範例

#### 時間表達偵測
```python
detect_time("今天台積電的股價如何？")  # 返回: "today"
detect_time("昨天的新聞有哪些？")      # 返回: "yesterday"
detect_time("本週的法人買賣超")        # 返回: "this_week"
detect_time("上個月的營收報告")        # 返回: "last_month"
detect_time("最近5天的技術分析")       # 返回: "recent_days_5"
detect_time("今年第一季的財報")        # 返回: "this_year"
```

#### 日期範圍計算
```python
# 假設今天是 2024-01-15
get_date_range("today")           # 返回: ("20240115", "20240115")
get_date_range("yesterday")       # 返回: ("20240114", "20240114")
get_date_range("this_week")       # 返回: ("20240108", "20240115")
get_date_range("last_month")      # 返回: ("20231215", "20240115")
get_date_range("recent_days_5")   # 返回: ("20240110", "20240115")
get_date_range("this_year")       # 返回: ("20240101", "20240115")
```

### 完整測試範例
```python
# 測試時間偵測
question = "最近3天的台積電技術分析"
time_expr = detect_time(question)
print(f"問題: {question}")
print(f"時間表達: {time_expr}")

# 測試日期範圍
start_date, end_date = get_date_range(time_expr)
print(f"日期範圍: {start_date} 到 {end_date}")
```

## 預設值處理

### 1. 未偵測到時間表達
當問題中沒有明確的時間表達時，模組會返回預設值：
```python
return "today"  # 預設為今天
```

### 2. 未知時間表達
當遇到未知的時間表達時，會使用預設的最近5天：
```python
else:
    # 預設最近5天
    start_date = today - timedelta(days=5)
    end_date = today
```

## 錯誤處理

### 1. 正則表達式匹配失敗
- 返回預設時間表達 "today"
- 不影響系統其他功能
- 記錄警告訊息

### 2. 日期計算錯誤
- 處理月份邊界情況（如1月減1個月）
- 處理年份邊界情況（如12月加1個月）
- 處理季度計算的邊界情況

### 3. 數字解析錯誤
- 處理相對時間中的數字提取
- 提供合理的預設值
- 避免系統崩潰

## 效能優化

### 1. 正則表達式預編譯
- 使用 `re.search()` 進行高效匹配
- 避免重複編譯正則表達式
- 優化匹配順序

### 2. 日期計算優化
- 使用 `datetime` 和 `timedelta` 進行高效計算
- 避免重複的日期物件創建
- 最小化計算複雜度

### 3. 記憶體管理
- 及時釋放臨時變數
- 避免不必要的字串操作
- 使用元組返回多個值

## 擴充性

### 1. 新增時間模式
- 在 `time_patterns` 字典中新增模式
- 支援更複雜的時間表達
- 保持向後相容性

### 2. 自訂日期格式
- 可修改日期輸出格式
- 支援不同的日期表示方法
- 適應不同系統需求

### 3. 多語言支援
- 可擴充其他語言的時間關鍵字
- 支援國際化的時間表達
- 保持一致的API介面

## 使用場景

### 1. 新聞查詢
- 根據時間範圍查詢相關新聞
- 支援相對時間表達
- 提供靈活的時間選擇

### 2. 技術分析
- 指定分析的時間範圍
- 支援不同時間週期的分析
- 適應不同的分析需求

### 3. 財報查詢
- 查詢特定期間的財報資料
- 支援季度和年度查詢
- 提供標準化的時間範圍

### 4. 法人買賣超
- 查詢特定時間的法人動向
- 支援週期性分析
- 提供時間範圍的靈活性 