#!/usr/bin/env python3
"""
搜尋 FinLab 中包含"毛利"相關的表格名稱
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def search_gross_profit_tables():
    """搜尋毛利相關的表格"""
    try:
        import finlab
        from finlab import data
        import pandas as pd
        
        # 登入 FinLab API
        api_token = 'AOl10aUjuRAwxdHjbO25jGoH7c8LOhXqKz/HgT9WlcCPkBwL8Qp6PDlqpd59YuR7#vip_m'
        finlab.login(api_token=api_token)
        
        print("=== 搜尋毛利相關表格 ===")
        
        # 可能的表格名稱模式
        possible_patterns = [
            "fundamental_features:毛利",
            "financial_statement:毛利",
            "fundamental_features:毛利率",
            "financial_statement:毛利率",
            "fundamental_features:毛利成長",
            "financial_statement:毛利成長",
            "fundamental_features:毛利成長率",
            "financial_statement:毛利成長率",
            "fundamental_features:營業毛利",
            "financial_statement:營業毛利",
            "fundamental_features:營業毛利率",
            "financial_statement:營業毛利率"
        ]
        
        for pattern in possible_patterns:
            print(f"\n--- 測試 {pattern} ---")
            try:
                df = data.get(pattern)
                print(f"✅ 成功取得表格: {pattern}")
                print(f"   Shape: {df.shape}")
                print(f"   Columns: {list(df.columns)[:5]}...")
                if "2330" in df.columns:
                    series = df["2330"].dropna()
                    print(f"   2330 資料筆數: {len(series)}")
                    print(f"   最新 3 筆: {series.tail(3).tolist()}")
                else:
                    print("   2330 不在欄位中")
            except Exception as e:
                print(f"❌ 失敗: {e}")
        
        print("\n=== 搜尋完成 ===")
        
    except Exception as e:
        print(f"搜尋失敗: {e}")

if __name__ == "__main__":
    search_gross_profit_tables() 