#!/usr/bin/env python3
"""
完整測試自選股摘要功能
包括 API 端點測試
"""

import sys
import os
import requests
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_backend_api():
    """測試後端 API 端點"""
    print("=== 測試後端 API 端點 ===")
    
    url = "http://localhost:8000/watchlist-summary"
    test_data = {
        "stock_list": [2303, 2330, 2610, 2376, 2317],
        "userId": "test-user"
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"API 回應狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API 端點測試成功！")
            print(f"回應內容: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ API 端點測試失敗，狀態碼: {response.status_code}")
            print(f"錯誤內容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到後端服務器，請確認服務器是否正在運行")
    except Exception as e:
        print(f"❌ API 測試時發生錯誤: {e}")

def test_pipeline_direct():
    """直接測試 pipeline"""
    print("\n=== 直接測試 Pipeline ===")
    
    try:
        from langgraph_app.nodes.generate_watchlist_summary_pipeline import generate_watchlist_summary_pipeline
        
        test_stock_list = [2303, 2330, 2610, 2376, 2317]
        result = generate_watchlist_summary_pipeline(test_stock_list)
        
        if result.get("success"):
            print("✅ Pipeline 測試成功！")
            print(f"產生 {len(result['sections'])} 個 sections:")
            
            for i, section in enumerate(result['sections'], 1):
                print(f"  {i}. {section['title']}")
                print(f"     內容: {section['content'][:100]}...")
                print(f"     卡片數量: {len(section['cards'])}")
                print()
        else:
            print("❌ Pipeline 測試失敗！")
            print(f"錯誤: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Pipeline 測試時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("開始測試自選股摘要功能...\n")
    
    # 測試 Pipeline
    test_pipeline_direct()
    
    # 測試 API 端點
    test_backend_api()
    
    print("\n測試完成！") 