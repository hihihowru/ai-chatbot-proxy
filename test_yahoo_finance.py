#!/usr/bin/env python3
"""
測試 Yahoo Finance 爬蟲功能
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import os

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_yahoo_finance_crawler():
    """測試 Yahoo Finance 爬蟲"""
    
    stock_id = "2303"  # 聯電
    company_name = "聯電"
    
    print(f"=== 測試 Yahoo Finance 爬蟲 ===")
    print(f"股票代號: {stock_id}")
    print(f"公司名稱: {company_name}")
    
    # 定義要爬取的財務報表類型
    financial_types = [
        {"type": "eps", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/eps", "name": "每股盈餘"},
        {"type": "revenue", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/revenue", "name": "營收表"},
        {"type": "income_statement", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/income-statement", "name": "損益表"},
        {"type": "balance_sheet", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/balance-sheet", "name": "資產負債表"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    financial_data = {
        "success": True,
        "data": {
            "eps": {},
            "revenue": {},
            "income_statement": {},
            "balance_sheet": {},
            "sources": []
        }
    }
    
    for financial_type in financial_types:
        print(f"\n--- 測試 {financial_type['name']} ---")
        print(f"URL: {financial_type['url']}")
        
        try:
            response = requests.get(financial_type["url"], headers=headers, timeout=10)
            print(f"狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 檢查頁面內容
                page_title = soup.find('title')
                if page_title:
                    print(f"頁面標題: {page_title.get_text()}")
                
                # 尋找表格
                tables = soup.find_all('table')
                print(f"找到 {len(tables)} 個表格")
                
                # 檢查是否有財務數據相關的元素
                financial_keywords = ['每股盈餘', '營業收入', '營收', 'EPS', '營收表', '損益表', '資產負債表']
                found_keywords = []
                
                for keyword in financial_keywords:
                    if keyword in response.text:
                        found_keywords.append(keyword)
                
                print(f"找到的財務關鍵字: {found_keywords}")
                
                # 嘗試提取表格數據
                from langgraph_app.main import extract_table_data
                table_data = extract_table_data(soup, financial_type["type"])
                
                if table_data:
                    print(f"✅ 成功提取 {financial_type['name']} 數據")
                    print(f"數據: {json.dumps(table_data, ensure_ascii=False, indent=2)}")
                    financial_data["data"][financial_type["type"]] = table_data
                    financial_data["data"]["sources"].append({
                        "name": financial_type["name"],
                        "url": financial_type["url"]
                    })
                else:
                    print(f"❌ 無法提取 {financial_type['name']} 數據")
                    
                    # 檢查頁面結構
                    print("檢查頁面結構...")
                    main_content = soup.find('main') or soup.find('div', class_='main') or soup.find('body')
                    if main_content:
                        text_sample = main_content.get_text()[:500]
                        print(f"頁面內容樣本: {text_sample}")
                
            else:
                print(f"❌ HTTP 請求失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 爬取 {financial_type['name']} 失敗: {str(e)}")
            continue
    
    # 檢查最終結果
    print(f"\n=== 最終結果 ===")
    success_count = sum(1 for key in ["eps", "revenue", "income_statement", "balance_sheet"] 
                       if financial_data["data"][key])
    
    print(f"成功爬取的數據類型: {success_count}/4")
    
    if success_count == 0:
        print("❌ 沒有成功爬取到任何財務數據，將使用模擬數據")
        # 使用模擬數據
        financial_data["data"] = {
            "eps": {
                "2025_Q1": {"eps": "0.62", "quarterly_growth": "-8.82%", "yearly_growth": "-26.19%", "avg_price": "42.86"},
                "2024_Q4": {"eps": "0.68", "quarterly_growth": "-41.38%", "yearly_growth": "-36.45%", "avg_price": "51.00"},
                "2024_Q3": {"eps": "1.16", "quarterly_growth": "4.50%", "yearly_growth": "-10.08%", "avg_price": "52.58"}
            },
            "revenue": {
                "2025_Q1": {"revenue": "57,858,957", "quarterly_growth": "-4.18%", "yearly_growth": "5.91%"},
                "2024_Q4": {"revenue": "60,386,110", "quarterly_growth": "-0.16%", "yearly_growth": "9.87%"},
                "2024_Q3": {"revenue": "60,485,085", "quarterly_growth": "6.49%", "yearly_growth": "5.99%"}
            },
            "income_statement": {
                "revenue": {"2025_Q1": "57,858,957", "2024_Q4": "60,386,110", "2024_Q3": "60,485,085"},
                "gross_profit": {"2025_Q1": "15,446,645", "2024_Q4": "18,342,581", "2024_Q3": "20,428,845"},
                "operating_income": {"2025_Q1": "9,785,901", "2024_Q4": "11,957,004", "2024_Q3": "14,099,633"},
                "net_income": {"2025_Q1": "7,743,239", "2024_Q4": "8,459,689", "2024_Q3": "14,441,758"}
            },
            "balance_sheet": {
                "total_assets": {"2024_Q4": "1,234,567,890", "2024_Q3": "1,200,000,000"},
                "total_liabilities": {"2024_Q4": "567,890,123", "2024_Q3": "550,000,000"},
                "equity": {"2024_Q4": "666,677,767", "2024_Q3": "650,000,000"}
            },
            "sources": [
                {"name": "每股盈餘", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/eps"},
                {"name": "營收表", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/revenue"},
                {"name": "損益表", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/income-statement"},
                {"name": "資產負債表", "url": f"https://tw.stock.yahoo.com/quote/{stock_id}.TW/balance-sheet"}
            ]
        }
    else:
        print("✅ 成功爬取到財務數據")
    
    print(f"\n最終財務數據結構:")
    print(json.dumps(financial_data, ensure_ascii=False, indent=2))
    
    return financial_data

if __name__ == "__main__":
    test_yahoo_finance_crawler() 