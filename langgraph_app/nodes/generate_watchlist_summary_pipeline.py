import json
from typing import Dict, Any, List
from .generate_section_industry_distribution import generate_industry_distribution_section
from .generate_section_price_summary import generate_price_summary_section
from .generate_section_return_analysis import generate_return_analysis_section
from .generate_section_focus_stocks import generate_focus_stocks_section
from .generate_section_industry_comparison import generate_industry_comparison_section

def generate_watchlist_summary_pipeline(stock_list: List[int]) -> Dict[str, Any]:
    """
    產生自選股摘要的完整 pipeline
    
    Args:
        stock_list: 自選股清單 (數字 list)
    
    Returns:
        Dict 包含 success 和 sections 資訊
    """
    try:
        print(f"[DEBUG] ===== 開始產生自選股摘要 ======")
        print(f"[DEBUG] 股票清單: {stock_list}")
        
        all_sections = []
        logs = []
        
        # 0. Mock 社群討論統計 section
        discussion_stats_section = {
            "title": "社群討論統計",
            "type": "discussion_stats",
            "content": "",
            "cards": [
                {
                    "title": "社群討論統計",
                    "type": "discussion_stats",
                    "data": {
                        "discussion_count": 5,
                        "comment_count": 61,
                        "emotions": [
                            {"type": "正面", "post": 2, "comment": 14},
                            {"type": "中性", "post": 3, "comment": 47},
                            {"type": "負面", "post": 0, "comment": 0}
                        ],
                        "market_label": "市場過熱警示"
                    },
                    "insights": [
                        {
                            "title": "輿情變化趨勢",
                            "content": "相較於前一週，討論量下降 45%，顯示市場對該股的關注度下降。情緒則維持穩定，未見大幅反轉。",
                            "why_important": "這能判斷是一時話題熱度還是長期信心變化。"
                        },
                        {
                            "title": "社群 vs. 法人行為對照",
                            "content": "雖社群看法略偏樂觀，但近三日外資持續賣超台積電，出現分歧情形，建議觀察是否為錯殺機會或社群過度樂觀。",
                            "why_important": "可用來偵測「社群情緒反指標」或過熱現象。"
                        },
                        {
                            "title": "關鍵詞雲摘要（情緒視角）",
                            "content": "本週常見正向關鍵詞：「技術支撐」、「營收創高」、「AI 趨勢延續」\n常見負向關鍵詞：「法人轉空」、「600撐不住」、「看空聲音變多」",
                            "why_important": "幫助快速抓到情緒驅動主軸與散戶觀點焦點。"
                        },
                        {
                            "title": "市場過熱警示",
                            "content": "留言數量與正向情緒比例雙雙上升至 80%，應留意是否為過熱跡象，短期內可能出現獲利了結壓力。",
                            "why_important": "可協助辨識短線過熱、過度樂觀訊號，提醒中立觀察。"
                        }
                    ]
                }
            ],
            "sources": []
        }
        all_sections.insert(0, discussion_stats_section)
        
        # 1. 產生產業分布統計
        print(f"\n[DEBUG] ===== 步驟 1: 產生產業分布統計 =====")
        logs.append("步驟 1: 產生產業分布統計")
        industry_result = generate_industry_distribution_section(stock_list)
        if industry_result.get("success"):
            print(f"[DEBUG] append 產業分布統計 section")
            all_sections.append(industry_result["section"])
        else:
            print(f"[ERROR] 產業分布統計失敗: {industry_result.get('error')}")
            logs.append(f"產業分布統計失敗: {industry_result.get('error')}")
        
        # 1.5 產生自選股 vs 同產業指數表現
        print(f"\n[DEBUG] ===== 步驟 1.5: 產生自選股 vs 同產業指數表現 =====")
        logs.append("步驟 1.5: 產生自選股 vs 同產業指數表現")
        try:
            industry_comparison_result = generate_industry_comparison_section(stock_list)
            if industry_comparison_result.get("success"):
                print(f"[DEBUG] append 自選股 vs 同產業指數表現 section")
                all_sections.append(industry_comparison_result["section"])
            else:
                print(f"[ERROR] 自選股 vs 同產業指數表現失敗: {industry_comparison_result.get('error')}")
                logs.append(f"自選股 vs 同產業指數表現失敗: {industry_comparison_result.get('error')}")
        except Exception as e:
            print(f"[ERROR] 產生自選股 vs 同產業指數表現時發生錯誤: {e}")
            logs.append(f"產生自選股 vs 同產業指數表現時發生錯誤: {e}")
        
        # 2. 產生股價摘要
        print(f"\n[DEBUG] ===== 步驟 2: 產生股價摘要 =====")
        logs.append("步驟 2: 產生股價摘要")
        price_result = generate_price_summary_section(stock_list)
        price_data = None
        if price_result.get("success"):
            print(f"[DEBUG] append 股價摘要 section")
            all_sections.append(price_result["section"])
            price_data = price_result.get("price_data")  # 保存股價資料供後續使用
        else:
            print(f"[ERROR] 股價摘要失敗: {price_result.get('error')}")
            logs.append(f"股價摘要失敗: {price_result.get('error')}")
        
        # 3. 產生報酬率統計分析
        print(f"\n[DEBUG] ===== 步驟 3: 產生報酬率統計分析 =====")
        logs.append("步驟 3: 產生報酬率統計分析")
        if price_data:
            return_result = generate_return_analysis_section(price_data)
            if return_result.get("success"):
                print(f"[DEBUG] append 報酬率統計分析 section")
                all_sections.append(return_result["section"])
            else:
                print(f"[ERROR] 報酬率統計分析失敗: {return_result.get('error')}")
                logs.append(f"報酬率統計分析失敗: {return_result.get('error')}")
        else:
            print(f"[WARNING] 沒有股價資料，跳過報酬率統計分析")
            logs.append("沒有股價資料，跳過報酬率統計分析")
        
        # 4. 產生異動焦點個股
        print(f"\n[DEBUG] ===== 步驟 4: 產生異動焦點個股 =====")
        logs.append("步驟 4: 產生異動焦點個股")
        focus_result = generate_focus_stocks_section(stock_list, price_data)
        if focus_result.get("success"):
            print(f"[DEBUG] append 異動焦點個股 section")
            all_sections.append(focus_result["section"])
        else:
            print(f"[ERROR] 異動焦點個股失敗: {focus_result.get('error')}")
            logs.append(f"異動焦點個股失敗: {focus_result.get('error')}")
        
        # 5. 添加資料來源 section
        print(f"\n[DEBUG] ===== 步驟 5: 添加資料來源 =====")
        logs.append("步驟 5: 添加資料來源")
        sources_section = {
            "title": "資料來源",
            "content": "本報告資料來源包括：\n• Finlab 台股資料庫\n• Serper API 搜尋結果",
            "cards": [
                {
                    "title": "資料來源說明",
                    "content": "本報告資料來源包括：\n• Finlab 台股資料庫：公司基本資訊、收盤價資料\n• Serper API：股票相關最新消息",
                    "type": "text"
                }
            ],
            "sources": [
                {
                    "name": "Finlab 台股資料庫",
                    "url": "https://finlab.tw/",
                    "description": "台股公司基本資訊與歷史價格資料"
                },
                {
                    "name": "Serper API",
                    "url": "https://serper.dev/",
                    "description": "股票相關最新消息搜尋"
                }
            ]
        }
        all_sections.append(sources_section)
        
        # 6. 添加免責聲明 section
        print(f"\n[DEBUG] ===== 步驟 6: 添加免責聲明 =====")
        logs.append("步驟 6: 添加免責聲明")
        disclaimer_section = {
            "title": "免責聲明",
            "content": "本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險。",
            "cards": [
                {
                    "title": "免責聲明",
                    "content": "本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險。",
                    "type": "text"
                }
            ],
            "sources": []
        }
        all_sections.append(disclaimer_section)
        
        print(f"\n[DEBUG] ===== 自選股摘要產生完成 =====")
        print(f"[DEBUG] 總共產生 {len(all_sections)} 個 sections")
        print(f"[DEBUG] Sections: {[section['title'] for section in all_sections]}")
        
        return {
            "success": True,
            "sections": all_sections,
            "logs": logs
        }
        
    except Exception as e:
        print(f"[ERROR] 產生自選股摘要時發生錯誤: {e}")
        return {
            "success": False,
            "error": f"產生自選股摘要時發生錯誤: {e}",
            "sections": [],
            "logs": []
        }

def generate_watchlist_summary_sse_pipeline(stock_list: List[int]):
    """
    SSE 版本：每個步驟即時 yield log，最後 yield 完成訊息和所有 sections
    """
    try:
        all_sections = []
        # 1. 產業分布統計
        log = "步驟 1: 產生產業分布統計"
        yield log, None
        industry_result = generate_industry_distribution_section(stock_list)
        if industry_result.get("success"):
            all_sections.append(industry_result["section"])
        else:
            yield f"產業分布統計失敗: {industry_result.get('error')}", None
        # 1.5 自選股 vs 同產業指數表現
        log = "步驟 1.5: 產生自選股 vs 同產業指數表現"
        yield log, None
        try:
            industry_comparison_result = generate_industry_comparison_section(stock_list)
            if industry_comparison_result.get("success"):
                all_sections.append(industry_comparison_result["section"])
            else:
                yield f"自選股 vs 同產業指數表現失敗: {industry_comparison_result.get('error')}", None
        except Exception as e:
            yield f"產生自選股 vs 同產業指數表現時發生錯誤: {e}", None
        # 2. 股價摘要
        log = "步驟 2: 產生股價摘要"
        yield log, None
        price_result = generate_price_summary_section(stock_list)
        price_data = None
        if price_result.get("success"):
            all_sections.append(price_result["section"])
            price_data = price_result.get("price_data")
        else:
            yield f"股價摘要失敗: {price_result.get('error')}", None
        # 3. 報酬率統計分析
        log = "步驟 3: 產生報酬率統計分析"
        yield log, None
        if price_data:
            return_result = generate_return_analysis_section(price_data)
            if return_result.get("success"):
                all_sections.append(return_result["section"])
            else:
                yield f"報酬率統計分析失敗: {return_result.get('error')}", None
        else:
            yield "沒有股價資料，跳過報酬率統計分析", None
        # 4. 異動焦點個股
        log = "步驟 4: 產生異動焦點個股"
        yield log, None
        focus_result = generate_focus_stocks_section(stock_list, price_data)
        if focus_result.get("success"):
            all_sections.append(focus_result["section"])
        else:
            yield f"異動焦點個股失敗: {focus_result.get('error')}", None
        # 5. 資料來源
        log = "步驟 5: 添加資料來源"
        yield log, None
        sources_section = {
            "title": "資料來源",
            "content": "本報告資料來源包括：\n• Finlab 台股資料庫\n• Serper API 搜尋結果",
            "cards": [
                {
                    "title": "資料來源說明",
                    "content": "本報告資料來源包括：\n• Finlab 台股資料庫：公司基本資訊、收盤價資料\n• Serper API：股票相關最新消息",
                    "type": "text"
                }
            ],
            "sources": [
                {
                    "name": "Finlab 台股資料庫",
                    "url": "https://finlab.tw/",
                    "description": "台股公司基本資訊與歷史價格資料"
                },
                {
                    "name": "Serper API",
                    "url": "https://serper.dev/",
                    "description": "股票相關最新消息搜尋"
                }
            ]
        }
        all_sections.append(sources_section)
        # 6. 免責聲明
        log = "步驟 6: 添加免責聲明"
        yield log, None
        disclaimer_section = {
            "title": "免責聲明",
            "content": "本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險。",
            "cards": [
                {
                    "title": "免責聲明",
                    "content": "本報告僅供參考，不構成投資建議。投資人應自行承擔投資風險。",
                    "type": "text"
                }
            ],
            "sources": []
        }
        all_sections.append(disclaimer_section)
        # 完成
        yield "✅ 自選股摘要分析完成", all_sections
    except Exception as e:
        yield f"❌ 產生自選股摘要時發生錯誤: {e}", None

# 測試用
if __name__ == "__main__":
    test_stock_list = [2303, 2330, 2610, 2376, 2317]
    result = generate_watchlist_summary_pipeline(test_stock_list)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 