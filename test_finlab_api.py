#!/usr/bin/env python3
"""
測試 FinLab API - 先取得一個表格並印出行和列的資訊
"""

import finlab
from finlab import data
import pandas as pd
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

def test_finlab_api():
    """測試 FinLab API - 印出表格結構"""
    
    # 登入 FinLab API
    api_key = os.environ['FINLAB_API_KEY']
    finlab.login(api_token=api_key)
    
    print("=== 測試 FinLab API 表格結構 ===")
    
    # 測試一個已知存在的資料類型
    data_type = "fundamental_features:營業利益"
    
    try:
        print(f"取得資料: {data_type}")
        df = data.get(data_type)
        
        print(f"\n=== 表格資訊 ===")
        print(f"Shape: {df.shape}")
        print(f"Columns (前10個): {list(df.columns[:10])}")
        print(f"Index (前10個): {list(df.index[:10])}")
        
        print(f"\n=== 前5行前5列資料 ===")
        print(df.head())
        
        # 檢查特定股票
        stock_id = "2303"
        if stock_id in df.columns:
            print(f"\n=== 股票 {stock_id} 的資料 ===")
            print(df[stock_id].dropna().tail(5))
        
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    test_finlab_api() 