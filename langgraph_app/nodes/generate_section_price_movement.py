import openai
import json
from typing import List, Dict
import os

def generate_price_movement_section(company_name: str, stock_id: str, news_summary: str, news_sources: List[Dict] = None) -> Dict:
    """
    產生個股分析的股價異動總結 section
    
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
        
        prompt = f"""
你是一位專業的證券分析師，請根據以下資訊，為 {company_name}({stock_id}) 產生股價異動總結。

請分析以下三個面向：
1. 近期漲跌主因：分析最近股價變動的主要原因
2. 法人動向：分析外資、投信、自營商的買賣超情況
3. 技術面觀察：分析技術指標和支撐壓力位

新聞摘要：
{news_summary}

請回傳 JSON 格式如下：
{{
  "section": "股價異動總結",
  "cards": [
    {{
      "title": "近期漲跌主因",
      "content": "根據新聞分析，{company_name}({stock_id})近期股價變動主要受到以下因素影響：[來源1] [來源2]"
    }},
    {{
      "title": "法人動向",
      "content": "法人買賣超分析：[來源3] [來源4]"
    }},
    {{
      "title": "技術面觀察",
      "content": "技術指標分析：[來源5] [來源6]"
    }}
  ]
}}

**重要：只回傳 JSON，不要有任何其他文字！**
**內容要具體、有根據，並包含實際的新聞來源！**
"""
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        raw_content = response.choices[0].message.content.strip()
        print(f"[DEBUG] LLM 原始回傳內容：\n{raw_content}")
        
        # 解析 JSON
        try:
            result = json.loads(raw_content)
            
            # 如果有新聞來源，替換來源標記
            if news_sources and isinstance(news_sources, list):
                source_mapping = {
                    "來源1": news_sources[0] if len(news_sources) > 0 else {"title": "來源1", "link": "無連結"},
                    "來源2": news_sources[1] if len(news_sources) > 1 else {"title": "來源2", "link": "無連結"},
                    "來源3": news_sources[2] if len(news_sources) > 2 else {"title": "來源3", "link": "無連結"},
                    "來源4": news_sources[3] if len(news_sources) > 3 else {"title": "來源4", "link": "無連結"},
                    "來源5": news_sources[4] if len(news_sources) > 4 else {"title": "來源5", "link": "無連結"},
                    "來源6": news_sources[5] if len(news_sources) > 5 else {"title": "來源6", "link": "無連結"}
                }
                
                # 替換每個 card 中的來源標記
                for card in result.get("cards", []):
                    content = card.get("content", "")
                    for source_key, source_info in source_mapping.items():
                        if source_key in content:
                            content = content.replace(f"[{source_key}]", f"[{source_info.get('title', source_key)}]")
                    card["content"] = content
            
            # 按照出現順序組成 sources 陣列
            sources = [news_sources[i] for i in sorted(used_indices)] if news_sources else []
            result["sources"] = sources
            
            print(f"[DEBUG] ✅ 股價異動總結產生成功")
            return {
                "success": True,
                "section": result
            }
            
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON 解析失敗: {e}")
            print(f"[DEBUG] LLM 回傳內容: {response.choices[0].message.content}")
            # 回傳預設內容
            default_section = {
                "section": "股價異動總結",
                "cards": [
                    {
                        "title": "近期漲跌主因",
                        "content": f"根據新聞分析，{company_name}({stock_id})近期股價變動主要受到市場因素影響。"
                    },
                    {
                        "title": "法人動向",
                        "content": f"法人買賣超分析：需關注外資和投信動向。"
                    },
                    {
                        "title": "技術面觀察",
                        "content": f"技術指標分析：建議關注支撐壓力位。"
                    }
                ],
                "sources": []  # 確保預設也是陣列
            }
            return {
                "success": False,
                "section": default_section,
                "error": f"JSON 解析失敗: {e}"
            }
            
    except Exception as e:
        print(f"[generate_price_movement_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "股價異動總結",
            "cards": [
                {
                    "title": "近期漲跌主因",
                    "content": f"根據新聞分析，{company_name}({stock_id})近期股價變動主要受到市場因素影響。"
                },
                {
                    "title": "法人動向",
                    "content": f"法人買賣超分析：需關注外資和投信動向。"
                },
                {
                    "title": "技術面觀察",
                    "content": f"技術指標分析：建議關注支撐壓力位。"
                }
            ],
            "sources": []  # 確保預設也是陣列
        }
        return {
            "success": False,
            "section": default_section,
            "error": str(e)
        } 