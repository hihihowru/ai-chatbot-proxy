#!/usr/bin/env python3
"""
測試生產環境 API 狀態
"""

import requests
import json
import time

def test_production_api():
    """測試生產環境 API"""
    
    # 可能的生產環境 URL
    production_urls = [
        "https://your-app-name.herokuapp.com",
        "https://your-app-name.railway.app", 
        "https://your-app-name.onrender.com",
        "https://your-app-name.fly.dev",
        "https://your-backend-domain.com"
    ]
    
    # 測試端點
    test_endpoints = [
        "/",
        "/docs",
        "/api/watchlist-summary",
        "/api/ask",
        "/health"
    ]
    
    print("=== 生產環境 API 測試 ===")
    
    for base_url in production_urls:
        print(f"\n🔍 測試 URL: {base_url}")
        
        for endpoint in test_endpoints:
            url = f"{base_url}{endpoint}"
            try:
                if endpoint == "/api/watchlist-summary":
                    # POST 請求
                    response = requests.post(
                        url,
                        json={"stock_list": [2330, 2454], "userId": "test"},
                        timeout=10
                    )
                else:
                    # GET 請求
                    response = requests.get(url, timeout=10)
                
                print(f"  ✅ {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    print(f"     內容長度: {len(response.text)} 字元")
                    
            except requests.exceptions.ConnectionError:
                print(f"  ❌ {endpoint}: 連接失敗")
            except requests.exceptions.Timeout:
                print(f"  ⏰ {endpoint}: 請求超時")
            except Exception as e:
                print(f"  ❌ {endpoint}: 錯誤 - {e}")

def test_watchlist_summary():
    """測試自選股摘要功能"""
    
    # 請替換為您的實際生產環境 URL
    production_url = "https://your-backend-domain.com"
    
    test_data = {
        "stock_list": [2330, 2454, 2317],  # 台積電、聯發科、鴻海
        "userId": "test_user"
    }
    
    print(f"\n=== 測試自選股摘要功能 ===")
    print(f"URL: {production_url}/api/watchlist-summary")
    print(f"測試資料: {test_data}")
    
    try:
        response = requests.post(
            f"{production_url}/api/watchlist-summary",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"HTTP 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功: {data.get('success')}")
            print(f"Sections 數量: {len(data.get('sections', []))}")
            print(f"Logs 數量: {len(data.get('logs', []))}")
            
            # 顯示前幾個 logs
            for i, log in enumerate(data.get('logs', [])[:5], 1):
                print(f"  {i}. {log}")
                
        else:
            print(f"❌ 錯誤: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到生產環境 API")
        print("請檢查：")
        print("1. URL 是否正確")
        print("2. 應用是否正在運行")
        print("3. 防火牆設定")
    except requests.exceptions.Timeout:
        print("⏰ 請求超時")
        print("可能原因：")
        print("1. 應用正在啟動中")
        print("2. 網路延遲")
        print("3. 應用負載過高")
    except Exception as e:
        print(f"❌ 測試時發生錯誤: {e}")

def check_environment_variables():
    """檢查環境變數"""
    print("\n=== 環境變數檢查 ===")
    
    required_vars = [
        "OPENAI_API_KEY",
        "SERPER_API_KEY"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 只顯示前10個字元
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: 未設定")

if __name__ == "__main__":
    import os
    
    print("🔧 生產環境診斷工具")
    print("請先更新 production_urls 列表中的 URL")
    
    # 檢查環境變數
    check_environment_variables()
    
    # 測試 API
    test_production_api()
    
    # 測試特定功能
    test_watchlist_summary()
    
    print("\n📋 檢查清單：")
    print("1. 確認生產環境 URL 是否正確")
    print("2. 檢查應用是否正在運行")
    print("3. 檢查環境變數是否設定")
    print("4. 檢查網路連接")
    print("5. 查看部署平台的日誌") 