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
    try:
        user_input = f"{company_name} {stock_id} {intent}"
        summary_points = news_summary.split('\n') if news_summary else []
        summary_text = "\n".join(summary_points)
        # DEBUG PRINTS
        print("[DEBUG] summary_points:", summary_points)
        print("[DEBUG] news_summary:", news_summary)
        if chart_info is not None:
            print("[DEBUG] chart_info:", chart_info)
        if news_sources is not None:
            print("[DEBUG] news_sources:", news_sources)
        if financial_sources is not None:
            print("[DEBUG] financial_sources:", financial_sources)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = PROMPT.replace("{{ company_name }}", company_name)
        prompt = prompt.replace("{{ stock_id }}", stock_id)
        prompt = prompt.replace("{{ user_input }}", user_input)
        prompt = prompt.replace("{{ summary_points }}", summary_text)
        print("[DEBUG] 最終 prompt：\n" + prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        report = response.choices[0].message.content.strip()
        print("[DEBUG] LLM 原始回傳內容：\n" + report)
        sections = None
        try:
            sections = json.loads(report)
            print("[DEBUG] LLM 回傳 JSON 成功，sections 數量：", len(sections))
            sections_dict = {}
            for sec in sections:
                if "section" in sec:
                    sections_dict[sec["section"]] = sec
                    print(f"[DEBUG] Section: {sec['section']}")
                    if "cards" in sec:
                        for idx, card in enumerate(sec["cards"], 1):
                            print(f"  Card {idx}: {card}")
                    if "table" in sec:
                        print(f"  Table: {sec['table']}")
                    if "bullets" in sec:
                        print(f"  Bullets: {sec['bullets']}")
                    if "summary_table" in sec:
                        print(f"  Summary Table: {sec['summary_table']}")
            sections = sections_dict
        except Exception as e:
            print("[DEBUG] LLM 回傳內容無法解析為 JSON，原始內容如上")
            sections = {}
        return {
            "success": True,
            "report": report,
            "sections": sections,
            "company_name": company_name,
            "stock_id": stock_id,
            "intent": intent,
            "time_info": time_info,
            "message": "成功生成投資分析報告"
        }
    except Exception as e:
        print(f"[generate_report ERROR] {e}")
        return {
            "success": False,
            "error": str(e),
            "report": "",
            "sections": {},
            "company_name": company_name,
            "stock_id": stock_id,
            "intent": intent
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