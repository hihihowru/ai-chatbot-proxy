#!/usr/bin/env python3
"""
測試 Yahoo Finance API 和其他可能的財務數據來源
"""

import requests
import json
import sys
import os

def test_yahoo_finance_api():
    """測試 Yahoo Finance API"""
    
    stock_id = "2303.TW"  # 聯電
    
    print(f"=== 測試 Yahoo Finance API ===")
    print(f"股票代號: {stock_id}")
    
    # 測試不同的 API 端點
    api_endpoints = [
        {
            "name": "Yahoo Finance API (v8)",
            "url": f"https://query2.finance.yahoo.com/v8/finance/chart/{stock_id}?interval=1d&range=1y"
        },
        {
            "name": "Yahoo Finance Key Statistics",
            "url": f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{stock_id}?modules=defaultKeyStatistics,financialData,summaryDetail"
        },
        {
            "name": "Yahoo Finance Income Statement",
            "url": f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{stock_id}?modules=incomeStatementHistory,incomeStatementHistoryQuarterly"
        },
        {
            "name": "Yahoo Finance Balance Sheet",
            "url": f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{stock_id}?modules=balanceSheetHistory,balanceSheetHistoryQuarterly"
        },
        {
            "name": "Yahoo Finance Cash Flow",
            "url": f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{stock_id}?modules=cashflowStatementHistory,cashflowStatementHistoryQuarterly"
        }
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://finance.yahoo.com/"
    }
    
    for endpoint in api_endpoints:
        print(f"\n--- 測試 {endpoint['name']} ---")
        print(f"URL: {endpoint['url']}")
        
        try:
            response = requests.get(endpoint["url"], headers=headers, timeout=10)
            print(f"狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ 成功獲取 JSON 數據")
                    
                    # 檢查數據結構
                    if "quoteSummary" in data:
                        result = data["quoteSummary"]["result"][0]
                        modules = list(result.keys())
                        print(f"可用模組: {modules}")
                        
                        # 檢查財務數據
                        if "financialData" in result:
                            financial_data = result["financialData"]
                            print(f"財務數據: {json.dumps(financial_data, ensure_ascii=False, indent=2)}")
                        
                        if "incomeStatementHistoryQuarterly" in result:
                            income_data = result["incomeStatementHistoryQuarterly"]
                            print(f"季度損益表: {json.dumps(income_data, ensure_ascii=False, indent=2)}")
                        
                        if "balanceSheetHistoryQuarterly" in result:
                            balance_data = result["balanceSheetHistoryQuarterly"]
                            print(f"季度資產負債表: {json.dumps(balance_data, ensure_ascii=False, indent=2)}")
                    
                    elif "chart" in data:
                        chart_data = data["chart"]
                        print(f"圖表數據: {json.dumps(chart_data, ensure_ascii=False, indent=2)}")
                    
                    else:
                        print(f"數據結構: {list(data.keys())}")
                        print(f"數據樣本: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}...")
                
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 解析失敗: {str(e)}")
                    print(f"回應內容: {response.text[:200]}...")
            
            else:
                print(f"❌ HTTP 請求失敗: {response.status_code}")
                print(f"回應內容: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ 請求失敗: {str(e)}")
            continue

def test_alternative_sources():
    """測試其他可能的財務數據來源"""
    
    print(f"\n=== 測試其他數據來源 ===")
    
    # 測試 Goodinfo
    print(f"\n--- 測試 Goodinfo ---")
    goodinfo_url = "https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID=2303"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(goodinfo_url, headers=headers, timeout=10)
        print(f"Goodinfo 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Goodinfo 可訪問")
            # 檢查是否有財務數據
            if "每股盈餘" in response.text or "EPS" in response.text:
                print("✅ 找到財務數據關鍵字")
            else:
                print("❌ 未找到財務數據關鍵字")
        else:
            print("❌ Goodinfo 無法訪問")
    
    except Exception as e:
        print(f"❌ Goodinfo 請求失敗: {str(e)}")
    
    # 測試 CMoney
    print(f"\n--- 測試 CMoney ---")
    cmoney_url = "https://www.cmoney.tw/finance/f00025.aspx?s=2303"
    
    try:
        response = requests.get(cmoney_url, headers=headers, timeout=10)
        print(f"CMoney 狀態碼: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ CMoney 可訪問")
            if "每股盈餘" in response.text or "EPS" in response.text:
                print("✅ 找到財務數據關鍵字")
            else:
                print("❌ 未找到財務數據關鍵字")
        else:
            print("❌ CMoney 無法訪問")
    
    except Exception as e:
        print(f"❌ CMoney 請求失敗: {str(e)}")

def test_yfinance_library():
    """測試 yfinance 函式庫"""
    
    print(f"\n=== 測試 yfinance 函式庫 ===")
    
    try:
        import yfinance as yf
        
        stock_id = "2303.TW"
        print(f"股票代號: {stock_id}")
        
        # 獲取股票資訊
        stock = yf.Ticker(stock_id)
        
        # 獲取財務報表
        print(f"\n--- 獲取財務報表 ---")
        
        # 季度損益表
        try:
            income_stmt = stock.quarterly_income_stmt
            print(f"✅ 季度損益表: {income_stmt.shape if hasattr(income_stmt, 'shape') else '無數據'}")
            if not income_stmt.empty:
                print(f"損益表數據: {income_stmt.head()}")
        except Exception as e:
            print(f"❌ 季度損益表失敗: {str(e)}")
        
        # 季度資產負債表
        try:
            balance_sheet = stock.quarterly_balance_sheet
            print(f"✅ 季度資產負債表: {balance_sheet.shape if hasattr(balance_sheet, 'shape') else '無數據'}")
            if not balance_sheet.empty:
                print(f"資產負債表數據: {balance_sheet.head()}")
        except Exception as e:
            print(f"❌ 季度資產負債表失敗: {str(e)}")
        
        # 季度現金流量表
        try:
            cash_flow = stock.quarterly_cashflow
            print(f"✅ 季度現金流量表: {cash_flow.shape if hasattr(cash_flow, 'shape') else '無數據'}")
            if not cash_flow.empty:
                print(f"現金流量表數據: {cash_flow.head()}")
        except Exception as e:
            print(f"❌ 季度現金流量表失敗: {str(e)}")
        
        # 獲取財務指標
        try:
            info = stock.info
            print(f"✅ 股票資訊: {len(info)} 個欄位")
            
            # 顯示關鍵財務指標
            key_metrics = ['trailingPE', 'forwardPE', 'marketCap', 'enterpriseValue', 
                          'trailingEps', 'forwardEps', 'bookValue', 'priceToBook']
            
            for metric in key_metrics:
                if metric in info:
                    print(f"{metric}: {info[metric]}")
        
        except Exception as e:
            print(f"❌ 股票資訊失敗: {str(e)}")
    
    except ImportError:
        print("❌ yfinance 函式庫未安裝")
        print("請執行: pip install yfinance")
    except Exception as e:
        print(f"❌ yfinance 測試失敗: {str(e)}")

if __name__ == "__main__":
    test_yahoo_finance_api()
    test_alternative_sources()
    test_yfinance_library() 