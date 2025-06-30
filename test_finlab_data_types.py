#!/usr/bin/env python3
"""
檢查 FinLab 可用的資料類型
"""

import finlab
from finlab import data
import pandas as pd

def check_available_data_types():
    """檢查可用的資料類型"""
    
    # 登入 FinLab API
    api_token = 'AOl10aUjuRAwxdHjbO25jGoH7c8LOhXqKz/HgT9WlcCPkBwL8Qp6PDlqpd59YuR7#vip_m'
    finlab.login(api_token=api_token)
    
    print("=== 檢查 FinLab 可用資料類型 ===")
    
    # 嘗試不同的資料類型名稱
    test_types = [
        "fundamental_features:每股盈餘",
        "fundamental_features:eps",
        "fundamental_features:EPS",
        "fundamental_features:每股盈餘(元)",
        "fundamental_features:營收",
        "fundamental_features:revenue",
        "fundamental_features:營收(千元)",
        "fundamental_features:每股淨值",
        "fundamental_features:book_value",
        "fundamental_features:每股淨值(元)",
        "fundamental_features:本益比",
        "fundamental_features:pe_ratio",
        "fundamental_features:股價淨值比",
        "fundamental_features:pb_ratio"
    ]
    
    stock_id = "2303"
    
    for data_type in test_types:
        try:
            print(f"\n--- 測試 {data_type} ---")
            df = data.get(data_type)
            
            if stock_id in df.columns:
                recent_data = df[stock_id].dropna().tail(3)
                print(f"✓ 成功 - 最近3筆資料:")
                print(recent_data)
            else:
                print(f"✗ 股票 {stock_id} 不在資料中")
                
        except Exception as e:
            print(f"✗ 錯誤: {e}")

if __name__ == "__main__":
    check_available_data_types() 