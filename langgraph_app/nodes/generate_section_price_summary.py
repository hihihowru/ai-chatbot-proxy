import openai
import json
from typing import List, Dict
import os

def generate_price_summary_section(company_name: str, stock_id: str, news_summary: str, news_sources: List[Dict] = None) -> Dict:
    """
    產生股價異動總結 section
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        news_summary: 新聞摘要
        news_sources: 新聞來源列表
    
    Returns:
        股價異動總結 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 開始產生 section: 股價異動總結")
        print(f"[DEBUG] 公司名稱: {company_name}")
        print(f"[DEBUG] 股票代號: {stock_id}")
        print(f"[DEBUG] 新聞摘要長度: {len(news_summary)}")
        print(f"[DEBUG] 新聞來源數量: {len(news_sources) if news_sources else 0}")
        
        # 準備來源資訊
        source_info = ""
        if news_sources and isinstance(news_sources, list):
            source_info = "\n\n參考來源：\n"
            for i, source in enumerate(news_sources[:5], 1):  # 只取前5個來源
                if isinstance(source, dict):
                    title = source.get("title", "無標題")
                    link = source.get("link", "")
                    source_info += f"{i}. {title} [來源{i}]\n"
                else:
                    source_info += f"{i}. {str(source)} [來源{i}]\n"
        
        prompt = f"""
你是一位專業的股票分析師，請根據以下新聞摘要，為 {company_name}({stock_id}) 產生股價異動總結。

請分析以下三個面向：
1. 近期漲跌主因：分析股價變動的主要原因
2. 法人動向：分析外資、投信、自營商的買賣動向
3. 技術面觀察：分析技術指標、支撐壓力位等

新聞摘要：
{news_summary}

請回傳 JSON 格式如下，並在每個 content 後面加上來源標記 [來源X]：
{{
  "section": "股價異動總結",
  "cards": [
    {{ 
      "title": "近期漲跌主因", 
      "content": "根據新聞分析，{company_name}({stock_id})近期股價受到財報營收表現不佳的影響，盤後暴跌近19%。然而，股息殖利率超過5%，且上半年EPS創同期新高，市場對其未來營運動能持樂觀態度，因此有特定買盤介入支撐股價。 [來源1][來源2]"
    }},
    {{ 
      "title": "法人動向", 
      "content": "根據法人買賣動向，外資連續賣超{company_name}({stock_id})，顯示外資持續看空該股。然而，{company_name}股利連續配息12年，且上半年EPS表現優異，吸引投資人青睞，可能有投信及自營商介入買盤。 [來源3][來源4]"
    }},
    {{ 
      "title": "技術面觀察", 
      "content": "根據技術指標，{company_name}({stock_id})的股價目前處於下跌趨勢，但股息殖利率超過5%，可能提供一定支撐。投資人可留意月線保衛戰的表現，以及股價是否能突破壓力位。 [來源5]"
    }}
  ]
}}

**重要：**
1. 只回傳 JSON，不要有任何其他文字！
2. 在每個 content 後面加上對應的來源標記 [來源X]
3. 根據實際新聞內容調整分析，不要完全照抄範例
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
            print(f"[DEBUG] 合併 section: 股價異動總結")
            return {
                "success": True,
                "section": parsed_content,
                "raw_content": raw_content
            }
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON 解析失敗: {e}")
            # 回傳預設內容
            default_section = {
                "section": "股價異動總結",
                "cards": [
                    {"title": "近期漲跌主因", "content": "根據市場消息分析，股價變動主要受市場情緒和法人動向影響。 [來源1]"},
                    {"title": "法人動向", "content": "需進一步觀察外資、投信等法人買賣動向。 [來源2]"},
                    {"title": "技術面觀察", "content": "建議關注技術指標變化，設定適當的支撐壓力位。 [來源3]"}
                ]
            }
            return {
                "success": False,
                "section": default_section,
                "raw_content": raw_content,
                "error": f"JSON 解析失敗: {e}"
            }
            
    except Exception as e:
        print(f"[generate_price_summary_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "股價異動總結",
            "cards": [
                {"title": "近期漲跌主因", "content": "資料處理中，請稍後查看。"},
                {"title": "法人動向", "content": "資料處理中，請稍後查看。"},
                {"title": "技術面觀察", "content": "資料處理中，請稍後查看。"}
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
        {"title": "台股大漲400點", "link": "https://example.com/1"},
        {"title": "聯電法說會重點", "link": "https://example.com/2"},
        {"title": "外資買超291億", "link": "https://example.com/3"}
    ]
    
    result = generate_price_summary_section("聯電", "2303", test_news, test_sources)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 