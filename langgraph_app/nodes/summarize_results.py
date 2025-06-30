import openai
import json
from typing import List, Dict
import os

SUMMARIZER_PROMPTS = {
    "price_movement_analysis": """
你是一位專業的證券分析師，請根據輸入的公司代號與近期市場變化，分析該股票在特定日期發生漲停、跌停或劇烈變動的可能原因。

請整合以下資訊來源（若有）並條列分析：
1. 法人動向（外資、投信、自營商）
2. 大戶買賣或主力進出
3. 技術面變化（如均線交叉、支撐壓力、過熱）
4. 新聞面與事件驅動（ETF換股、法說會、財報、利多利空）
5. 整體盤勢與資金流動影響

禁止主觀預測，請保持中立、資訊客觀。
""",

    "financial_summary": """
請整理可查得的財務數據，包括：
- 每股盈餘 (EPS)：最新季度、年增率、季增率趨勢
- 營收表現：最新營收、年增率、季增率趨勢
- 損益表重點：營業收入、營業毛利、營業利益、稅後淨利
- 資產負債表重點：資產總計、負債總計、股東權益
- 財務比率：毛利率、營業利益率、淨利率、ROE、ROA
- 現金流量：營業現金流、投資現金流、籌資現金流

如果沒有 Yahoo 財經數據，請從新聞內容中提取相關財務資訊。

請以「根據 Yahoo 財經財務報表」或「根據公開資料」語氣呈現，不做任何投資建議。
""",

    "industry_context": """
請說明該股票所屬產業的近期趨勢與環境概況，包含：
- 近期熱門題材（如 AI、生技、重電等）
- 同產業競爭對手概況
- 大盤與總體經濟變數（如利率、原物料價格、外銷）

請維持客觀、不評論買賣。
""",

    "analyst_estimate": """
請整理可查得的分析師預估數據，包括：
- 今年度(2025) EPS 預估值：中位數、最高值、最低值、分析師人數
- 明年度(2026) EPS 預估值：中位數、最高值、最低值、分析師人數  
- 目標價：中位數、最高值、最低值、分析師人數
- 投資建議分布：買進、持有、賣出比例
- 市場共識語氣（如偏多、中性、偏空）

如果沒有分析師預估數據，請從新聞內容中提取相關分析師預估資訊。

請以「根據市場分析師預估」或「根據公開資料」語氣呈現，不做任何投資建議。
""",

    "investment_strategy_by_time": """
針對不同投資期間，請說明該股票在不同時間架構中，投資者可觀察的變數與可能思考角度：

- 📉 日內（當沖、短線）：量價異動、技術型態
- 🔄 短線（1–5 日）：消息面效應、主力籌碼行為
- 📅 中期（1–3 週）：法人佈局、題材反應、法說會
- 🧭 長期（1–3 月以上）：基本面趨勢、EPS 預估、產業趨勢

提供思考依據，不給予明確操作建議。
""",

    "action_recommendation": """
根據上述分析，請以簡要方式列出對不同類型投資人（如短線交易者、長線持有者）可考慮的策略方向，並說明原因。

舉例格式：
- 短線建議：保守觀望 / 技術整理中
- 中期觀點：中性偏多，關注 XXX 指標
- 長線看法：基本面仍穩健，但建議逢回佈局

建議語氣需謹慎，保持資訊中立與保留空間。
""",

    "risk_assessment": """
請條列該股票可能面臨的投資風險與觀察點，包括但不限於：
- 產業競爭風險
- 獲利不如預期風險
- 法人籌碼轉弱風險
- 技術面轉空或跌破支撐
- 大盤或總體環境惡化風險

請盡量貼近該股票實際情境。
""",

    "disclaimer": """
免責聲明：
本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險，並在投資前充分了解相關風險。過往績效不代表未來表現，投資有賺有賠，投資人應審慎評估。
""",

    "data_sources": """
資料來源：
請整理本報告使用的所有資料來源，包括：
- Yahoo 財經財務報表連結
- 新聞來源
- 其他公開資料來源

請以「本報告資料來源：」開頭，列出所有使用的資料連結。
"""
}

def summarize_results(company_name: str, stock_id: str, news_results: List[Dict], user_input: str, factset_data: str = "", news_sources: List[Dict] = None, financial_sources: List[Dict] = None) -> Dict:
    """
    使用 OpenAI 生成投資分析報告摘要
    """
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 準備新聞內容
        news_content = ""
        for i, news in enumerate(news_results[:20]):  # 限制前20則新聞
            title = news.get("title", "")
            snippet = news.get("snippet", "")
            news_content += f"新聞{i+1}: {title}\n{snippet}\n\n"
        
        # 構建完整的提示詞
        full_prompt = f"""
請根據以下資訊，為 {company_name}({stock_id}) 生成一份詳細的投資分析報告。

用戶問題：{user_input}

{factset_data}

相關新聞：
{news_content}

請按照以下8個面向生成分析報告：

1. 📈 股價變動分析
{SUMMARIZER_PROMPTS['price_movement_analysis']}

2. 📊 財務數據摘要
{SUMMARIZER_PROMPTS['financial_summary']}

3. 🌐 產業環境分析
{SUMMARIZER_PROMPTS['industry_context']}

4. 🎯 分析師預估
{SUMMARIZER_PROMPTS['analyst_estimate']}

5. ⏰ 投資策略建議
{SUMMARIZER_PROMPTS['investment_strategy_by_time']}

6. 💡 操作建議
{SUMMARIZER_PROMPTS['action_recommendation']}

7. ⚠️ 風險評估
{SUMMARIZER_PROMPTS['risk_assessment']}

請確保每個面向都有詳細的分析內容。
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一位專業的證券分析師，擅長分析台股個股。"},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        summary = response.choices[0].message.content
        
        # 解析摘要為不同的 sections
        sections = parse_summary_sections(summary)
        
        # 添加資料來源 section
        if news_sources or financial_sources:
            sources_content = []
            
            if news_sources and isinstance(news_sources, list):
                sources_content.append("📰 新聞資料來源：")
                for source in news_sources:
                    if isinstance(source, dict):
                        title = source.get('title', '無標題')
                        link = source.get('link', '')
                        if link:
                            sources_content.append(f"• <a href='{link}' target='_blank'>{title}</a>")
                        else:
                            sources_content.append(f"• {title}")
                sources_content.append("")
            
            if financial_sources and isinstance(financial_sources, list):
                sources_content.append("📊 財務資料來源：")
                for source in financial_sources:
                    if isinstance(source, dict):
                        name = source.get('name', '未知來源')
                        url = source.get('url', '')
                        if url:
                            sources_content.append(f"• <a href='{url}' target='_blank'>{name}</a>")
                        else:
                            sources_content.append(f"• {name}")
            
            sections["📚 資料來源"] = '\n'.join(sources_content)
        
        # 添加免責聲明 section
        disclaimer_content = """本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險，並在投資前充分了解相關風險。

• 本報告所載資料僅供參考，不保證其準確性、完整性或時效性
• 投資有風險，入市需謹慎，過往表現不代表未來表現
• 投資人應根據自身風險承受能力做出投資決策
• 本報告不構成任何投資建議或推薦"""
        
        sections["⚖️ 免責聲明"] = disclaimer_content
        
        return {
            "success": True,
            "sections": sections,
            "raw_summary": summary
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def parse_summary_sections(summary: str) -> Dict[str, str]:
    """
    解析摘要內容為不同的 sections
    """
    sections = {}
    current_section = ""
    current_content = []
    
    lines = summary.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 檢查是否為 section 標題（更寬鬆的匹配）
        if (any(keyword in line for keyword in ['📈', '📊', '🌐', '🎯', '⏰', '💡', '⚠️']) or
            any(keyword in line for keyword in ['股價變動分析', '財務數據摘要', '產業環境分析', '分析師預估', '投資策略建議', '操作建議', '風險評估']) or
            (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.')) and any(keyword in line for keyword in ['📈', '📊', '🌐', '🎯', '⏰', '💡', '⚠️']))):
            
            # 保存前一個 section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # 開始新的 section
            current_section = line
            current_content = []
        else:
            # 添加到當前 section 內容
            if current_section:
                current_content.append(line)
    
    # 保存最後一個 section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    # 如果沒有解析到任何 section，嘗試手動分割
    if not sections and summary:
        # 根據關鍵字手動分割
        section_keywords = [
            ('📈 股價變動分析', '📈'),
            ('📊 財務數據摘要', '📊'),
            ('🌐 產業環境分析', '🌐'),
            ('🎯 分析師預估', '🎯'),
            ('⏰ 投資策略建議', '⏰'),
            ('💡 操作建議', '💡'),
            ('⚠️ 風險評估', '⚠️')
        ]
        
        for section_title, emoji in section_keywords:
            if emoji in summary:
                # 找到該 section 的開始位置
                start_idx = summary.find(emoji)
                if start_idx != -1:
                    # 找到下一個 section 的開始位置
                    next_start = -1
                    for next_emoji in ['📈', '📊', '🌐', '🎯', '⏰', '💡', '⚠️']:
                        if next_emoji != emoji:
                            next_idx = summary.find(next_emoji, start_idx + 1)
                            if next_idx != -1 and (next_start == -1 or next_idx < next_start):
                                next_start = next_idx
                    
                    # 提取 section 內容
                    if next_start != -1:
                        section_content = summary[start_idx:next_start].strip()
                    else:
                        section_content = summary[start_idx:].strip()
                    
                    # 移除標題，只保留內容
                    lines = section_content.split('\n')
                    if lines and emoji in lines[0]:
                        content_lines = lines[1:]
                        sections[section_title] = '\n'.join(content_lines).strip()
                    else:
                        sections[section_title] = section_content
    
    return sections

# 測試用
if __name__ == "__main__":
    test_results = [
        {
            "title": "華碩股價分析",
            "snippet": "華碩(2357)近期股價表現強勁，主要受惠於AI PC需求成長...",
            "link": "https://example.com/news1"
        },
        {
            "title": "華碩財報亮眼",
            "snippet": "華碩最新財報顯示EPS成長15%，營收創新高...",
            "link": "https://example.com/news2"
        }
    ]
    
    result = summarize_results("華碩", "2357", test_results, "華碩股價分析")
    print(json.dumps(result, ensure_ascii=False, indent=2)) 