import openai
import json
from typing import List, Dict
import os

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

請回傳 JSON 格式如下，並在每個 suggestion 和 bullets 後面加上來源標記 [來源X]：
{{
  "section": "投資策略建議",
  "cards": [
    {{
      "title": "日內交易",
      "suggestion": "根據技術面和消息面分析，建議日內交易時留意{company_name}({stock_id})的盤勢波動，可考慮在適當時機進行快速交易。 [來源1][來源2]",
      "bullets": [
        "技術面：根據盤後分析，{company_name}({stock_id})有特定買盤介入，可能帶動盤勢波動。 [來源1]",
        "消息面：外資連續賣超{company_name}({stock_id})，需留意外資動向對股價的影響。 [來源2]",
        "風險提醒：日內交易風險較高，需注意市場波動和個股消息對股價的影響。"
      ]
    }},
    {{
      "title": "短線交易", 
      "suggestion": "根據短期趨勢分析，建議短線交易時關注{company_name}({stock_id})的支撐壓力位，可考慮在適當位置進行交易。 [來源3]",
      "bullets": [
        "趨勢分析：{company_name}({stock_id})上半年EPS創同期新高，股息殖利率超過5%，營收衰退但EPS逆勢增長。 [來源3]",
        "支撐壓力：支撐位可參考歷年EPS與獲利趨勢，壓力位則需留意外資賣超等因素。 [來源4]",
        "操作建議：建議在支撐位附近低位進場，並設定適當停損點進行短線交易。"
      ]
    }},
    {{
      "title": "中線投資",
      "suggestion": "根據基本面分析，建議中線投資時考慮{company_name}({stock_id})的長期獲利能力和競爭優勢，可考慮進行中長期持有。 [來源5]",
      "bullets": [
        "基本面：{company_name}({stock_id})上半年EPS表現良好，股息連續配息12年，具有穩定的盈利能力。 [來源5]",
        "產業面：儘管營收有所下滑，但EPS逆勢增長，顯示公司具備應對市場挑戰的能力。 [來源6]",
        "投資建議：建議考慮中長期持有{company_name}({stock_id})，並留意公司未來營運動能和市場表現。"
      ]
    }},
    {{
      "title": "長線投資",
      "suggestion": "根據長期發展分析，建議長線投資時關注{company_name}({stock_id})的競爭優勢和未來發展潛力，可考慮長期持有。 [來源7]",
      "bullets": [
        "長期趨勢：{company_name}({stock_id})具有穩定的盈利能力和股息配發，未來獲利預期可望持續增長。 [來源7]",
        "競爭優勢：股息連續配息12年，營收雖衰退但EPS逆勢增長，顯示公司在競爭激烈市場中仍有優勢。 [來源8]",
        "投資價值：考慮{company_name}({stock_id})的長期投資價值，建議長期持有並留意公司未來發展潛力。"
      ]
    }}
  ],
  "summary_table": [
    {{
      "period": "1天",
      "suggestion": "觀望",
      "confidence": "中",
      "reason": "外資連續賣超{company_name}({stock_id})，需留意外資動向對股價的影響。 [來源2]"
    }},
    {{
      "period": "1週",
      "suggestion": "買進",
      "confidence": "中",
      "reason": "{company_name}({stock_id})上半年EPS表現良好，股息連續配息12年，具有穩定的盈利能力。 [來源5]"
    }},
    {{
      "period": "1個月",
      "suggestion": "買進",
      "confidence": "高",
      "reason": "{company_name}({stock_id})營收衰退，但EPS逆勢增長，全年盈餘可望大幅優於去年。 [來源6]"
    }},
    {{
      "period": "1季+",
      "suggestion": "買進",
      "confidence": "高",
      "reason": "{company_name}({stock_id})具有穩定的盈利能力和股息配發，未來獲利預期可望持續增長。 [來源7]"
    }}
  ]
}}

**重要：**
1. 只回傳 JSON，不要有任何其他文字！
2. 在每個 suggestion、bullets 和 reason 後面加上對應的來源標記 [來源X]
3. 根據實際新聞內容調整分析，不要完全照抄範例
4. 來源標記要對應實際的新聞來源
"""
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        raw_content = response.choices[0].message.content.strip()
        print(f"[DEBUG] LLM 原始回傳內容：\n{raw_content}")
        
        try:
            parsed_content = json.loads(raw_content)
            print(f"[DEBUG] 解析後內容：{json.dumps(parsed_content, ensure_ascii=False, indent=2)}")
            print(f"[DEBUG] 合併 section: 投資策略建議")
            return {
                "success": True,
                "section": parsed_content,
                "raw_content": raw_content
            }
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON 解析失敗: {e}")
            # 回傳預設內容
            default_section = {
                "section": "投資策略建議",
                "cards": [
                    {
                        "title": "日內交易",
                        "suggestion": "建議觀望，等待明確訊號",
                        "bullets": ["技術面：等待突破確認", "消息面：關注法人動向", "風險提醒：波動較大"]
                    },
                    {
                        "title": "短線交易",
                        "suggestion": "謹慎操作，設定停損",
                        "bullets": ["趨勢分析：短期調整", "支撐壓力：關注關鍵價位", "操作建議：分批進出"]
                    },
                    {
                        "title": "中線投資",
                        "suggestion": "逢低布局，關注基本面",
                        "bullets": ["基本面：觀察財報改善", "產業面：關注產業趨勢", "投資建議：價值投資"]
                    },
                    {
                        "title": "長線投資",
                        "suggestion": "長期持有，看好發展",
                        "bullets": ["長期趨勢：產業前景佳", "競爭優勢：技術領先", "投資價值：具投資價值"]
                    }
                ],
                "summary_table": [
                    {"period": "1天", "suggestion": "觀望", "confidence": "中", "reason": "等待明確訊號"},
                    {"period": "1週", "suggestion": "謹慎", "confidence": "中", "reason": "短期調整"},
                    {"period": "1個月", "suggestion": "逢低買進", "confidence": "高", "reason": "基本面改善"},
                    {"period": "1季+", "suggestion": "長期持有", "confidence": "很高", "reason": "長期成長趨勢"}
                ]
            }
            return {
                "success": False,
                "section": default_section,
                "raw_content": raw_content,
                "error": f"JSON 解析失敗: {e}"
            }
            
    except Exception as e:
        print(f"[generate_strategy_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "投資策略建議",
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