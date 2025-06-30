#!/usr/bin/env python3
"""
測試財務資料處理修正
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_financial_data_processing():
    """測試財務資料處理"""
    try:
        from langgraph_app.nodes.generate_section_financial import generate_financial_section
        
        # 模擬 financial_data（fallback 格式）
        financial_data = {
            "eps": {},
            "revenue": {},
            "income_statement": {
                # 2022 年
                "2022Q1": {"每股盈餘": 1.2, "營收": 38000000000, "營業利益": 4800000000},
                "2022Q2": {"每股盈餘": 1.3, "營收": 40000000000, "營業利益": 5000000000},
                "2022Q3": {"每股盈餘": 1.4, "營收": 42000000000, "營業利益": 5200000000},
                "2022Q4": {"每股盈餘": 1.5, "營收": 44000000000, "營業利益": 5400000000},
                # 2023 年
                "2023Q1": {"每股盈餘": 1.6, "營收": 46000000000, "營業利益": 5600000000},
                "2023Q2": {"每股盈餘": 1.7, "營收": 48000000000, "營業利益": 5800000000},
                "2023Q3": {"每股盈餘": 1.8, "營收": 50000000000, "營業利益": 6000000000},
                "2023Q4": {"每股盈餘": 1.9, "營收": 52000000000, "營業利益": 6200000000},
                # 2024 年
                "2024Q1": {"每股盈餘": 2.0, "營收": 54000000000, "營業利益": 6400000000},
                "2024Q2": {"每股盈餘": 2.1, "營收": 56000000000, "營業利益": 6600000000},
                "2024Q3": {"每股盈餘": 2.2, "營收": 58000000000, "營業利益": 6800000000},
                "2024Q4": {"每股盈餘": 2.3, "營收": 60000000000, "營業利益": 7000000000},
                # 2025 年
                "2025Q1": {"每股盈餘": 2.4, "營收": 62000000000, "營業利益": 7200000000},
                "2025Q2": {"每股盈餘": 2.5, "營收": 64000000000, "營業利益": 7400000000},
                "2025Q3": {"每股盈餘": 2.6, "營收": 66000000000, "營業利益": 7600000000},
                "2025Q4": {"每股盈餘": 2.7, "營收": 68000000000, "營業利益": 7800000000}
            },
            "balance_sheet": {},
            "sources": [{"name": "模擬資料", "url": "fallback"}]
        }
        
        test_news = """
        1. 聯電(2303)法說會重點整理：EPS創19季低、估第二季毛利回升，毛利率下滑至26.7%，跌破3成，創下近年低點。
        2. 營業利益率為16.9%，稅後純益77.8億元，每股盈餘0.62元，創下自2020年第二季以來的19季新低紀錄。
        """
        
        print("=== 測試財務資料處理 ===")
        print(f"Financial data keys: {list(financial_data.keys())}")
        print(f"Income statement keys: {list(financial_data['income_statement'].keys())}")
        print(f"First quarter data: {financial_data['income_statement']['2024Q1']}")
        
        result = generate_financial_section("聯電", "2303", financial_data, test_news)
        
        if result.get("success"):
            print("✅ 財務資料處理成功！")
            print(f"Section: {result['section']['section']}")
            print(f"Tabs count: {len(result['section']['tabs'])}")
            for tab in result['section']['tabs']:
                print(f"  - {tab['tab']}: {len(tab['table'])} rows")
            
            # 詳細檢查圖表格式
            print("\n=== 圖表格式詳細檢查 ===")
            for tab in result['section']['tabs']:
                print(f"\n📊 {tab['tab']} Tab:")
                print(f"  內容: {tab['content']}")
                print(f"  行數: {len(tab['table'])}")
                
                # 檢查每一行的結構
                for i, row in enumerate(tab['table']):
                    print(f"  第{i+1}行: {row}")
                    
                    # 檢查是否有年度欄位
                    if '年度' in row:
                        year = row['年度']
                        print(f"    年度: {year}")
                        
                        # 檢查是否有 Q1-Q4 欄位
                        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
                        for q in quarters:
                            if q in row:
                                value = row[q]
                                print(f"    {q}: {value}")
                            else:
                                print(f"    {q}: 缺失")
                        
                        # 檢查成長率欄位
                        growth_quarters = ['Q1_成長率', 'Q2_成長率', 'Q3_成長率', 'Q4_成長率']
                        for gq in growth_quarters:
                            if gq in row:
                                growth = row[gq]
                                print(f"    {gq}: {growth}")
                            else:
                                print(f"    {gq}: 缺失")
                    else:
                        print(f"    警告: 缺少年度欄位")
            
            # 輸出 insight 內容檢查格式
            print("\n=== Insight 內容檢查 ===")
            for tab in result['section']['tabs']:
                if tab['tab'] == '營收':
                    print(f"營收 Tab 內容: {tab['content']}")
                    print(f"營收 Tab 表格前兩行: {tab['table'][:2]}")
                    break
        else:
            print(f"❌ 財務資料處理失敗: {result.get('error')}")
        
        print("=== 測試完成 ===")
        
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_financial_data_processing() 