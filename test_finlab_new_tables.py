#!/usr/bin/env python3
"""
測試新的 FinLab 表格：每股盈餘、毛利成長率、月營收成長率
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_finlab_new_tables():
    """測試新的三個 FinLab 表格"""
    try:
        import finlab
        from finlab import data
        import pandas as pd
        
        # 登入 FinLab API
        api_key = os.environ['FINLAB_API_KEY']
        finlab.login(api_token=api_key)
        
        print("=== 測試新的 FinLab 表格 ===")
        
        # 測試股票代碼
        stock_id = "2330"  # 台積電
        
        # 新的三個表格
        finlab_data = {
            "每股盈餘": "financial_statement:每股盈餘",
            "營業毛利率": "fundamental_features:營業毛利率", 
            "月營收成長率": "monthly_revenue:去年同月增減(%)"
        }
        
        for name, data_type in finlab_data.items():
            print(f"\n--- 測試 {name} ({data_type}) ---")
            try:
                df = data.get(data_type)
                print(f"DataFrame shape: {df.shape}")
                print(f"DataFrame columns: {list(df.columns)[:5]}...")  # 只顯示前5個
                print(f"DataFrame index type: {type(df.index[0]) if len(df.index) > 0 else 'Empty'}")
                
                if stock_id in df.columns:
                    series = df[stock_id].dropna()
                    print(f"找到 {stock_id} 的資料，共 {len(series)} 筆")
                    print(f"最新 5 筆資料:")
                    print(series.tail(5))
                    
                    # 檢查 date index 格式
                    if name == "月營收成長率":
                        print(f"月營收成長率的 date index 範例:")
                        for i, date in enumerate(series.tail(3).index):
                            print(f"  {i+1}: {date} (type: {type(date)})")
                    else:
                        print(f"{name} 的 date index 範例:")
                        for i, date in enumerate(series.tail(3).index):
                            print(f"  {i+1}: {date} (type: {type(date)})")
                else:
                    print(f"找不到 {stock_id} 的資料")
                    
            except Exception as e:
                print(f"取得 {name} 資料失敗: {e}")
        
        print("\n=== 測試完成 ===")
        
    except Exception as e:
        print(f"測試失敗: {e}")

if __name__ == "__main__":
    test_finlab_new_tables() 