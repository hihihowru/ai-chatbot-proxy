import openai
import json
from typing import List, Dict
import os
from .detect_stock import get_stock_name_by_id

PROMPT = '''你是一位只能回傳 JSON 的 API，請根據下列資訊，產生結構化個股分析報告，**只回傳 JSON 陣列，每個 section 格式如下**：

[
  {
    "section": "股價異動總結",
    "cards": [
      { "title": "近期漲跌主因", "content": "..." },
      { "title": "法人動向", "content": "..." },
      { "title": "技術面觀察", "content": "..." }
    ]
  },
  {
    "section": "財務狀況分析",
    "cards": [
      { "title": "EPS", "content": "...", "table": [ ... ] },
      { "title": "營收", "content": "...", "table": [ ... ] },
      { "title": "毛利率", "content": "...", "table": [ ... ] },
      { "title": "負債比率", "content": "...", "table": [ ... ] }
    ]
  },
  {
    "section": "分析師預估",
    "eps_median": "...",
    "eps_high": "...",
    "eps_low": "...",
    "eps_avg": "...",
    "target_price": "...",
    "analyst_count": ...,
    "note": "..."
  },
  {
    "section": "投資策略建議",
    "cards": [
      { "title": "日內交易", "suggestion": "...", "bullets": ["...", "..."] },
      { "title": "短線交易", "suggestion": "...", "bullets": ["...", "..."] },
      { "title": "中線投資", "suggestion": "...", "bullets": ["...", "..."] },
      { "title": "長線投資", "suggestion": "...", "bullets": ["...", "..."] }
    ],
    "summary_table": [
      {"period": "1天", "suggestion": "...", "confidence": "...", "reason": "..."},
      {"period": "1週", "suggestion": "...", "confidence": "...", "reason": "..."},
      {"period": "1個月", "suggestion": "...", "confidence": "...", "reason": "..."},
      {"period": "1季+", "suggestion": "...", "confidence": "...", "reason": "..."}
    ]
  },
  {
    "section": "操作注意事項",
    "bullets": ["...", "..."]
  },
  {
    "section": "資料來源",
    "sources": ["...", "..."]
  },
  {
    "section": "免責聲明",
    "disclaimer": "..."
  }
]

**重要：你必須嚴格回傳上述 JSON 陣列格式，每個 section 只允許出現一次，且內容必須完整！**
**不要有任何說明、不要有 markdown、不要有多餘的文字，只能回傳 JSON 陣列！**

【輸入資料】
- 公司名稱：{{ company_name }}
- 股票代號：{{ stock_id }}
- 使用者問題：{{ user_input }}
- 資料摘要整理：{{ summary_points }}
'''

def generate_report(company_name: str, stock_id: str, intent: str = "", time_info: str = "", news_summary: str = "", chart_info: dict = None, news_sources: list = None, financial_sources: list = None) -> dict:
    # 若 company_name 為空，則自動補上中文股名
    if not company_name and stock_id:
        company_name = get_stock_name_by_id(stock_id) or stock_id
    
    # 產生完整報告
    report_result = generate_report_pipeline(
        company_name=company_name,
        stock_id=stock_id,
        intent=intent,
        time_info=time_info,
        news_summary=news_summary,
        news_sources=news_sources,
        financial_data=chart_info,
        financial_sources=financial_sources
    )
    
    if report_result.get("success"):
        report = report_result["report"]
        return {
            "success": True,
            "stockName": report["stockName"],
            "stockId": report["stockId"],
            "sections": report["sections"],
            "summary": report["summary"],
            "paraphrased_prompt": report["paraphrased_prompt"],
            "logs": report.get("logs", [])  # 新增 logs 欄位
        }
    else:
        return {
            "success": False,
            "error": report_result.get("error", "未知錯誤"),
            "stockName": company_name,
            "stockId": stock_id,
            "sections": [],
            "summary": "報告產生失敗",
            "paraphrased_prompt": intent,
            "logs": report_result.get("report", {}).get("logs", [])  # 即使失敗也要回傳 logs
        }

# 測試用
if __name__ == "__main__":
    test_summary = [
        "1. 📰 消息面分析：華碩受惠於AI PC需求成長，股價表現強勁",
        "2. 📊 財務數據：EPS成長15%，營收創新高",
        "3. 🎯 券商觀點：分析師預估目標價上調至500元",
        "4. 🌐 產業趨勢：AI PC市場需求持續成長",
        "5. ⚠️ 風險提醒：需注意市場波動風險"
    ]
    test_sources = [
        {"title": "華碩AI PC需求強勁", "link": "https://example.com/news1"},
        {"title": "華碩財報亮眼", "link": "https://example.com/news2"}
    ]
    print("[TEST] 問題：華碩前幾天漲停後隔天又大跌，是為什麼呢？")
    result = generate_report("華碩", "2357", "華碩前幾天漲停後隔天又大跌，是為什麼呢？", test_summary, news_sources=test_sources)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 