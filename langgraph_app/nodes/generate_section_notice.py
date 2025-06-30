import openai
import json
from typing import List, Dict
import os

def generate_notice_section(company_name: str, stock_id: str, news_summary: str, financial_data: Dict = None, news_sources: List[Dict] = None) -> Dict:
    """
    產生操作注意事項 section
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        news_summary: 新聞摘要
        financial_data: 財務資料
        news_sources: 新聞來源列表
    
    Returns:
        操作注意事項 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 開始產生 section: 操作注意事項")
        print(f"[DEBUG] 公司名稱: {company_name}")
        print(f"[DEBUG] 股票代號: {stock_id}")
        print(f"[DEBUG] 新聞摘要長度: {len(news_summary)}")
        
        # 準備財務摘要
        financial_summary = ""
        if financial_data:
            if financial_data.get("eps"):
                latest_eps = list(financial_data["eps"].values())[0]
                financial_summary += f"最新EPS: {latest_eps.get('eps', 'N/A')}元，{latest_eps.get('quarterly_growth', 'N/A')}季增率。"
            
            if financial_data.get("revenue"):
                latest_revenue = list(financial_data["revenue"].values())[0]
                financial_summary += f"最新營收: {latest_revenue.get('revenue', 'N/A')}仟元，{latest_revenue.get('quarterly_growth', 'N/A')}季增率。"
        
        prompt = f"""
你是一位專業的投資顧問，請根據以下資訊，為 {company_name}({stock_id}) 產生操作注意事項。

請提供具體、可執行的操作建議，包含以下面向：
1. 技術指標監控：關注哪些技術指標的變化
2. 法人動向：如何追蹤法人買賣動向
3. 產業消息：需要關注哪些產業相關新聞
4. 財報發布：關注哪些財報時程
5. 風險控管：如何設定停損停利
6. 持續調整：如何根據市場變化調整策略

新聞摘要：
{news_summary}

財務摘要：
{financial_summary}

請回傳 JSON 格式如下：
{{
  "section": "操作注意事項",
  "bullets": [
    "技術指標監控：關注RSI、MACD變化，設定關鍵支撐壓力位",
    "法人動向：追蹤外資和投信買賣超，關注大戶持股變化",
    "產業消息：留意相關產業新聞，關注競爭對手動態",
    "財報發布：關注下季業績表現，注意法說會時程",
    "風險控管：設定明確停損點，控制單筆投資比例",
    "持續調整：根據市場變化適時修正策略，保持彈性"
  ]
}}

**重要：只回傳 JSON，不要有任何其他文字！**
**注意事項要具體、可執行，並包含實際操作建議！**
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
            print(f"[DEBUG] 合併 section: 操作注意事項")
            return {
                "success": True,
                "section": parsed_content,
                "raw_content": raw_content
            }
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON 解析失敗: {e}")
            # 回傳預設內容
            default_section = {
                "section": "操作注意事項",
                "bullets": [
                    "技術指標監控：關注RSI、MACD變化，設定關鍵支撐壓力位",
                    "法人動向：追蹤外資和投信買賣超，關注大戶持股變化",
                    "產業消息：留意相關產業新聞，關注競爭對手動態",
                    "財報發布：關注下季業績表現，注意法說會時程",
                    "風險控管：設定明確停損點，控制單筆投資比例",
                    "持續調整：根據市場變化適時修正策略，保持彈性"
                ]
            }
            return {
                "success": False,
                "section": default_section,
                "raw_content": raw_content,
                "error": f"JSON 解析失敗: {e}"
            }
            
    except Exception as e:
        print(f"[generate_notice_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "操作注意事項",
            "bullets": [
                "技術指標監控：關注RSI、MACD變化",
                "法人動向：追蹤外資和投信買賣超",
                "產業消息：留意相關產業新聞",
                "財報發布：關注下季業績表現",
                "風險控管：設定明確停損點",
                "持續調整：根據市場變化適時修正"
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
    
    result = generate_notice_section("聯電", "2303", test_news)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 