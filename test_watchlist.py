#!/usr/bin/env python3
"""
測試自選股摘要功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.nodes.generate_watchlist_summary_pipeline import generate_watchlist_summary_pipeline

def test_watchlist_summary():
    """測試自選股摘要功能"""
    print("=== 測試自選股摘要功能 ===")
    
    # 測試股票清單
    test_stock_list = [2303, 2330, 2610, 2376, 2317]  # 聯電、台積電、華航、技嘉、鴻海
    print(f"測試股票清單: {test_stock_list}")
    
    try:
        # 調用自選股摘要 pipeline
        result = generate_watchlist_summary_pipeline(test_stock_list)
        
        if result.get("success"):
            print("✅ 自選股摘要產生成功！")
            print(f"產生 {len(result['sections'])} 個 sections:")
            
            for i, section in enumerate(result['sections'], 1):
                print(f"  {i}. {section['title']}")
                print(f"     內容: {section['content'][:100]}...")
                print(f"     卡片數量: {len(section['cards'])}")
                print()
            
            print("📋 處理日誌:")
            for log in result.get('logs', []):
                print(f"  - {log}")
                
        else:
            print("❌ 自選股摘要產生失敗！")
            print(f"錯誤: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ 測試時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_watchlist_summary() 