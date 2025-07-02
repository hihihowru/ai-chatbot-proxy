# generate_section_financial.py

## 功能說明

`generate_section_financial.py` 是財務狀況分析章節生成模組，專門用於產生股票投資分析報告中的財務狀況分析部分。此模組能夠：

1. **多源資料整合**：整合 FinLab API、Yahoo Finance 和新聞摘要的財務資料
2. **歷史資料分析**：提供近四年加上今年 Q1 的完整財務歷史
3. **多指標分析**：涵蓋 EPS、營收、營業利益等關鍵財務指標
4. **成長率計算**：自動計算年成長率並標示顏色
5. **智能洞察**：根據財務資料生成分析洞察
6. **表格格式化**：將財務資料格式化為易讀的表格格式

## 主要函數

### `generate_financial_section(company_name: str, stock_id: str, financial_data: Dict = None, news_summary: str = "") -> Dict`
- **功能**：產生財務狀況分析章節
- **參數**：
  - `company_name`: 公司名稱
  - `stock_id`: 股票代號
  - `financial_data`: 財務資料（從 FinLab API 或 Yahoo Finance 爬取）
  - `news_summary`: 新聞摘要（用於補充分析）
- **邏輯**：
  1. 處理多種格式的財務資料
  2. 生成 EPS、營收、營業利益表格
  3. 計算成長率和財務評分
  4. 生成分析洞察
- **返回**：財務狀況分析章節的 JSON 格式

### `calculate_financial_scores(eps_table, revenue_table, operating_income_table, financial_data) -> Dict`
- **功能**：計算財務評分
- **邏輯**：
  1. 分析 EPS 趨勢和穩定性
  2. 評估營收成長性
  3. 計算營業利益率
  4. 綜合評分
- **返回**：包含各項評分的字典

### `generate_eps_insight(eps_table, eps_info) -> str`
- **功能**：生成 EPS 分析洞察
- **邏輯**：
  1. 分析 EPS 趨勢
  2. 比較歷史表現
  3. 結合新聞資訊
- **返回**：EPS 分析文字

### `generate_revenue_insight(revenue_table, revenue_info) -> str`
- **功能**：生成營收分析洞察
- **邏輯**：
  1. 分析營收成長趨勢
  2. 評估季節性表現
  3. 結合新聞資訊
- **返回**：營收分析文字

### `generate_operating_income_insight(operating_income_table, margin_info) -> str`
- **功能**：生成營業利益分析洞察
- **邏輯**：
  1. 分析營業利益率趨勢
  2. 評估獲利能力
  3. 結合新聞資訊
- **返回**：營業利益分析文字

## 支援的資料格式

### 1. DataFrame 格式
```python
# 假設 index 是季度（如 '2025Q1'），columns 有 '每股盈餘'、'營收'、'營業利益' 等
financial_data = pd.DataFrame({
    '每股盈餘': [1.2, 1.8, 1.6, 1.4],
    '營收': [100000, 160000, 140000, 120000],
    '營業利益': [15000, 24000, 21000, 18000]
}, index=['2025Q1', '2024Q4', '2024Q3', '2024Q2'])
```

### 2. JSON 格式
```python
financial_data = {
    'Data': [
        ['2025Q1', 1.2, 100000, 15000],
        ['2024Q4', 1.8, 160000, 24000],
        ['2024Q3', 1.6, 140000, 21000]
    ],
    'Title': ['季度', '每股盈餘', '營收', '營業利益']
}
```

### 3. 新格式（包含 income_statement）
```python
financial_data = {
    'income_statement': {
        '2025Q1': {'每股盈餘': 1.2, '營收': 100000, '營業利益': 15000},
        '2024Q4': {'每股盈餘': 1.8, '營收': 160000, '營業利益': 24000}
    }
}
```

## 財務指標分析

### 1. EPS（每股盈餘）分析
- **趨勢分析**：觀察 EPS 的長期趨勢
- **穩定性評估**：分析 EPS 的波動性
- **成長性評估**：計算年成長率
- **同業比較**：與產業平均比較

### 2. 營收分析
- **成長趨勢**：分析營收的成長軌跡
- **季節性分析**：觀察季度營收變化
- **規模評估**：以億元為單位顯示
- **成長率計算**：年對年成長率

### 3. 營業利益分析
- **獲利能力**：評估營業利益率
- **成本控制**：分析成本結構變化
- **效率提升**：觀察營運效率改善
- **趨勢預測**：基於歷史趨勢預測

## 成長率計算邏輯

### 計算公式
```python
growth = (curr_val - prev_val) / abs(prev_val) * 100 if prev_val != 0 else 0
```

### 顏色標示
- **紅色**：成長率 > 0（正成長）
- **綠色**：成長率 < 0（負成長）
- **灰色**：成長率 = 0 或無資料

### 計算範圍
- 支援 Q1-Q4 各季度的成長率
- 年對年比較
- 處理缺失資料（顯示為 "N/A"）

## Input/Output 範例

### 輸入範例
```python
# 基本參數
company_name = "台積電"
stock_id = "2330"

# 財務資料
financial_data = {
    'income_statement': {
        '2025Q1': {'每股盈餘': 8.5, '營收': 592700, '營業利益': 243800},
        '2024Q4': {'每股盈餘': 9.2, '營收': 625500, '營業利益': 262300},
        '2024Q3': {'每股盈餘': 8.7, '營收': 546700, '營業利益': 224500},
        '2024Q2': {'每股盈餘': 7.8, '營收': 480800, '營業利益': 195600}
    }
}

# 新聞摘要
news_summary = "台積電2024年第四季EPS達9.2元，創歷史新高，營收成長15%。"
```

### 輸出範例
```python
{
    "section": "財務狀況分析",
    "cards": [
        {
            "title": "EPS",
            "content": "台積電EPS表現強勁，2024年第四季達9.2元創歷史新高，較去年同期成長18.5%。近四年EPS呈現穩定成長趨勢，顯示公司獲利能力持續提升。",
            "table": [
                {
                    "年度": "2025",
                    "Q1": "8.5",
                    "Q2": "N/A",
                    "Q3": "N/A",
                    "Q4": "N/A"
                },
                {
                    "年度": "2024",
                    "Q1": "8.2",
                    "Q2": "7.8",
                    "Q3": "8.7",
                    "Q4": "9.2",
                    "Q1_成長率": {"value": "3.7%", "color": "red"},
                    "Q2_成長率": {"value": "-4.9%", "color": "green"},
                    "Q3_成長率": {"value": "11.5%", "color": "red"},
                    "Q4_成長率": {"value": "5.7%", "color": "red"}
                }
            ]
        },
        {
            "title": "營收",
            "content": "台積電營收表現亮眼，2024年第四季達6,255億元，年成長15%。近四年營收呈現穩定成長，顯示公司在半導體產業的領導地位穩固。",
            "table": [
                {
                    "年度": "2025",
                    "Q1": "592.7億",
                    "Q2": "N/A",
                    "Q3": "N/A",
                    "Q4": "N/A"
                },
                {
                    "年度": "2024",
                    "Q1": "592.7億",
                    "Q2": "480.8億",
                    "Q3": "546.7億",
                    "Q4": "625.5億",
                    "Q1_成長率": {"value": "0.0%", "color": "gray"},
                    "Q2_成長率": {"value": "-18.9%", "color": "green"},
                    "Q3_成長率": {"value": "13.7%", "color": "red"},
                    "Q4_成長率": {"value": "14.4%", "color": "red"}
                }
            ]
        },
        {
            "title": "營業利益",
            "content": "台積電營業利益表現優異，2024年第四季達2,623億元，營業利益率41.9%。近四年營業利益率維持在40%以上，顯示公司具有優異的獲利能力。",
            "table": [
                {
                    "年度": "2025",
                    "Q1": "243.8億",
                    "Q2": "N/A",
                    "Q3": "N/A",
                    "Q4": "N/A"
                },
                {
                    "年度": "2024",
                    "Q1": "243.8億",
                    "Q2": "195.6億",
                    "Q3": "224.5億",
                    "Q4": "262.3億",
                    "Q1_成長率": {"value": "0.0%", "color": "gray"},
                    "Q2_成長率": {"value": "-19.8%", "color": "green"},
                    "Q3_成長率": {"value": "14.8%", "color": "red"},
                    "Q4_成長率": {"value": "16.9%", "color": "red"}
                }
            ]
        }
    ],
    "financial_score": {
        "eps_score": 85,
        "revenue_score": 88,
        "operating_income_score": 92,
        "overall_score": 88
    }
}
```

### 完整測試範例
```python
# 測試財務分析
result = generate_financial_section(
    company_name="台積電",
    stock_id="2330",
    financial_data=financial_data,
    news_summary=news_summary
)

print(f"財務分析完成")
print(f"EPS 評分: {result['financial_score']['eps_score']}")
print(f"營收評分: {result['financial_score']['revenue_score']}")
print(f"營業利益評分: {result['financial_score']['operating_income_score']}")
print(f"綜合評分: {result['financial_score']['overall_score']}")
```

## 資料處理邏輯

### 1. 多格式資料處理
```python
# DataFrame 處理
if isinstance(financial_data, pd.DataFrame):
    for idx, row in financial_data.iterrows():
        quarter = str(idx)
        quarterly[quarter] = row.to_dict()

# JSON 處理
elif isinstance(financial_data, dict):
    if 'Data' in financial_data and 'Title' in financial_data:
        # 處理傳統 JSON 格式
        data = financial_data.get('Data', [])
        title = financial_data.get('Title', [])
        # 轉換為 quarterly 格式
    elif 'income_statement' in financial_data:
        # 處理新格式
        quarterly = financial_data['income_statement']
```

### 2. 季度資料標準化
```python
# 統一 quarterly key 格式（去除 dash）
quarterly = {q.replace('-', ''): v for q, v in quarterly.items()}

# 只取近 17 季（4年 + 今年 Q1）
all_quarters = sorted(quarterly.keys(), reverse=True)[:17]
```

### 3. 年度分組處理
```python
# 依年度分組
year_quarters = {}
for q in all_quarters:
    year = q[:4]
    if year not in year_quarters:
        year_quarters[year] = []
    year_quarters[year].append(q)

# 只保留近四年加上今年
years = sorted(year_quarters.keys(), reverse=True)[:5]
```

## 財務評分系統

### 1. EPS 評分 (0-100)
- **趨勢穩定性** (30分)：EPS 波動性評估
- **成長性** (40分)：年成長率評估
- **絕對值** (30分)：EPS 絕對水準評估

### 2. 營收評分 (0-100)
- **成長趨勢** (40分)：營收成長軌跡
- **規模** (30分)：營收絕對規模
- **穩定性** (30分)：營收波動性

### 3. 營業利益評分 (0-100)
- **獲利能力** (40分)：營業利益率水準
- **成長性** (30分)：營業利益成長
- **效率** (30分)：營運效率改善

### 4. 綜合評分
- 加權平均：EPS(40%) + 營收(30%) + 營業利益(30%)
- 範圍：0-100 分
- 評級：90+ 優秀，80-89 良好，70-79 一般，<70 需改善

## 新聞資訊提取

### 1. EPS 資訊提取
```python
def extract_eps_from_news(news_summary: str) -> Optional[str]:
    """從新聞摘要中提取 EPS 相關資訊"""
    # 使用正則表達式匹配 EPS 相關資訊
    eps_patterns = [
        r'EPS[：:]\s*([\d.]+)',
        r'每股盈餘[：:]\s*([\d.]+)',
        r'每股獲利[：:]\s*([\d.]+)'
    ]
    # 返回匹配到的資訊
```

### 2. 營收資訊提取
```python
def extract_revenue_from_news(news_summary: str) -> Optional[str]:
    """從新聞摘要中提取營收相關資訊"""
    # 使用正則表達式匹配營收相關資訊
    revenue_patterns = [
        r'營收[：:]\s*([\d.]+)',
        r'營業額[：:]\s*([\d.]+)',
        r'營收成長[：:]\s*([\d.]+)%'
    ]
    # 返回匹配到的資訊
```

### 3. 毛利率資訊提取
```python
def extract_margin_from_news(news_summary: str) -> Optional[str]:
    """從新聞摘要中提取毛利率相關資訊"""
    # 使用正則表達式匹配毛利率相關資訊
    margin_patterns = [
        r'毛利率[：:]\s*([\d.]+)%',
        r'營業利益率[：:]\s*([\d.]+)%',
        r'獲利率[：:]\s*([\d.]+)%'
    ]
    # 返回匹配到的資訊
```

## 錯誤處理

### 1. 資料格式錯誤
```python
try:
    # 處理財務資料
    if isinstance(financial_data, pd.DataFrame):
        # DataFrame 處理邏輯
    elif isinstance(financial_data, dict):
        # Dict 處理邏輯
    else:
        # 使用預設資料
        quarterly = default_quarterly_data
except Exception as e:
    print(f"[ERROR] 財務資料處理失敗: {e}")
    quarterly = default_quarterly_data
```

### 2. 成長率計算錯誤
```python
try:
    if isinstance(prev_val, (int, float)) and isinstance(curr_val, (int, float)):
        growth = (curr_val - prev_val) / abs(prev_val) * 100 if prev_val != 0 else 0
        color = "red" if growth > 0 else "green" if growth < 0 else "gray"
        table[i][f"{q}_成長率"] = {"value": f"{growth:.1f}%", "color": color}
    else:
        table[i][f"{q}_成長率"] = {"value": "N/A", "color": "gray"}
except Exception as e:
    print(f"[DEBUG] 成長率計算失敗 {q}: {e}")
    table[i][f"{q}_成長率"] = {"value": "N/A", "color": "gray"}
```

### 3. 預設資料機制
- 當無法取得實際財務資料時，使用預設資料
- 預設資料涵蓋近4年的完整季度資料
- 確保分析報告的完整性

## 效能優化

### 1. 資料快取
- 快取常用的財務資料
- 避免重複的 API 調用
- 實作資料過期機制

### 2. 批次處理
- 批次處理多個季度的資料
- 優化記憶體使用
- 提高處理效率

### 3. 並發處理
- 支援多個財務指標同時計算
- 實作非同步處理
- 提高響應速度

## 擴充性

### 1. 新增財務指標
- 支援更多財務指標（如 ROE、ROA）
- 可自訂指標計算邏輯
- 保持向後相容性

### 2. 自訂評分系統
- 可調整評分權重
- 支援自訂評分標準
- 適應不同產業需求

### 3. 多語言支援
- 支援多語言財務術語
- 可擴充多語言分析
- 保持一致的API介面

## 使用場景

### 1. 投資分析報告
- 生成完整的財務分析章節
- 提供結構化的財務資料
- 支援投資決策

### 2. 研究報告
- 提供詳細的財務歷史分析
- 支援趨勢預測
- 協助研究分析

### 3. 財報解讀
- 自動解讀財報數據
- 提供關鍵指標分析
- 支援財報比較

### 4. 風險評估
- 評估財務風險
- 分析獲利能力
- 支援風險管理 