#!/usr/bin/env python3
"""
簡單測試 FinLab API 資料結構
"""

import sys
import os
import json
import pandas as pd

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.data_tools.database_query import db_query

def test_finlab_data():
    """簡單測試 FinLab API 資料"""
    print("=== 簡單測試 FinLab API 資料 ===")
    
    # 測試基本面 table_id
    table_id = "778132"  # 基本面分析
    stock_id = "2330"    # 台積電
    
    print(f"測試 table_id: {table_id}, stock_id: {stock_id}")
    
    try:
        # 查詢資料
        result = db_query.query_by_table_id(table_id, [stock_id])
        
        if result.get('success'):
            data = result.get('data', {})
            print(f"資料結構: {list(data.keys())}")
            
            # 檢查 Data 欄位
            if 'Data' in data:
                print(f"Data 欄位類型: {type(data['Data'])}")
                print(f"Data 長度: {len(data['Data'])}")
                
                if data['Data']:
                    print(f"第一筆資料: {data['Data'][0]}")
                    
                    # 如果是 DataFrame，顯示欄位和索引
                    if isinstance(data['Data'], pd.DataFrame):
                        print(f"DataFrame 欄位: {data['Data'].columns.tolist()}")
                        print(f"DataFrame 索引: {data['Data'].index.tolist()}")
                        print(f"DataFrame 形狀: {data['Data'].shape}")
                    else:
                        print(f"第一筆資料欄位: {list(data['Data'][0].keys()) if isinstance(data['Data'][0], dict) else 'N/A'}")
            
            # 檢查 Title 欄位
            if 'Title' in data:
                print(f"Title 欄位: {data['Title']}")
                
        else:
            print(f"查詢失敗: {result.get('error')}")
            
    except Exception as e:
        print(f"測試失敗: {e}")

def test_financial_data_get():
    """測試財務資料的 data.get() 方法"""
    print("\n=== 測試財務資料 data.get() ===")
    
    # 模擬 FinLab API 回傳的資料結構
    mock_data = {
        "Data": [
            {"年度": "2025", "Q1": 1.2, "Q2": 1.5, "Q3": 1.8, "Q4": 2.0},
            {"年度": "2024", "Q1": 1.0, "Q2": 1.3, "Q3": 1.6, "Q4": 1.9},
            {"年度": "2023", "Q1": 0.8, "Q2": 1.1, "Q3": 1.4, "Q4": 1.7},
            {"年度": "2022", "Q1": 0.6, "Q2": 0.9, "Q3": 1.2, "Q4": 1.5},
        ],
        "Title": ["年度", "Q1", "Q2", "Q3", "Q4"]
    }
    
    print("模擬資料結構:")
    print(f"Data 欄位: {list(mock_data.get('Data', [])[0].keys()) if mock_data.get('Data') else 'N/A'}")
    print(f"Title 欄位: {mock_data.get('Title', [])}")
    
    # 測試 data.get() 方法
    data = mock_data.get('Data', [])
    title = mock_data.get('Title', [])
    
    print(f"\n使用 data.get() 結果:")
    print(f"data.get('Data'): {len(data)} 筆資料")
    print(f"data.get('Title'): {title}")
    
    if data:
        print(f"第一筆資料: {data[0]}")
        print(f"第一筆資料欄位: {list(data[0].keys())}")

if __name__ == "__main__":
    test_finlab_data()
    test_financial_data_get() 