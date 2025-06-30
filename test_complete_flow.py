#!/usr/bin/env python3
"""
測試完整的投資分析流程，包括財務資料傳遞
"""

import sys
import os
import json

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.nodes.generate_report_pipeline import generate_report_pipeline

def test_complete_flow():
    """測試完整的投資分析流程"""
    
    print("=== 測試完整投資分析流程 ===")
    
    # 模擬輸入資料
    company_name = "聯電"
    stock_id = "2303"
    intent = "請分析聯電的財務狀況"
    time_info = "recent_5_days"
    news_summary = """
    1. 聯電近期財報表現良好，營業利益率維持在較高水平
    2. 聯電在晶圓代工市場佔有率穩定，技術實力受到認可
    3. 聯電積極擴產，預計未來營收將持續成長
    """
    
    # 模擬新聞來源
    news_sources = [
        {"title": "聯電財報亮眼", "link": "https://example.com/news1"},
        {"title": "聯電技術實力受認可", "link": "https://example.com/news2"}
    ]
    
    # 模擬 FinLab API 財務資料
    financial_data = {
        "income_statement": {
            "2024-Q2": {"營業利益": 13891432, "營業利益率": 24.46},
            "2024-Q3": {"營業利益": 14099633, "營業利益率": 23.31},
            "2024-Q4": {"營業利益": 11957004, "營業利益率": 19.8},
            "2025-Q1": {"營業利益": 9785901, "營業利益率": 16.91}
        }
    }
    
    # 模擬財務資料來源
    financial_sources = [
        {"name": "FinLab API - 營業利益", "url": "https://ai.finlab.tw/database"},
        {"name": "FinLab API - 營業利益率", "url": "https://ai.finlab.tw/database"}
    ]
    
    try:
        print(f"公司名稱: {company_name}")
        print(f"股票代號: {stock_id}")
        print(f"財務資料: {financial_data is not None}")
        print(f"財務資料內容: {json.dumps(financial_data, ensure_ascii=False, indent=2)}")
        
        # 執行完整的報告生成流程
        result = generate_report_pipeline(
            company_name=company_name,
            stock_id=stock_id,
            intent=intent,
            time_info=time_info,
            news_summary=news_summary,
            news_sources=news_sources,
            financial_data=financial_data,
            financial_sources=financial_sources
        )
        
        print(f"\n=== 結果 ===")
        print(f"成功: {result.get('success', False)}")
        
        if result.get('success'):
            sections = result.get('sections', [])
            print(f"Sections 數量: {len(sections)}")
            
            # 檢查財務狀況分析 section
            financial_section = None
            for section in sections:
                if section.get('section') == '財務狀況分析':
                    financial_section = section
                    break
            
            if financial_section:
                print(f"\n=== 財務狀況分析 Section ===")
                print(f"財務分數: {financial_section.get('financial_scores', 'N/A')}")
                
                tabs = financial_section.get('tabs', [])
                print(f"Tabs 數量: {len(tabs)}")
                
                for i, tab in enumerate(tabs):
                    print(f"\n--- Tab {i+1}: {tab.get('tab', 'N/A')} ---")
                    print(f"內容: {tab.get('content', 'N/A')[:100]}...")
                    
                    table = tab.get('table', [])
                    print(f"表格行數: {len(table)}")
                    if table:
                        print(f"表格欄位: {list(table[0].keys()) if table else 'N/A'}")
                        print(f"第一行資料: {table[0] if table else 'N/A'}")
                        
                        # 特別檢查營業利益 Tab
                        if tab.get('tab') == '營業利益':
                            print(f"✅ 營業利益 Tab 包含 {len(table)} 筆資料")
                            for row in table:
                                print(f"  季度: {row.get('季度', 'N/A')}, 營業利益: {row.get('營業利益', 'N/A')}, 營業利益率: {row.get('營業利益率', 'N/A')}")
            else:
                print("❌ 未找到財務狀況分析 section")
            
            # 檢查 paraphrased_prompt
            paraphrased_prompt = result.get('paraphrased_prompt')
            if paraphrased_prompt:
                print(f"\n=== 改寫後的問題 ===")
                print(f"原始問題: {intent}")
                print(f"改寫後: {paraphrased_prompt}")
        else:
            print(f"錯誤: {result.get('error', '未知錯誤')}")
        
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_flow() 