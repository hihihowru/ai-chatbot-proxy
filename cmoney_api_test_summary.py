#!/usr/bin/env python3
"""
分析 CMoney API 測試結果並生成總結報告
"""

import json
import os
from typing import Dict, List, Any

def load_test_results():
    """載入測試結果"""
    with open("cmoney_table_results.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def load_successful_tables():
    """載入成功的 table ID 列表"""
    with open("successful_table_ids.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_results():
    """分析測試結果"""
    results = load_test_results()
    successful_tables = load_successful_tables()
    
    # 統計資訊
    total_tested = len(results)
    successful_count = len(successful_tables)
    failed_count = total_tested - successful_count
    
    # 按資料量分類
    data_categories = {
        "大量資料 (>1000筆)": [],
        "中量資料 (100-1000筆)": [],
        "少量資料 (10-100筆)": [],
        "微量資料 (<10筆)": [],
        "無資料": []
    }
    
    # 按標題分類
    title_categories = {}
    
    for table_id, result in results.items():
        if result["status"] == "success" and result["has_data"]:
            data_count = result["data_count"]
            title = " | ".join(result["title"])
            
            # 按資料量分類
            if data_count > 1000:
                data_categories["大量資料 (>1000筆)"].append(table_id)
            elif data_count > 100:
                data_categories["中量資料 (100-1000筆)"].append(table_id)
            elif data_count > 10:
                data_categories["少量資料 (10-100筆)"].append(table_id)
            elif data_count > 0:
                data_categories["微量資料 (<10筆)"].append(table_id)
            else:
                data_categories["無資料"].append(table_id)
            
            # 按標題分類
            if title not in title_categories:
                title_categories[title] = []
            title_categories[title].append(table_id)
    
    return {
        "summary": {
            "total_tested": total_tested,
            "successful": successful_count,
            "failed": failed_count,
            "success_rate": f"{(successful_count/total_tested*100):.1f}%"
        },
        "data_categories": data_categories,
        "title_categories": title_categories,
        "successful_tables": successful_tables,
        "all_results": results
    }

def generate_log_format():
    """生成 log 格式的結果"""
    analysis = analyze_results()
    
    log_data = {}
    
    # 將所有成功的 table ID 加入 log
    for table_id in analysis["successful_tables"]:
        result = analysis["all_results"][str(table_id)]
        log_data[table_id] = {
            "status": "success",
            "data_count": result["data_count"],
            "title": result["title"],
            "has_data": result["has_data"]
        }
    
    # 將失敗的 table ID 也加入 log
    for table_id, result in analysis["all_results"].items():
        if result["status"] != "success":
            log_data[table_id] = {
                "status": "failed",
                "error": result.get("error", "Unknown error")
            }
    
    return log_data

def print_summary():
    """印出詳細摘要"""
    analysis = analyze_results()
    
    print("="*80)
    print("📊 CMoney API 測試結果詳細分析")
    print("="*80)
    
    # 基本統計
    summary = analysis["summary"]
    print(f"總測試數: {summary['total_tested']}")
    print(f"成功數: {summary['successful']}")
    print(f"失敗數: {summary['failed']}")
    print(f"成功率: {summary['success_rate']}")
    
    print("\n" + "="*50)
    print("📈 按資料量分類")
    print("="*50)
    
    for category, tables in analysis["data_categories"].items():
        print(f"{category}: {len(tables)} 個")
        if len(tables) <= 10:
            print(f"  Table IDs: {', '.join(map(str, tables))}")
        else:
            print(f"  Table IDs: {', '.join(map(str, tables[:10]))} ... (還有 {len(tables)-10} 個)")
    
    print("\n" + "="*50)
    print("🏷️  按標題分類 (前10個)")
    print("="*50)
    
    sorted_titles = sorted(analysis["title_categories"].items(), key=lambda x: len(x[1]), reverse=True)
    
    for i, (title, tables) in enumerate(sorted_titles[:10], 1):
        print(f"{i:2d}. {title}")
        print(f"    數量: {len(tables)} 個")
        print(f"    Table IDs: {', '.join(map(str, tables[:5]))}{'...' if len(tables) > 5 else ''}")
        print()

def save_log_format():
    """儲存 log 格式的結果"""
    log_data = generate_log_format()
    
    with open("cmoney_api_log.json", 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print("💾 Log 格式結果已儲存到 cmoney_api_log.json")

def main():
    """主函數"""
    print("🔍 分析 CMoney API 測試結果...")
    
    # 檢查檔案是否存在
    if not os.path.exists("cmoney_table_results.json"):
        print("❌ 找不到 cmoney_table_results.json 檔案")
        return
    
    if not os.path.exists("successful_table_ids.json"):
        print("❌ 找不到 successful_table_ids.json 檔案")
        return
    
    # 印出詳細摘要
    print_summary()
    
    # 儲存 log 格式
    save_log_format()
    
    print("\n✅ 分析完成！")

if __name__ == "__main__":
    main() 