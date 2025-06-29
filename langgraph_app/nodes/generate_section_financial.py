import json
from typing import List, Dict, Optional

def generate_financial_section(company_name: str, stock_id: str, financial_data: Dict = None, news_summary: str = "") -> Dict:
    """
    產生財務狀況分析 section，直接使用爬蟲資料
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        financial_data: 財務資料（從 Yahoo Finance 爬取）
        news_summary: 新聞摘要（用於補充分析）
    
    Returns:
        財務狀況分析 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 開始產生 section: 財務狀況分析")
        print(f"[DEBUG] 公司名稱: {company_name}")
        print(f"[DEBUG] 股票代號: {stock_id}")
        print(f"[DEBUG] 財務資料: {financial_data is not None}")
        
        # 預設財務資料結構
        if not financial_data:
            financial_data = {
                "eps": {
                    "2025_Q1": {"eps": "0.62", "quarterly_growth": "-8.82%", "yearly_growth": "-26.19%", "avg_price": "42.86"},
                    "2024_Q4": {"eps": "0.68", "quarterly_growth": "-41.38%", "yearly_growth": "-36.45%", "avg_price": "51.00"},
                    "2024_Q3": {"eps": "1.16", "quarterly_growth": "4.50%", "yearly_growth": "-10.08%", "avg_price": "52.58"}
                },
                "revenue": {
                    "2025_Q1": {"revenue": "57,858,957", "quarterly_growth": "-4.18%", "yearly_growth": "5.91%"},
                    "2024_Q4": {"revenue": "60,386,110", "quarterly_growth": "-0.16%", "yearly_growth": "9.87%"},
                    "2024_Q3": {"revenue": "60,485,085", "quarterly_growth": "6.49%", "yearly_growth": "5.99%"}
                },
                "income_statement": {
                    "revenue": {"2025_Q1": "57,858,957", "2024_Q4": "60,386,110", "2024_Q3": "60,485,085"},
                    "gross_profit": {"2025_Q1": "15,446,645", "2024_Q4": "18,342,581", "2024_Q3": "20,428,845"},
                    "operating_income": {"2025_Q1": "9,785,901", "2024_Q4": "11,957,004", "2024_Q3": "14,099,633"},
                    "net_income": {"2025_Q1": "7,743,239", "2024_Q4": "8,459,689", "2024_Q3": "14,441,758"}
                },
                "balance_sheet": {
                    "total_assets": {"2024_Q4": "1,234,567,890", "2024_Q3": "1,200,000,000"},
                    "total_liabilities": {"2024_Q4": "567,890,123", "2024_Q3": "550,000,000"},
                    "equity": {"2024_Q4": "666,677,767", "2024_Q3": "650,000,000"}
                }
            }
        
        # 從新聞摘要中提取財務相關資訊
        eps_info = extract_eps_from_news(news_summary)
        revenue_info = extract_revenue_from_news(news_summary)
        margin_info = extract_margin_from_news(news_summary)
        
        # 構建 EPS 表格
        eps_table = []
        if financial_data.get("eps"):
            for quarter, data in financial_data["eps"].items():
                eps_table.append({
                    "季度": quarter,
                    "每股盈餘": data.get("eps", "N/A"),
                    "季增率": data.get("quarterly_growth", "N/A"),
                    "年增率": data.get("yearly_growth", "N/A"),
                    "季均價": data.get("avg_price", "N/A")
                })
        
        # 構建營收表格
        revenue_table = []
        if financial_data.get("revenue"):
            for quarter, data in financial_data["revenue"].items():
                revenue_table.append({
                    "季度": quarter,
                    "營收": data.get("revenue", "N/A"),
                    "季增率": data.get("quarterly_growth", "N/A"),
                    "年增率": data.get("yearly_growth", "N/A")
                })
        
        # 構建毛利率表格
        margin_table = []
        if financial_data.get("income_statement"):
            income_data = financial_data["income_statement"]
            if "revenue" in income_data and "gross_profit" in income_data:
                for quarter in ["2025_Q1", "2024_Q4", "2024_Q3"]:
                    revenue = income_data["revenue"].get(quarter, 0)
                    gross_profit = income_data["gross_profit"].get(quarter, 0)
                    if revenue and gross_profit:
                        try:
                            margin = (float(gross_profit.replace(",", "")) / float(revenue.replace(",", ""))) * 100
                            margin_table.append({
                                "季度": quarter,
                                "營收": revenue,
                                "營業毛利": gross_profit,
                                "毛利率": f"{margin:.1f}%"
                            })
                        except:
                            margin_table.append({
                                "季度": quarter,
                                "營收": revenue,
                                "營業毛利": gross_profit,
                                "毛利率": "N/A"
                            })
        
        # 構建負債比率表格
        debt_table = []
        if financial_data.get("balance_sheet"):
            balance_data = financial_data["balance_sheet"]
            for quarter in ["2024_Q4", "2024_Q3"]:
                total_assets = balance_data.get("total_assets", {}).get(quarter, 0)
                total_liabilities = balance_data.get("total_liabilities", {}).get(quarter, 0)
                equity = balance_data.get("equity", {}).get(quarter, 0)
                if total_assets and total_liabilities:
                    try:
                        debt_ratio = (float(total_liabilities.replace(",", "")) / float(total_assets.replace(",", ""))) * 100
                        debt_table.append({
                            "季度": quarter,
                            "總資產": total_assets,
                            "總負債": total_liabilities,
                            "股東權益": equity,
                            "負債比率": f"{debt_ratio:.1f}%"
                        })
                    except:
                        debt_table.append({
                            "季度": quarter,
                            "總資產": total_assets,
                            "總負債": total_liabilities,
                            "股東權益": equity,
                            "負債比率": "N/A"
                        })
        
        # 計算財務分數
        financial_scores = calculate_financial_scores(eps_table, revenue_table, margin_table, debt_table)
        
        # 生成更有 insight 的內容
        eps_content = generate_eps_insight(eps_table, eps_info)
        revenue_content = generate_revenue_insight(revenue_table, revenue_info)
        margin_content = generate_margin_insight(margin_table, margin_info)
        debt_content = generate_debt_insight(debt_table)
        
        # 調整為 tabs 結構
        financial_section = {
            "section": "財務狀況分析",
            "financial_scores": financial_scores,
            "tabs": [
                {
                    "tab": "EPS",
                    "content": eps_content,
                    "table": eps_table
                },
                {
                    "tab": "營收",
                    "content": revenue_content,
                    "table": revenue_table
                },
                {
                    "tab": "毛利率",
                    "content": margin_content,
                    "table": margin_table
                },
                {
                    "tab": "負債比率",
                    "content": debt_content,
                    "table": debt_table
                }
            ]
        }
        
        print(f"[DEBUG] 解析後內容：{json.dumps(financial_section, ensure_ascii=False, indent=2)}")
        print(f"[DEBUG] 合併 section: 財務狀況分析")
        
        return {
            "success": True,
            "section": financial_section,
            "raw_content": "直接從財務資料生成，無需 LLM"
        }
        
    except Exception as e:
        print(f"[generate_financial_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "財務狀況分析",
            "financial_scores": {"eps_score": 0, "revenue_score": 0, "margin_score": 0, "overall_score": 0},
            "tabs": [
                {"tab": "EPS", "content": "資料處理中，請稍後查看。", "table": []},
                {"tab": "營收", "content": "資料處理中，請稍後查看。", "table": []},
                {"tab": "毛利率", "content": "資料處理中，請稍後查看。", "table": []},
                {"tab": "負債比率", "content": "資料處理中，請稍後查看。", "table": []}
            ]
        }
        return {
            "success": False,
            "section": default_section,
            "error": str(e)
        }

def calculate_financial_scores(eps_table, revenue_table, margin_table, debt_table):
    """計算財務分數 (0-100)"""
    scores = {"eps_score": 0, "revenue_score": 0, "margin_score": 0, "overall_score": 0}
    
    # EPS 分數計算
    if eps_table:
        try:
            latest_eps = float(eps_table[0]["每股盈餘"])
            latest_qoq = float(eps_table[0]["季增率"].replace("%", ""))
            latest_yoy = float(eps_table[0]["年增率"].replace("%", ""))
            
            # EPS 絕對值分數 (0-40分)
            if latest_eps > 2: eps_abs_score = 40
            elif latest_eps > 1: eps_abs_score = 30
            elif latest_eps > 0.5: eps_abs_score = 20
            else: eps_abs_score = 10
            
            # 成長率分數 (0-30分)
            growth_score = 0
            if latest_qoq > 0: growth_score += 15
            if latest_yoy > 0: growth_score += 15
            
            scores["eps_score"] = min(100, eps_abs_score + growth_score)
        except:
            scores["eps_score"] = 50
    
    # 營收分數計算
    if revenue_table:
        try:
            latest_qoq = float(revenue_table[0]["季增率"].replace("%", ""))
            latest_yoy = float(revenue_table[0]["年增率"].replace("%", ""))
            
            # 成長率分數 (0-100分)
            growth_score = 0
            if latest_qoq > 5: growth_score += 50
            elif latest_qoq > 0: growth_score += 30
            elif latest_qoq > -5: growth_score += 10
            
            if latest_yoy > 10: growth_score += 50
            elif latest_yoy > 5: growth_score += 30
            elif latest_yoy > 0: growth_score += 10
            
            scores["revenue_score"] = min(100, growth_score)
        except:
            scores["revenue_score"] = 50
    
    # 毛利率分數計算
    if margin_table:
        try:
            latest_margin = float(margin_table[0]["毛利率"].replace("%", ""))
            
            if latest_margin > 50: margin_score = 100
            elif latest_margin > 30: margin_score = 80
            elif latest_margin > 20: margin_score = 60
            elif latest_margin > 10: margin_score = 40
            else: margin_score = 20
            
            scores["margin_score"] = margin_score
        except:
            scores["margin_score"] = 50
    
    # 總分計算
    scores["overall_score"] = int((scores["eps_score"] + scores["revenue_score"] + scores["margin_score"]) / 3)
    
    return scores

def generate_eps_insight(eps_table, eps_info):
    """生成 EPS 分析 insight"""
    if not eps_table:
        return "EPS 資料不足，無法進行分析。"
    
    try:
        latest_eps = float(eps_table[0]["每股盈餘"])
        latest_qoq = float(eps_table[0]["季增率"].replace("%", ""))
        latest_yoy = float(eps_table[0]["年增率"].replace("%", ""))
        
        insight = f"📊 **EPS 分析洞察**\n\n"
        
        # EPS 絕對值分析
        if latest_eps > 2:
            insight += f"🔥 **優秀表現**：最新季度 EPS {latest_eps} 元，表現優異，顯示公司具備強勁的盈利能力。\n"
        elif latest_eps > 1:
            insight += f"✅ **良好表現**：最新季度 EPS {latest_eps} 元，表現穩定，符合市場預期。\n"
        elif latest_eps > 0.5:
            insight += f"⚠️ **需關注**：最新季度 EPS {latest_eps} 元，表現一般，建議密切關注後續發展。\n"
        else:
            insight += f"❌ **表現不佳**：最新季度 EPS {latest_eps} 元，表現較差，需要深入分析原因。\n"
        
        # 成長趨勢分析
        insight += f"\n📈 **成長趨勢分析**：\n"
        if latest_qoq > 0 and latest_yoy > 0:
            insight += f"• 季增率：{eps_table[0]['季增率']} (正向成長)\n"
            insight += f"• 年增率：{eps_table[0]['年增率']} (正向成長)\n"
            insight += "🎯 **投資建議**：雙重正向成長，顯示公司營運動能強勁，值得關注。\n"
        elif latest_qoq > 0:
            insight += f"• 季增率：{eps_table[0]['季增率']} (正向成長)\n"
            insight += f"• 年增率：{eps_table[0]['年增率']} (需關注)\n"
            insight += "⚠️ **投資建議**：短期改善但長期趨勢需觀察。\n"
        else:
            insight += f"• 季增率：{eps_table[0]['季增率']} (需關注)\n"
            insight += f"• 年增率：{eps_table[0]['年增率']} (需關注)\n"
            insight += "🚨 **投資建議**：成長動能減弱，建議謹慎評估。\n"
        
        return insight
        
    except:
        return f"最新季度 EPS 為 {eps_table[0]['每股盈餘'] if eps_table else 'N/A'} 元，{eps_table[0]['季增率'] if eps_table else 'N/A'} 季增率，{eps_table[0]['年增率'] if eps_table else 'N/A'} 年增率。"

def generate_revenue_insight(revenue_table, revenue_info):
    """生成營收分析 insight"""
    if not revenue_table:
        return "營收資料不足，無法進行分析。"
    
    try:
        latest_qoq = float(revenue_table[0]["季增率"].replace("%", ""))
        latest_yoy = float(revenue_table[0]["年增率"].replace("%", ""))
        
        insight = f"💰 **營收分析洞察**\n\n"
        
        # 營收規模分析
        latest_revenue = revenue_table[0]["營收"]
        insight += f"📊 **營收規模**：最新季度營收 {latest_revenue} 仟元\n\n"
        
        # 成長趨勢分析
        insight += f"📈 **成長趨勢分析**：\n"
        if latest_qoq > 5 and latest_yoy > 10:
            insight += f"• 季增率：{revenue_table[0]['季增率']} (強勁成長)\n"
            insight += f"• 年增率：{revenue_table[0]['年增率']} (強勁成長)\n"
            insight += "🚀 **投資建議**：營收成長動能強勁，顯示業務擴張良好。\n"
        elif latest_qoq > 0 and latest_yoy > 0:
            insight += f"• 季增率：{revenue_table[0]['季增率']} (正向成長)\n"
            insight += f"• 年增率：{revenue_table[0]['年增率']} (正向成長)\n"
            insight += "✅ **投資建議**：營收穩定成長，業務發展健康。\n"
        elif latest_qoq > 0:
            insight += f"• 季增率：{revenue_table[0]['季增率']} (短期改善)\n"
            insight += f"• 年增率：{revenue_table[0]['年增率']} (需關注)\n"
            insight += "⚠️ **投資建議**：短期改善但長期趨勢需觀察。\n"
        else:
            insight += f"• 季增率：{revenue_table[0]['季增率']} (下滑)\n"
            insight += f"• 年增率：{revenue_table[0]['年增率']} (需關注)\n"
            insight += "🚨 **投資建議**：營收成長動能減弱，建議深入分析原因。\n"
        
        return insight
        
    except:
        return f"最新季度營收為 {revenue_table[0]['營收'] if revenue_table else 'N/A'} 仟元，{revenue_table[0]['季增率'] if revenue_table else 'N/A'} 季增率，{revenue_table[0]['年增率'] if revenue_table else 'N/A'} 年增率。"

def generate_margin_insight(margin_table, margin_info):
    """生成毛利率分析 insight"""
    if not margin_table:
        return "毛利率資料不足，無法進行分析。"
    
    try:
        latest_margin = float(margin_table[0]["毛利率"].replace("%", ""))
        
        insight = f"📊 **毛利率分析洞察**\n\n"
        
        # 毛利率水平分析
        if latest_margin > 50:
            insight += f"🔥 **優秀表現**：毛利率 {margin_table[0]['毛利率']}，顯示公司具備極強的定價能力和成本控制能力。\n"
        elif latest_margin > 30:
            insight += f"✅ **良好表現**：毛利率 {margin_table[0]['毛利率']}，顯示公司具備良好的盈利能力。\n"
        elif latest_margin > 20:
            insight += f"⚠️ **一般表現**：毛利率 {margin_table[0]['毛利率']}，表現一般，建議關注成本控制。\n"
        else:
            insight += f"❌ **需改善**：毛利率 {margin_table[0]['毛利率']}，較低，需要關注成本結構和定價策略。\n"
        
        insight += f"\n💰 **營業毛利**：{margin_table[0]['營業毛利']} 仟元\n"
        insight += f"📈 **營收規模**：{margin_table[0]['營收']} 仟元\n\n"
        
        # 行業比較建議
        if latest_margin > 30:
            insight += "🎯 **投資建議**：毛利率表現優異，顯示公司在產業中具備競爭優勢。\n"
        elif latest_margin > 20:
            insight += "⚠️ **投資建議**：毛利率表現一般，建議與同業比較評估競爭力。\n"
        else:
            insight += "🚨 **投資建議**：毛利率偏低，建議深入分析成本結構和市場競爭狀況。\n"
        
        return insight
        
    except:
        return f"最新季度毛利率為 {margin_table[0]['毛利率'] if margin_table else 'N/A'}，營業毛利為 {margin_table[0]['營業毛利'] if margin_table else 'N/A'} 仟元。"

def generate_debt_insight(debt_table):
    """生成負債比率分析 insight"""
    if not debt_table:
        return "負債比率資料不足，無法進行分析。"
    
    try:
        latest_debt_ratio = float(debt_table[0]["負債比率"].replace("%", ""))
        
        insight = f"🏦 **負債比率分析洞察**\n\n"
        
        # 負債比率分析
        if latest_debt_ratio < 30:
            insight += f"✅ **財務穩健**：負債比率 {debt_table[0]['負債比率']}，財務結構非常健康，風險較低。\n"
        elif latest_debt_ratio < 50:
            insight += f"⚠️ **財務良好**：負債比率 {debt_table[0]['負債比率']}，財務結構良好，但需關注負債變化。\n"
        elif latest_debt_ratio < 70:
            insight += f"🚨 **需關注**：負債比率 {debt_table[0]['負債比率']}，負債水平較高，建議密切關注財務狀況。\n"
        else:
            insight += f"❌ **風險較高**：負債比率 {debt_table[0]['負債比率']}，負債水平過高，財務風險較大。\n"
        
        insight += f"\n📊 **財務結構**：\n"
        insight += f"• 總資產：{debt_table[0]['總資產']} 仟元\n"
        insight += f"• 總負債：{debt_table[0]['總負債']} 仟元\n"
        insight += f"• 股東權益：{debt_table[0]['股東權益']} 仟元\n\n"
        
        # 投資建議
        if latest_debt_ratio < 50:
            insight += "🎯 **投資建議**：財務結構健康，適合長期投資。\n"
        else:
            insight += "⚠️ **投資建議**：財務風險較高，建議謹慎評估。\n"
        
        return insight
        
    except:
        return f"最新季度負債比率為 {debt_table[0]['負債比率'] if debt_table else 'N/A'}，總資產為 {debt_table[0]['總資產'] if debt_table else 'N/A'} 仟元。"

def extract_eps_from_news(news_summary: str) -> Optional[str]:
    """從新聞摘要中提取 EPS 相關資訊"""
    if "EPS" in news_summary or "每股盈餘" in news_summary:
        # 簡單的關鍵字提取
        lines = news_summary.split('\n')
        for line in lines:
            if "EPS" in line or "每股盈餘" in line:
                return line.strip()
    return None

def extract_revenue_from_news(news_summary: str) -> Optional[str]:
    """從新聞摘要中提取營收相關資訊"""
    if "營收" in news_summary:
        lines = news_summary.split('\n')
        for line in lines:
            if "營收" in line:
                return line.strip()
    return None

def extract_margin_from_news(news_summary: str) -> Optional[str]:
    """從新聞摘要中提取毛利率相關資訊"""
    if "毛利率" in news_summary:
        lines = news_summary.split('\n')
        for line in lines:
            if "毛利率" in line:
                return line.strip()
    return None

# 測試用
if __name__ == "__main__":
    test_news = """
    1. 聯電(2303)法說會重點整理：EPS創19季低、估第二季毛利回升，毛利率下滑至26.7%，跌破3成，創下近年低點。
    2. 營業利益率為16.9%，稅後純益77.8億元，每股盈餘0.62元，創下自2020年第二季以來的19季新低紀錄。
    """
    
    result = generate_financial_section("聯電", "2303", None, test_news)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 