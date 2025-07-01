import openai
import json
from typing import List, Dict
import os
import re

def generate_strategy_section(company_name: str, stock_id: str, news_summary: str, financial_data: Dict = None, news_sources: List[Dict] = None) -> Dict:
    """
    產生投資策略建議 section
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        news_summary: 新聞摘要
        financial_data: 財務資料
        news_sources: 新聞來源列表
    
    Returns:
        投資策略建議 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 開始產生 section: 投資策略建議")
        print(f"[DEBUG] 公司名稱: {company_name}")
        print(f"[DEBUG] 股票代號: {stock_id}")
        print(f"[DEBUG] 新聞摘要長度: {len(news_summary)}")
        print(f"[DEBUG] 新聞來源數量: {len(news_sources) if news_sources else 0}")
        
        # 準備財務摘要
        financial_summary = ""
        if financial_data and isinstance(financial_data, dict):
            if financial_data.get("eps") and isinstance(financial_data["eps"], dict):
                eps_values = list(financial_data["eps"].values())
                if eps_values and isinstance(eps_values[0], dict):
                    latest_eps = eps_values[0]
                    financial_summary += f"最新EPS: {latest_eps.get('eps', 'N/A')}元，{latest_eps.get('quarterly_growth', 'N/A')}季增率。"
            
            if financial_data.get("revenue") and isinstance(financial_data["revenue"], dict):
                revenue_values = list(financial_data["revenue"].values())
                if revenue_values and isinstance(revenue_values[0], dict):
                    latest_revenue = revenue_values[0]
                    financial_summary += f"最新營收: {latest_revenue.get('revenue', 'N/A')}仟元，{latest_revenue.get('quarterly_growth', 'N/A')}季增率。"
        
        # 準備新聞來源參考
        source_references = ""
        if news_sources and isinstance(news_sources, list):
            source_references = "參考來源：\n"
            for i, source in enumerate(news_sources[:5], 1):  # 只取前5個來源
                if isinstance(source, dict):
                    source_references += f"{i}. {source.get('title', '無標題')}: {source.get('link', '無連結')}\n"
                else:
                    source_references += f"{i}. {str(source)}\n"
        
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
        }},
        {{
          "text": "**技術面**：根據盤後分析，{company_name}({stock_id})有特定買盤介入，可能帶動盤勢波動。",
          "sources": [
            {{"title": "盤後分析報告", "link": "https://example.com/after-hours"}}
          ]
        }},
        {{
          "text": "**消息面**：外資連續賣超{company_name}({stock_id})，需留意外資動向對股價的影響。",
          "sources": [
            {{"title": "外資動向分析", "link": "https://example.com/foreign"}}
          ]
        }},
        {{
          "text": "**風險提醒**：日內交易風險較高，需注意市場波動和個股消息對股價的影響。"
        }}
      ]
    }},
    {{
      "title": "短線交易", 
      "content": [
        {{
          "text": "根據短期趨勢分析，建議短線交易時關注{company_name}({stock_id})的支撐壓力位，可考慮在適當位置進行交易。",
          "sources": [
            {{"title": "短期趨勢分析", "link": "https://example.com/short-term"}}
          ]
        }},
        {{
          "text": "**趨勢分析**：{company_name}({stock_id})上半年EPS創同期新高，顯示基本面強勁。",
          "sources": [
            {{"title": "財務報表分析", "link": "https://example.com/financial"}}
          ]
        }}
      ]
    }},
    {{
      "title": "中線投資",
      "content": [
        {{
          "text": "基於產業發展趨勢，建議中線投資者可分批布局{company_name}({stock_id})，關注產業政策變化。",
          "sources": [
            {{"title": "產業發展報告", "link": "https://example.com/industry"}},
            {{"title": "政策分析", "link": "https://example.com/policy"}}
          ]
        }}
      ]
    }},
    {{
      "title": "長線投資",
      "content": [
        {{
          "text": "從長期發展角度，{company_name}({stock_id})具備良好的成長潛力，適合長期持有。",
          "sources": [
            {{"title": "長期發展分析", "link": "https://example.com/long-term"}}
          ]
        }}
      ]
    }}
  ]
}}

請根據實際的新聞來源和財務資料，為每個句子分配適當的來源。如果沒有對應的來源，可以省略 sources 欄位。
"""
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        raw_content = response.choices[0].message.content.strip()
        print(f"[DEBUG] LLM 原始回傳內容：\n{raw_content}")
        # 自動將 *技術面：等替換為 markdown 粗體
        raw_content = re.sub(r'\*([\u4e00-\u9fa5]+面)：', r'**\1**：', raw_content)
        
        # 解析 LLM 回傳的 JSON
        try:
            result = json.loads(response.choices[0].message.content)
            
            # 後處理：將範例 sources 映射到實際的新聞來源
            if result.get("cards") and news_sources:
                source_mapping = {
                    "技術面分析": news_sources[0] if len(news_sources) > 0 else {"title": "技術面分析", "link": "無連結"},
                    "消息面分析": news_sources[1] if len(news_sources) > 1 else {"title": "消息面分析", "link": "無連結"},
                    "盤後分析報告": news_sources[2] if len(news_sources) > 2 else {"title": "盤後分析報告", "link": "無連結"},
                    "外資動向分析": news_sources[3] if len(news_sources) > 3 else {"title": "外資動向分析", "link": "無連結"},
                    "短期趨勢分析": news_sources[0] if len(news_sources) > 0 else {"title": "短期趨勢分析", "link": "無連結"},
                    "財務報表分析": news_sources[1] if len(news_sources) > 1 else {"title": "財務報表分析", "link": "無連結"},
                    "產業發展報告": news_sources[0] if len(news_sources) > 0 else {"title": "產業發展報告", "link": "無連結"},
                    "政策分析": news_sources[1] if len(news_sources) > 1 else {"title": "政策分析", "link": "無連結"},
                    "長期發展分析": news_sources[0] if len(news_sources) > 0 else {"title": "長期發展分析", "link": "無連結"}
                }
                
                # 替換每個 card 中的 sources
                for card in result["cards"]:
                    if card.get("content"):
                        for content_item in card["content"]:
                            if content_item.get("sources"):
                                for source in content_item["sources"]:
                                    if source.get("title") in source_mapping:
                                        source.update(source_mapping[source["title"]])
            
            # 修正：若 LLM 回傳沒有 summary_table，則補上一份 fallback summary_table
            if result.get("cards") and not result.get("summary_table"):
                result["summary_table"] = [
                    {"period": "1天", "suggestion": "根據技術面分析，快速交易", "confidence": "中等", "reason": "市場波動大"},
                    {"period": "1週", "suggestion": "關注支撐壓力", "confidence": "中等", "reason": "短期趨勢"},
                    {"period": "1個月", "suggestion": "分批布局", "confidence": "中等", "reason": "中期發展"},
                    {"period": "1季+", "suggestion": "長期持有", "confidence": "中等", "reason": "基本面穩健"}
                ]
            
            print(f"[DEBUG] ✅ 投資策略建議產生成功")
            return {
                "success": True,
                "section": result
            }
            
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON 解析失敗: {e}")
            print(f"[DEBUG] LLM 回傳內容: {response.choices[0].message.content}")
            # 回傳預設內容
            default_section = {
                "section": "不同投資型態的投資策略建議",
                "cards": [
                    {
                        "title": "日內交易",
                        "content": [
                            {
                                "text": "根據技術面和消息面分析，建議日內交易時留意{company_name}({stock_id})的盤勢波動，可考慮在適當時機進行快速交易。"
                            },
                            {
                                "text": "**技術面**：根據盤後分析，{company_name}({stock_id})有特定買盤介入，可能帶動盤勢波動。"
                            },
                            {
                                "text": "**消息面**：外資連續賣超{company_name}({stock_id})，需留意外資動向對股價的影響。"
                            },
                            {
                                "text": "**風險提醒**：日內交易風險較高，需注意市場波動和個股消息對股價的影響。"
                            }
                        ]
                    },
                    {
                        "title": "短線交易",
                        "content": [
                            {
                                "text": "根據短期趨勢分析，建議短線交易時關注{company_name}({stock_id})的支撐壓力位，可考慮在適當位置進行交易。"
                            },
                            {
                                "text": "**趨勢分析**：{company_name}({stock_id})上半年EPS創同期新高，顯示基本面強勁。"
                            }
                        ]
                    },
                    {
                        "title": "中線投資",
                        "content": [
                            {
                                "text": "基於產業發展趨勢，建議中線投資者可分批布局{company_name}({stock_id})，關注產業政策變化。"
                            }
                        ]
                    },
                    {
                        "title": "長線投資",
                        "content": [
                            {
                                "text": "從長期發展角度，{company_name}({stock_id})具備良好的成長潛力，適合長期持有。"
                            }
                        ]
                    }
                ]
            }
            return {
                "success": False,
                "section": default_section,
                "error": f"JSON 解析失敗: {e}"
            }
            
    except Exception as e:
        print(f"[generate_strategy_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "不同投資型態的投資策略建議",
            "cards": [
                {"title": "日內交易", "suggestion": "資料處理中，請稍後查看。", "bullets": ["處理中..."]},
                {"title": "短線交易", "suggestion": "資料處理中，請稍後查看。", "bullets": ["處理中..."]},
                {"title": "中線投資", "suggestion": "資料處理中，請稍後查看。", "bullets": ["處理中..."]},
                {"title": "長線投資", "suggestion": "資料處理中，請稍後查看。", "bullets": ["處理中..."]}
            ],
            "summary_table": [
                {"period": "1天", "suggestion": "處理中", "confidence": "處理中", "reason": "處理中"},
                {"period": "1週", "suggestion": "處理中", "confidence": "處理中", "reason": "處理中"},
                {"period": "1個月", "suggestion": "處理中", "confidence": "處理中", "reason": "處理中"},
                {"period": "1季+", "suggestion": "處理中", "confidence": "處理中", "reason": "處理中"}
            ]
        }
        return {
            "success": False,
            "section": default_section,
            "error": str(e)
        }

# 測試用
if __name__ == "__main__":
    test_news = """
    1. 台股今日反彈大漲逾400點，站回2萬2,000點大關，三大法人全站買方，買超台股339.05億元，外資則是由賣轉買，買超291.84億元，其中買進聯電（2303）高達3.5萬張居冠。
    2. 聯電(2303)法說會重點整理：EPS創19季低、估第二季毛利回升，毛利率下滑至26.7%，跌破3成，創下近年低點。
    """
    
    test_sources = [
        {"title": "台股反彈大漲", "link": "https://tw.finance.yahoo.com/news/example1"},
        {"title": "聯電法說會重點", "link": "https://www.cmoney.tw/notes/example2"}
    ]
    
    result = generate_strategy_section("聯電", "2303", test_news, None, test_sources)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 