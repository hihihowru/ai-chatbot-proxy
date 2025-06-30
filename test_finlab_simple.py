#!/usr/bin/env python3
"""
簡化測試 - 只取需要的關鍵財務資料
"""

import finlab
from finlab import data
import pandas as pd

def test_simple_finlab():
    """簡化測試 - 只取關鍵資料"""
    
    # 登入 FinLab API
    api_token = 'AOl10aUjuRAwxdHjbO25jGoH7c8LOhXqKz/HgT9WlcCPkBwL8Qp6PDlqpd59YuR7#vip_m'
    finlab.login(api_token=api_token)
    
    print("=== 簡化測試 - 關鍵財務資料 ===")
    
    stock_id = "2303"
    
    # 只測試我們需要的資料類型
    needed_data = {
        "營業利益": "fundamental_features:營業利益",
        "營業利益率": "fundamental_features:營業利益率"
    }
    
    results = {}
    
    for name, data_type in needed_data.items():
        try:
            print(f"\n--- 取得 {name} ---")
            df = data.get(data_type)
            
            if stock_id in df.columns:
                recent_data = df[stock_id].dropna().tail(4)
                results[name] = recent_data
                print(f"✓ 成功取得 {len(recent_data)} 筆資料")
                print(recent_data)
            else:
                print(f"✗ 找不到股票 {stock_id}")
                
        except Exception as e:
            print(f"✗ 錯誤: {e}")
    
    print(f"\n=== 總結 ===")
    print(f"成功取得的資料: {list(results.keys())}")

if __name__ == "__main__":
    test_simple_finlab() 