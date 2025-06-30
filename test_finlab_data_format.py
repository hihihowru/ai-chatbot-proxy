#!/usr/bin/env python3
"""
測試 FinLab API 的資料格式
"""

import sys
import os
import json
import requests

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.data_tools.database_query import db_query

def test_finlab_api_format():
    """測試 FinLab API 的資料格式"""
    print("=== 測試 FinLab API 資料格式 ===")
    
    # 測試不同的 table_id
    test_table_ids = [
        "105567992",  # 新聞
        "105567993",  # 籌碼
        "105567994",  # 基本面
        "105567995",  # 技術比較
        "105567996",  # 籌碼比較
        "105567997",  # 基本面比較
        "105567998",  # 大盤技術
        "105567999",  # 大盤籌碼
        "105568000",  # 產業技術
        "105568001",  # 產業籌碼
    ]
    
    stock_id = "2330"  # 台積電
    
    for table_id in test_table_ids:
        print(f"\n--- 測試 table_id: {table_id} ---")
        
        try:
            result = db_query.test_table_id(table_id, stock_id)
            
            print(f"狀態: {result.get('status', 'N/A')}")
            print(f"有資料: {result.get('has_data', 'N/A')}")
            print(f"資料數量: {result.get('data_count', 'N/A')}")
            print(f"標題: {result.get('title', 'N/A')}")
            
            if result.get('status') == 'success' and result.get('has_data'):
                # 嘗試獲取實際資料
                query_result = db_query.query_by_table_id(table_id, [stock_id])
                
                if query_result.get('success'):
                    data = query_result.get('data', {})
                    print(f"資料結構: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                    
                    # 檢查 Data 欄位
                    if 'Data' in data and data['Data']:
                        first_row = data['Data'][0]
                        print(f"第一行資料欄位: {list(first_row.keys()) if isinstance(first_row, dict) else 'N/A'}")
                        print(f"第一行資料範例: {first_row}")
                        
                        # 檢查是否有財務相關欄位
                        financial_fields = ['每股純益', '營收', '營業利益', 'EPS', 'Revenue', 'Operating Income']
                        found_fields = []
                        for field in financial_fields:
                            if field in first_row:
                                found_fields.append(field)
                        
                        if found_fields:
                            print(f"找到財務欄位: {found_fields}")
                        else:
                            print("未找到財務相關欄位")
                else:
                    print(f"查詢失敗: {query_result.get('error', 'N/A')}")
            
        except Exception as e:
            print(f"測試失敗: {e}")

def test_financial_data_processing():
    """測試財務資料處理邏輯"""
    print("\n=== 測試財務資料處理邏輯 ===")
    
    # 模擬 FinLab API 的資料格式
    test_data_formats = [
        {
            "name": "格式1: 標準格式",
            "data": {
                "quarterly": {
                    "2024Q1": {"每股純益": 1.2, "營收": 100000, "營業利益": 15000},
                    "2024Q2": {"每股純益": 1.5, "營收": 120000, "營業利益": 18000},
                    "2023Q1": {"每股純益": 1.0, "營收": 90000, "營業利益": 12000},
                    "2023Q2": {"每股純益": 1.3, "營收": 110000, "營業利益": 15000},
                }
            }
        },
        {
            "name": "格式2: 不同欄位名稱",
            "data": {
                "quarterly": {
                    "2024Q1": {"EPS": 1.2, "Revenue": 100000, "Operating Income": 15000},
                    "2024Q2": {"EPS": 1.5, "Revenue": 120000, "Operating Income": 18000},
                }
            }
        },
        {
            "name": "格式3: 空資料",
            "data": {}
        }
    ]
    
    for test_case in test_data_formats:
        print(f"\n--- {test_case['name']} ---")
        
        try:
            # 模擬 generate_financial_section 的處理邏輯
            financial_data = test_case['data']
            quarterly = financial_data.get('quarterly', {}) if financial_data else {}
            
            print(f"quarterly 資料: {quarterly}")
            
            if quarterly:
                # 取得所有年度與季度
                all_quarters = sorted(quarterly.keys(), reverse=True)
                print(f"所有季度: {all_quarters}")
                
                # 依年度分組
                year_quarters = {}
                for q in all_quarters:
                    year = q[:4]
                    if year not in year_quarters:
                        year_quarters[year] = []
                    year_quarters[year].append(q)
                
                print(f"年度分組: {year_quarters}")
                
                # 產生 EPS 表格
                eps_table = []
                for y in sorted(year_quarters.keys(), reverse=True)[:4]:
                    row = {"年度": y}
                    for i, q in enumerate(sorted(year_quarters[y])):
                        # 嘗試不同的欄位名稱
                        val = quarterly[q].get("每股純益") or quarterly[q].get("EPS", "N/A")
                        row[f"Q{i+1}"] = val
                    eps_table.append(row)
                
                print(f"EPS 表格: {eps_table}")
                
                # 測試成長率計算
                if len(eps_table) > 1:
                    for i in range(1, len(eps_table)):
                        for q in ["Q1", "Q2", "Q3", "Q4"]:
                            try:
                                prev = float(eps_table[i][q])
                                curr = float(eps_table[i-1][q])
                                growth = (curr - prev) / abs(prev) * 100 if prev != 0 else 0
                                color = "red" if growth > 0 else "green" if growth < 0 else "gray"
                                eps_table[i][f"{q}_成長率"] = {"value": f"{growth:.1f}%", "color": color}
                                print(f"成長率計算: {q} = {growth:.1f}% ({color})")
                            except Exception as e:
                                eps_table[i][f"{q}_成長率"] = {"value": "N/A", "color": "gray"}
                                print(f"成長率計算失敗: {e}")
            else:
                print("沒有 quarterly 資料")
                
        except Exception as e:
            print(f"處理失敗: {e}")

if __name__ == "__main__":
    test_finlab_api_format()
    test_financial_data_processing() 