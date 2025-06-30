#!/usr/bin/env python3
"""
測試 FinLab 整合後的財務資料函數
"""

import sys
import os

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.main import fetch_yahoo_financial_data

def test_finlab_integration():
    """測試 FinLab 整合"""
    
    print("=== 測試 FinLab 整合 ===")
    
    # 測試聯電
    stock_id = "2303"
    company_name = "聯電"
    
    print(f"測試股票: {stock_id} ({company_name})")
    
    try:
        result = fetch_yahoo_financial_data(stock_id, company_name)
        
        print(f"\n=== 結果 ===")
        print(f"EPS 資料: {result.get('eps', {})}")
        print(f"營收資料: {result.get('revenue', {})}")
        print(f"損益表: {result.get('income_statement', {})}")
        print(f"資產負債表: {result.get('balance_sheet', {})}")
        print(f"資料來源: {result.get('sources', [])}")
        
    except Exception as e:
        print(f"測試失敗: {e}")

if __name__ == "__main__":
    test_finlab_integration() 