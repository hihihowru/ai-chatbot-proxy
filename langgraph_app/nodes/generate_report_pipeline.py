import json
import sys
import os
from typing import List, Dict
import openai

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph_app.nodes.generate_section_price_movement import generate_price_movement_section
from langgraph_app.nodes.generate_section_financial import generate_financial_section
from langgraph_app.nodes.generate_section_strategy import generate_strategy_section
from langgraph_app.nodes.generate_section_social_sentiment import generate_social_sentiment_section
from langgraph_app.nodes.generate_section_notice import generate_notice_section
from langgraph_app.nodes.generate_section_sources import generate_sources_section
from langgraph_app.nodes.generate_section_disclaimer import generate_disclaimer_section
from langgraph_app.nodes.generate_section_institutional_trend import generate_institutional_trend_section

def generate_report_pipeline(
    company_name: str,
    stock_id: str,
    intent: str = "",
    time_info: str = "",
    news_summary: str = "",
    news_sources: List[Dict] = None,
    financial_data: Dict = None,
    financial_sources: List[Dict] = None
) -> Dict:
    """
    主 pipeline：整合所有 section 節點，產生完整的投資分析報告
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        intent: 搜尋意圖
        time_info: 時間資訊
        news_summary: 新聞摘要
        news_sources: 新聞來源列表
        financial_data: 財務資料
        financial_sources: 財務資料來源列表
    
    Returns:
        完整的投資分析報告
    """
    try:
        print(f"[DEBUG] ===== 開始執行投資分析報告 pipeline =====")
        print(f"[DEBUG] 公司名稱: {company_name}")
        print(f"[DEBUG] 股票代號: {stock_id}")
        print(f"[DEBUG] 搜尋意圖: {intent}")
        print(f"[DEBUG] 新聞摘要長度: {len(news_summary)}")
        print(f"[DEBUG] 新聞來源數量: {len(news_sources) if news_sources else 0}")
        print(f"[DEBUG] 財務資料: {financial_data is not None}")
        
        # 初始化 logs
        logs = []
        logs.append(f"[{time_info}] 開始產生 {company_name}({stock_id}) 投資分析報告")
        
        all_sections = []
        section_results = {}
        
        # 1. 產生股價異動總結
        print(f"\n[DEBUG] ===== 步驟 1: 產生股價異動總結 =====")
        logs.append("步驟 1: 產生股價異動總結")
        price_result = generate_price_movement_section(company_name, stock_id, news_summary, news_sources)
        if price_result.get("success"):
            print(f"[DEBUG] append 股價異動總結 section: {json.dumps(price_result['section'], ensure_ascii=False)}")
            # 只萃取實際用到的來源
            used_indices = set()
            for card in price_result["section"].get("cards", []):
                # 找出所有 [來源X]
                import re
                matches = re.findall(r"\[來源(\d+)\]", card.get("content", ""))
                for m in matches:
                    try:
                        idx = int(m) - 1
                        if news_sources and 0 <= idx < len(news_sources):
                            used_indices.add(idx)
                    except Exception:
                        pass
            # 按照出現順序組成 sources 陣列
            sources = [news_sources[i] for i in sorted(used_indices)] if news_sources else []
            price_result["section"]["sources"] = sources
            all_sections.append(price_result["section"])
            section_results["股價異動總結"] = price_result
            logs.append("✅ 股價異動總結產生成功")
            print(f"[DEBUG] ✅ 股價異動總結產生成功")
        else:
            print(f"[DEBUG] ❌ 股價異動總結產生失敗: {price_result.get('error', '未知錯誤')}")
            price_result["section"]["sources"] = news_sources
            all_sections.append(price_result["section"])  # 使用預設內容
            logs.append("❌ 股價異動總結產生失敗，使用預設內容")
        
        # 1.5 產生法人動向分析
        print(f"\n[DEBUG] ===== 步驟 1.5: 產生法人動向分析 =====")
        logs.append("步驟 1.5: 產生法人動向分析")
        try:
            institutional_result = generate_institutional_trend_section(stock_id)
            all_sections.append(institutional_result)
            logs.append("✅ 法人動向分析產生成功")
            print(f"[DEBUG] ✅ 法人動向分析產生成功")
        except Exception as e:
            logs.append(f"❌ 法人動向分析產生失敗: {e}")
            print(f"[DEBUG] ❌ 法人動向分析產生失敗: {e}")
        
        # 2. 產生財務狀況分析
        print(f"\n[DEBUG] ===== 步驟 2: 產生財務狀況分析 =====")
        logs.append("步驟 2: 產生財務狀況分析")
        financial_result = generate_financial_section(company_name, stock_id, financial_data, news_summary)
        if financial_result.get("success"):
            print(f"[DEBUG] append 財務狀況分析 section: {json.dumps(financial_result['section'], ensure_ascii=False)}")
            # 添加 sources 資訊到 section
            financial_result["section"]["sources"] = news_sources
            all_sections.append(financial_result["section"])
            section_results["財務狀況分析"] = financial_result
            logs.append("✅ 財務狀況分析產生成功")
            print(f"[DEBUG] ✅ 財務狀況分析產生成功")
        else:
            print(f"[DEBUG] ❌ 財務狀況分析產生失敗: {financial_result.get('error', '未知錯誤')}")
            financial_result["section"]["sources"] = news_sources
            all_sections.append(financial_result["section"])  # 使用預設內容
            logs.append("❌ 財務狀況分析產生失敗，使用預設內容")
        
        # 3. 產生投資策略建議
        print(f"\n[DEBUG] ===== 步驟 3: 產生投資策略建議 =====")
        logs.append("步驟 3: 產生投資策略建議")
        strategy_result = generate_strategy_section(company_name, stock_id, news_summary, financial_data, news_sources)
        if strategy_result.get("success"):
            print(f"[DEBUG] append 投資策略建議 section: {json.dumps(strategy_result['section'], ensure_ascii=False)}")
            # 添加 sources 資訊到 section
            strategy_result["section"]["sources"] = news_sources
            all_sections.append(strategy_result["section"])
            section_results["投資策略建議"] = strategy_result
            logs.append("✅ 投資策略建議產生成功")
            print(f"[DEBUG] ✅ 投資策略建議產生成功")
        else:
            print(f"[DEBUG] ❌ 投資策略建議產生失敗: {strategy_result.get('error', '未知錯誤')}")
            strategy_result["section"]["sources"] = news_sources
            all_sections.append(strategy_result["section"])  # 使用預設內容
            logs.append("❌ 投資策略建議產生失敗，使用預設內容")
        
        # 4. 產生爆料同學會輿情分析
        print(f"\n[DEBUG] ===== 步驟 4: 產生爆料同學會輿情分析 =====")
        logs.append("步驟 4: 產生爆料同學會輿情分析")
        sentiment_result = generate_social_sentiment_section(company_name, stock_id)
        if sentiment_result.get("success"):
            print(f"[DEBUG] append 爆料同學會輿情分析 section: {json.dumps(sentiment_result['section'], ensure_ascii=False)}")
            # 添加 sources 資訊到 section
            sentiment_result["section"]["sources"] = []
            all_sections.append(sentiment_result["section"])
            section_results["爆料同學會輿情分析"] = sentiment_result
            logs.append("✅ 爆料同學會輿情分析產生成功")
            print(f"[DEBUG] ✅ 爆料同學會輿情分析產生成功")
        else:
            print(f"[DEBUG] ❌ 爆料同學會輿情分析產生失敗: {sentiment_result.get('error', '未知錯誤')}")
            sentiment_result["section"]["sources"] = []
            all_sections.append(sentiment_result["section"])  # 使用預設內容
            logs.append("❌ 爆料同學會輿情分析產生失敗，使用預設內容")
        
        # 5. 產生操作注意事項
        print(f"\n[DEBUG] ===== 步驟 5: 產生操作注意事項 =====")
        logs.append("步驟 5: 產生操作注意事項")
        notice_result = generate_notice_section(company_name, stock_id, news_summary)
        if notice_result.get("success"):
            print(f"[DEBUG] append 操作注意事項 section: {json.dumps(notice_result['section'], ensure_ascii=False)}")
            # 添加 sources 資訊到 section
            notice_result["section"]["sources"] = news_sources
            all_sections.append(notice_result["section"])
            section_results["操作注意事項"] = notice_result
            logs.append("✅ 操作注意事項產生成功")
            print(f"[DEBUG] ✅ 操作注意事項產生成功")
        else:
            print(f"[DEBUG] ❌ 操作注意事項產生失敗: {notice_result.get('error', '未知錯誤')}")
            notice_result["section"]["sources"] = news_sources
            all_sections.append(notice_result["section"])  # 使用預設內容
            logs.append("❌ 操作注意事項產生失敗，使用預設內容")
        
        # 6. 產生資料來源
        print(f"\n[DEBUG] ===== 步驟 6: 產生資料來源 =====")
        logs.append("步驟 6: 產生資料來源")
        sources_result = generate_sources_section(news_sources, financial_sources)
        if sources_result.get("success"):
            print(f"[DEBUG] append 資料來源 section: {json.dumps(sources_result['section'], ensure_ascii=False)}")
            all_sections.append(sources_result["section"])
            section_results["資料來源"] = sources_result
            logs.append("✅ 資料來源產生成功")
            print(f"[DEBUG] ✅ 資料來源產生成功")
        else:
            print(f"[DEBUG] ❌ 資料來源產生失敗: {sources_result.get('error', '未知錯誤')}")
            all_sections.append(sources_result["section"])  # 使用預設內容
            logs.append("❌ 資料來源產生失敗，使用預設內容")
        
        # 7. 產生免責聲明
        print(f"\n[DEBUG] ===== 步驟 7: 產生免責聲明 =====")
        logs.append("步驟 7: 產生免責聲明")
        disclaimer_result = generate_disclaimer_section()
        if disclaimer_result.get("success"):
            print(f"[DEBUG] append 免責聲明 section: {json.dumps(disclaimer_result['section'], ensure_ascii=False)}")
            all_sections.append(disclaimer_result["section"])
            section_results["免責聲明"] = disclaimer_result
            logs.append("✅ 免責聲明產生成功")
            print(f"[DEBUG] ✅ 免責聲明產生成功")
        else:
            print(f"[DEBUG] ❌ 免責聲明產生失敗: {disclaimer_result.get('error', '未知錯誤')}")
            all_sections.append(disclaimer_result["section"])  # 使用預設內容
            logs.append("❌ 免責聲明產生失敗，使用預設內容")
        
        # 8. 合併所有 section
        print(f"\n[DEBUG] ===== 步驟 8: 合併所有 section =====")
        print(f"[DEBUG] 總共產生 {len(all_sections)} 個 section")
        
        # 直接回傳 list 結構，順序即為 UI 順序
        print(f"[DEBUG] ===== 投資分析報告 pipeline 完成 =====")
        print(f"[DEBUG] 最終 sections 數量: {len(all_sections)}")
        
        # 新增 paraphrased_prompt
        paraphrased_prompt = None
        user_prompt = intent or ""
        if user_prompt:
            try:
                openai_api_key = os.getenv("OPENAI_API_KEY")
                if openai_api_key:
                    client = openai.OpenAI(api_key=openai_api_key)
                    prompt = f"請用更自然、口語化的方式改寫這句投資問題，保持原意但更適合放在報告開頭：\n{user_prompt}"
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5
                    )
                    paraphrased = response.choices[0].message.content.strip()
                    paraphrased_prompt = f"{user_prompt} - {paraphrased}"
                else:
                    paraphrased_prompt = user_prompt
            except Exception as e:
                print(f"[DEBUG] OpenAI paraphrase 失敗: {str(e)}")
                paraphrased_prompt = user_prompt
        
        # 回傳結果
        return {
            "success": True,
            "sections": all_sections,
            "section_results": section_results,
            "company_name": company_name,
            "stock_id": stock_id,
            "intent": intent,
            "time_info": time_info,
            "paraphrased_prompt": paraphrased_prompt,
            "message": f"成功生成投資分析報告，共{len(all_sections)}個 section",
            "logs": logs  # 新增 logs 欄位
        }
        
    except Exception as e:
        print(f"[generate_report_pipeline ERROR] {e}")
        return {
            "success": False,
            "error": str(e),
            "sections": [],
            "section_results": {},
            "company_name": company_name,
            "stock_id": stock_id,
            "intent": intent,
            "logs": logs  # 新增 logs 欄位
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
    
    result = generate_report_pipeline(
        company_name="聯電",
        stock_id="2303",
        intent="個股分析",
        news_summary=test_news,
        news_sources=test_sources
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2)) 