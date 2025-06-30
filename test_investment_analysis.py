#!/usr/bin/env python3
"""
測試投資分析系統
"""

import requests
import json
import time

# API 基礎 URL
BASE_URL = "http://localhost:8000"

def test_investment_analysis():
    """測試投資分析 API"""
    print("🧪 測試投資分析系統...")
    
    # 測試問題
    test_questions = [
        "華碩前天漲停板但今天下跌，是什麼原因",
        "台積電這季財報怎麼樣？",
        "請給我2330的法人買賣超"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 測試 {i}: {question}")
        
        # 發送請求
        try:
            response = requests.post(
                f"{BASE_URL}/api/investment-analysis",
                json={"question": question},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    print("✅ 分析成功")
                    print(f"   公司: {result.get('company_name')} ({result.get('stock_id')})")
                    print(f"   意圖: {result.get('intent')}")
                    print(f"   搜尋關鍵詞: {result.get('search_keywords', [])}")
                    print(f"   搜尋結果數: {len(result.get('search_results', []))}")
                    print(f"   報告長度: {len(result.get('report', ''))} 字元")
                    
                    # 顯示日誌
                    print("   日誌:")
                    for log in result.get('logs', []):
                        print(f"     {log}")
                    
                    # 顯示報告摘要
                    if result.get('report'):
                        print("   報告摘要:")
                        report_lines = result.get('report', '').split('\n')[:5]
                        for line in report_lines:
                            if line.strip():
                                print(f"     {line}")
                else:
                    print(f"❌ 分析失敗: {result.get('error')}")
            else:
                print(f"❌ HTTP 錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 請求失敗: {str(e)}")

def test_sse_investment_analysis():
    """測試 SSE 投資分析"""
    print("\n🔄 測試 SSE 投資分析...")
    
    question = "華碩前天漲停板但今天下跌，是什麼原因"
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/investment-analysis-sse",
            params={"question": question},
            stream=True,
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ SSE 連接成功")
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # 移除 'data: ' 前綴
                        try:
                            event_data = json.loads(data)
                            
                            if 'log' in event_data:
                                print(f"📝 {event_data['log']}")
                            elif 'result' in event_data:
                                result = event_data['result']
                                print(f"✅ 分析完成: {result.get('company_name')} ({result.get('stock_id')})")
                                break
                            elif 'error' in event_data:
                                print(f"❌ 錯誤: {event_data['error']}")
                                break
                                
                        except json.JSONDecodeError:
                            continue
        else:
            print(f"❌ SSE 連接失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ SSE 測試失敗: {str(e)}")

def test_individual_nodes():
    """測試個別節點"""
    print("\n🔧 測試個別節點...")
    
    # 測試 classify_and_extract
    try:
        from langgraph_app.nodes.classify_and_extract import classify_and_extract
        
        result = classify_and_extract("華碩前天漲停板但今天下跌，是什麼原因")
        print("✅ classify_and_extract 測試成功")
        print(f"   結果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"❌ classify_and_extract 測試失敗: {str(e)}")
    
    # 測試 search_news
    try:
        from langgraph_app.nodes.search_news import search_news
        
        result = search_news("華碩", "2357", "股價分析", ["漲停", "下跌"])
        print("✅ search_news 測試成功")
        print(f"   搜尋關鍵詞: {result.get('search_keywords')}")
        print(f"   結果數: {len(result.get('results', []))}")
        
    except Exception as e:
        print(f"❌ search_news 測試失敗: {str(e)}")

if __name__ == "__main__":
    print("🚀 開始測試投資分析系統...")
    
    # 測試個別節點
    test_individual_nodes()
    
    # 測試完整分析流程
    test_investment_analysis()
    
    # 測試 SSE
    test_sse_investment_analysis()
    
    print("\n✨ 測試完成！") 