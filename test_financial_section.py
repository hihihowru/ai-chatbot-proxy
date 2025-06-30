#!/usr/bin/env python3
"""
測試財務狀況分析是否能正確處理 FinLab API 資料
"""

import sys
import os

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.nodes.generate_section_financial import generate_financial_section

def test_financial_section():
    """測試財務狀況分析"""
    
    print("=== 測試財務狀況分析 ===")
    
    # 模擬 FinLab API 的財務資料
    financial_data = {
        "income_statement": {
            "2024-Q2": {"營業利益": 13891432, "營業利益率": 24.46},
            "2024-Q3": {"營業利益": 14099633, "營業利益率": 23.31},
            "2024-Q4": {"營業利益": 11957004, "營業利益率": 19.8},
            "2025-Q1": {"營業利益": 9785901, "營業利益率": 16.91}
        }
    }
    
    company_name = "聯電"
    stock_id = "2303"
    news_summary = "聯電近期財報表現良好，營業利益率維持在較高水平。"
    
    try:
        result = generate_financial_section(company_name, stock_id, financial_data, news_summary)
        
        print(f"\n=== 結果 ===")
        print(f"成功: {result.get('success', False)}")
        
        if result.get('success'):
            section = result.get('section', {})
            print(f"Section: {section.get('section', 'N/A')}")
            
            # 檢查財務分數
            financial_scores = section.get('financial_scores', {})
            print(f"財務分數: {financial_scores}")
            
            # 檢查 tabs
            tabs = section.get('tabs', [])
            print(f"Tabs 數量: {len(tabs)}")
            
            for i, tab in enumerate(tabs):
                print(f"\n--- Tab {i+1}: {tab.get('tab', 'N/A')} ---")
                print(f"內容: {tab.get('content', 'N/A')[:100]}...")
                
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
    test_financial_section() 