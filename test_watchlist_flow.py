#!/usr/bin/env python3
"""
測試自選股摘要完整流程
"""

import requests
import json
import time

def test_watchlist_summary_flow():
    """測試自選股摘要流程"""
    
    # 測試資料
    test_data = {
        "stock_list": [2330, 2454, 2317],  # 台積電、聯發科、鴻海
        "userId": "test_user"
    }
    
    print("=== 測試自選股摘要流程 ===")
    print(f"股票清單: {test_data['stock_list']}")
    print()
    
    try:
        # 1. 調用後端 API
        print("1. 調用後端 watchlist-summary API...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8000/watchlist-summary",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        end_time = time.time()
        print(f"API 回應時間: {end_time - start_time:.2f} 秒")
        print(f"HTTP 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data.get('success')}")
            
            if data.get('success'):
                print(f"Sections 數量: {len(data.get('sections', []))}")
                print(f"Logs 數量: {len(data.get('logs', []))}")
                
                # 顯示 logs
                print("\n=== 分析 Logs ===")
                for i, log in enumerate(data.get('logs', []), 1):
                    print(f"{i}. {log}")
                
                # 顯示 sections
                print("\n=== Sections 標題 ===")
                for i, section in enumerate(data.get('sections', []), 1):
                    print(f"{i}. {section.get('title', '無標題')}")
                
            else:
                print(f"錯誤: {data.get('error')}")
        else:
            print(f"API 錯誤: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到後端 API (http://localhost:8000)")
        print("請確保後端伺服器正在運行")
    except Exception as e:
        print(f"❌ 測試時發生錯誤: {e}")

def test_frontend_api():
    """測試前端 API 代理"""
    
    test_data = {
        "stock_list": [2330, 2454, 2317],
        "userId": "test_user"
    }
    
    print("\n=== 測試前端 API 代理 ===")
    
    try:
        response = requests.post(
            "http://localhost:3000/api/watchlist-summary",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"前端 API 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"前端代理成功: {data.get('success')}")
        else:
            print(f"前端代理錯誤: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到前端 API (http://localhost:3000)")
        print("請確保前端開發伺服器正在運行")
    except Exception as e:
        print(f"❌ 前端測試時發生錯誤: {e}")

if __name__ == "__main__":
    test_watchlist_summary_flow()
    test_frontend_api() 