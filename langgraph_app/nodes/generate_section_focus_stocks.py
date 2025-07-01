import json
import os
import requests
from typing import Dict, Any, List
from .search_news import search_news, generate_search_keywords

def generate_focus_stocks_section(stock_list: List[int], price_data: List[Dict] = None) -> Dict[str, Any]:
    """
    產生異動焦點個股 section，使用 Serper API 搜尋每檔股票的最新消息
    
    Args:
        stock_list: 自選股清單 (數字 list)
        price_data: 股價摘要資料（可選，用於結合報酬率資訊）
    
    Returns:
        Dict 包含 success 和 section 資訊
    """
    try:
        print(f"[DEBUG] 開始產生異動焦點個股，股票清單: {stock_list}")
        
        # 建立股票代號到公司名稱的對應
        stock_name_map = {}
        if price_data:
            for stock in price_data:
                stock_name_map[stock['stock_id']] = stock['company_name']
        
        # 建立股票代號到報酬率的對應
        stock_return_map = {}
        if price_data:
            for stock in price_data:
                stock_return_map[stock['stock_id']] = {
                    '1日報酬': stock.get('1日報酬'),
                    '5日報酬': stock.get('5日報酬'),
                    '20日報酬': stock.get('20日報酬')
                }
        
        focus_stocks_content = "🔍 異動焦點個股\n"
        focus_cards = []
        
        # 為了避免 API 效能問題，只處理前 5 檔股票
        # 優先處理報酬率較高或較低的股票
        processed_stocks = []
        
        if price_data:
            # 根據 20 日報酬率排序，取前 5 名
            sorted_stocks = sorted(price_data, key=lambda x: abs(x.get('20日報酬', 0)), reverse=True)
            top_stocks = sorted_stocks[:5]
            processed_stocks = [stock['stock_id'] for stock in top_stocks]
        else:
            # 如果沒有股價資料，就處理前 5 檔
            processed_stocks = [str(stock_id) for stock_id in stock_list[:5]]
        
        print(f"[DEBUG] 將處理以下股票: {processed_stocks}")
        
        for stock_id in processed_stocks:
            try:
                # 取得公司名稱
                company_name = stock_name_map.get(stock_id, f"股票{stock_id}")
                # 智能生成多組關鍵字
                keywords = generate_search_keywords(company_name, stock_id, "最新消息", [], "", "")
                print(f"[DEBUG] 智能生成關鍵字: {keywords}")
                # 搜尋該股票的最新消息（多組關鍵字合併搜尋）
                search_result = search_news(company_name, stock_id, "最新消息", keywords)
                # 聚合新聞摘要
                if search_result and search_result.get("results") and len(search_result["results"]) > 0:
                    search_results = search_result["results"]
                    # 取近一週、近一月新聞
                    from datetime import datetime, timedelta
                    now = datetime.now()
                    def parse_date(result):
                        date_str = result.get("date") or result.get("publishedDate") or ""
                        try:
                            return datetime.strptime(date_str[:10], "%Y-%m-%d")
                        except Exception:
                            return None
                    recent_news = [r for r in search_results if parse_date(r) and (now - parse_date(r)).days <= 7]
                    month_news = [r for r in search_results if parse_date(r) and (now - parse_date(r)).days <= 31]
                    # 主題分類
                    themes = set()
                    for result in search_results:
                        title = result.get('title', '').lower()
                        snippet = result.get('snippet', '').lower()
                        if any(k in title or k in snippet for k in ['ai', '人工智慧', 'chatgpt']):
                            themes.add('AI 題材')
                        if any(k in title or k in snippet for k in ['重電', '電力', '綠能']):
                            themes.add('重電題材')
                        if any(k in title or k in snippet for k in ['半導體', '晶片', '台積電']):
                            themes.add('半導體題材')
                        if any(k in title or k in snippet for k in ['pc', '筆電', '電腦']):
                            themes.add('PC 題材')
                        if any(k in title or k in snippet for k in ['法人', '外資', '投信']):
                            themes.add('法人動向')
                        if any(k in title or k in snippet for k in ['財報', '營收', '獲利']):
                            themes.add('財報表現')
                        if any(k in title or k in snippet for k in ['新高', '新低', '漲停', '跌停', '創高', '創低']):
                            themes.add('股價異動')
                    # 聚合摘要
                    summary_parts = []
                    if recent_news:
                        summary_parts.append(f"近一週有{len(recent_news)}則新聞")
                    elif month_news:
                        summary_parts.append(f"近一月有{len(month_news)}則新聞")
                    if themes:
                        summary_parts.append(f"主題：{', '.join(themes)}")
                    # 報酬率資訊
                    if stock_id in stock_return_map:
                        returns = stock_return_map[stock_id]
                        day20_return = returns.get('20日報酬', 0)
                        if abs(day20_return) > 5:
                            if day20_return > 0:
                                summary_parts.append(f"20日上漲最多")
                            else:
                                summary_parts.append(f"20日下跌最多")
                    if not summary_parts:
                        summary_parts.append("需關注後續發展")
                    summary = f"{company_name}：{'，'.join(summary_parts)}"
                    focus_stocks_content += f"\t•\t{summary}\n"
                    # 建立卡片
                    focus_cards.append({
                        "title": f"{company_name}({stock_id})",
                        "content": summary,
                        "type": "text",
                        "sources": search_results[:2] if search_results else []
                    })
                else:
                    search_results = []
                    # 如果沒有搜尋結果，使用報酬率資訊
                    if stock_id in stock_return_map:
                        returns = stock_return_map[stock_id]
                        summary = f"{company_name}：20日報酬率 {returns.get('20日報酬', 0):+.1f}%，需關注後續發展"
                    else:
                        summary = f"{company_name}：無最新消息，建議關注基本面"
                    focus_stocks_content += f"\t•\t{summary}\n"
                    focus_cards.append({
                        "title": f"{company_name}({stock_id})",
                        "content": summary,
                        "type": "text"
                    })
                
            except Exception as e:
                print(f"[ERROR] 處理股票 {stock_id} 時發生錯誤: {e}")
                # 使用預設摘要
                company_name = stock_name_map.get(stock_id, f"股票{stock_id}")
                summary = f"{company_name}：資料處理中，請稍後查看"
                focus_stocks_content += f"\t•\t{summary}\n"
                
                focus_cards.append({
                    "title": f"{company_name}({stock_id})",
                    "content": summary,
                    "type": "text"
                })
        
        # 建立 section 結構
        section = {
            "title": "異動焦點個股",
            "content": focus_stocks_content,
            "cards": focus_cards,
            "sources": [
                {
                    "name": "Serper API 搜尋結果",
                    "url": "https://serper.dev/",
                    "description": "股票相關最新消息"
                }
            ]
        }
        
        print(f"[DEBUG] 異動焦點個股 section 建立完成，處理了 {len(processed_stocks)} 檔股票")
        return {
            "success": True,
            "section": section
        }
        
    except Exception as e:
        print(f"[ERROR] 產生異動焦點個股時發生錯誤: {e}")
        return {
            "success": False,
            "error": f"產生異動焦點個股時發生錯誤: {e}"
        }

def generate_stock_summary(stock_id: str, company_name: str, search_results: List[Dict], returns: Dict = None) -> str:
    """
    根據搜尋結果和報酬率資訊，產生股票摘要
    
    Args:
        stock_id: 股票代號
        company_name: 公司名稱
        search_results: 搜尋結果
        returns: 報酬率資訊
    
    Returns:
        摘要文字
    """
    try:
        # 分析搜尋結果的主題
        themes = []
        if search_results:
            for result in search_results:
                title = result.get('title', '').lower()
                snippet = result.get('snippet', '').lower()
            
            # 簡單的主題分類
            if any(keyword in title or keyword in snippet for keyword in ['ai', '人工智慧', 'chatgpt']):
                themes.append('AI 題材')
            elif any(keyword in title or keyword in snippet for keyword in ['重電', '電力', '綠能']):
                themes.append('重電題材')
            elif any(keyword in title or keyword in snippet for keyword in ['半導體', '晶片', '台積電']):
                themes.append('半導體題材')
            elif any(keyword in title or keyword in snippet for keyword in ['pc', '筆電', '電腦']):
                themes.append('PC 題材')
            elif any(keyword in title or keyword in snippet for keyword in ['法人', '外資', '投信']):
                themes.append('法人動向')
            elif any(keyword in title or keyword in snippet for keyword in ['財報', '營收', '獲利']):
                themes.append('財報表現')
        
        # 去重並取前 2 個主題
        themes = list(set(themes))[:2]
        
        # 建立摘要
        summary_parts = []
        
        # 加入報酬率資訊
        if returns:
            day20_return = returns.get('20日報酬', 0)
            if abs(day20_return) > 5:  # 如果 20 日報酬率超過 5%
                if day20_return > 0:
                    summary_parts.append(f"20日上漲最多")
                else:
                    summary_parts.append(f"20日下跌最多")
        
        # 加入主題
        if themes:
            summary_parts.append(f"{', '.join(themes)} 熱")
        
        # 如果沒有特別資訊，使用預設
        if not summary_parts:
            summary_parts.append("需關注後續發展")
        
        summary = f"{company_name}：{'，'.join(summary_parts)}"
        
        return summary
        
    except Exception as e:
        print(f"[ERROR] 產生股票摘要時發生錯誤: {e}")
        return f"{company_name}：資料分析中" 