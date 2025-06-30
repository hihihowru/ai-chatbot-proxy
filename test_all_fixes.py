#!/usr/bin/env python3
"""
測試所有修改是否正確
"""

import sys
import os
import json

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.nodes.generate_section_strategy import generate_strategy_section
from langgraph_app.nodes.generate_section_financial import generate_financial_section

def test_strategy_section():
    """測試投資策略建議 section"""
    print("=== 測試投資策略建議 Section ===")
    
    company_name = "聯電"
    stock_id = "2303"
    news_summary = "聯電近期財報表現良好，營業利益率維持在較高水平。"
    news_sources = [
        {"title": "聯電財報亮眼", "link": "https://example.com/news1"},
        {"title": "聯電技術實力受認可", "link": "https://example.com/news2"}
    ]
    
    try:
        result = generate_strategy_section(company_name, stock_id, news_summary, None, news_sources)
        
        print(f"成功: {result.get('success', False)}")
        
        if result.get('success'):
            section = result.get('section', {})
            print(f"Section 標題: {section.get('section', 'N/A')}")
            
            cards = section.get('cards', [])
            print(f"Cards 數量: {len(cards)}")
            
            for i, card in enumerate(cards):
                print(f"\n--- Card {i+1}: {card.get('title', 'N/A')} ---")
                print(f"建議: {card.get('suggestion', 'N/A')}")
                
                bullets = card.get('bullets', [])
                print(f"要點數量: {len(bullets)}")
                for j, bullet in enumerate(bullets):
                    print(f"  要點 {j+1}: {bullet}")
        else:
            print(f"錯誤: {result.get('error', '未知錯誤')}")
        
    except Exception as e:
        print(f"測試失敗: {e}")

def test_financial_section():
    """測試財務狀況分析 section"""
    print("\n=== 測試財務狀況分析 Section ===")
    
    # 模擬 FinLab API 的財務資料
    financial_data = {
        "quarterly": {
            "2024Q1": {"每股純益": 1.2, "營收": 100000, "營業利益": 15000},
            "2024Q2": {"每股純益": 1.5, "營收": 120000, "營業利益": 18000},
            "2024Q3": {"每股純益": 1.8, "營收": 140000, "營業利益": 21000},
            "2024Q4": {"每股純益": 2.0, "營收": 160000, "營業利益": 24000},
            "2023Q1": {"每股純益": 1.0, "營收": 90000, "營業利益": 12000},
            "2023Q2": {"每股純益": 1.3, "營收": 110000, "營業利益": 15000},
            "2023Q3": {"每股純益": 1.6, "營收": 130000, "營業利益": 19000},
            "2023Q4": {"每股純益": 1.9, "營收": 150000, "營業利益": 22000},
        }
    }
    
    company_name = "聯電"
    stock_id = "2303"
    news_summary = "聯電近期財報表現良好，營業利益率維持在較高水平。"
    
    try:
        result = generate_financial_section(company_name, stock_id, financial_data, news_summary)
        
        print(f"成功: {result.get('success', False)}")
        
        if result.get('success'):
            section = result.get('section', {})
            print(f"Section 標題: {section.get('section', 'N/A')}")
            
            tabs = section.get('tabs', [])
            print(f"Tabs 數量: {len(tabs)}")
            
            for i, tab in enumerate(tabs):
                print(f"\n--- Tab {i+1}: {tab.get('tab', 'N/A')} ---")
                print(f"內容: {tab.get('content', 'N/A')}")
                
                table = tab.get('table', [])
                print(f"表格行數: {len(table)}")
                if table:
                    print(f"表格欄位: {list(table[0].keys()) if table else 'N/A'}")
                    print(f"第一行資料: {table[0] if table else 'N/A'}")
        else:
            print(f"錯誤: {result.get('error', '未知錯誤')}")
        
    except Exception as e:
        print(f"測試失敗: {e}")

if __name__ == "__main__":
    test_strategy_section()
    test_financial_section() 