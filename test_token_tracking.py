#!/usr/bin/env python3
"""
Token 追蹤器測試腳本
示範如何記錄和分析 OpenAI API 的 token 使用量
"""

import os
import sys
from datetime import datetime, timedelta

# 添加專案路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.token_tracker import TokenTracker, track_openai_call
from langgraph_app.nodes.classify_and_extract import classify_and_extract

def test_token_tracking():
    """測試 token 追蹤功能"""
    print("🧪 開始測試 Token 追蹤器...")
    
    # 創建測試用的追蹤器
    tracker = TokenTracker("test_token_usage.json")
    
    # 測試 1: 模擬 API 調用記錄
    print("\n📝 測試 1: 模擬 API 調用記錄")
    tracker.record_api_call(
        node_name="classify_and_extract",
        model="gpt-3.5-turbo",
        prompt_tokens=150,
        completion_tokens=50,
        total_tokens=200,
        cost=0.0004,
        user_input="台積電怎麼樣？",
        stock_id="2330"
    )
    
    tracker.record_api_call(
        node_name="summarize_results",
        model="gpt-3.5-turbo",
        prompt_tokens=300,
        completion_tokens=200,
        total_tokens=500,
        cost=0.0010,
        user_input="台積電財報分析",
        stock_id="2330"
    )
    
    # 測試 2: 取得使用摘要
    print("\n📊 測試 2: 取得使用摘要")
    summary = tracker.get_usage_summary()
    print("整體摘要:")
    print(f"  總調用次數: {summary['total_calls']}")
    print(f"  總輸入 tokens: {summary['total_prompt_tokens']:,}")
    print(f"  總輸出 tokens: {summary['total_completion_tokens']:,}")
    print(f"  總 tokens: {summary['total_tokens']:,}")
    print(f"  總成本: ${summary['total_cost']:.4f}")
    print(f"  成功率: {summary['success_rate']:.1%}")
    
    print("\n節點細分:")
    for node, stats in summary['node_breakdown'].items():
        print(f"  {node}:")
        print(f"    調用次數: {stats['calls']}")
        print(f"    總 tokens: {stats['total_tokens']:,}")
        print(f"    成本: ${stats['cost']:.4f}")
    
    # 測試 3: 成本計算
    print("\n💰 測試 3: 成本計算")
    models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    token_counts = [100, 500, 1000, 2000]
    
    for model in models:
        print(f"\n{model} 成本:")
        for tokens in token_counts:
            cost = tracker.calculate_cost(model, tokens, tokens)
            print(f"  {tokens:,} tokens: ${cost:.4f}")
    
    # 測試 4: 實際 API 調用追蹤
    print("\n🔍 測試 4: 實際 API 調用追蹤")
    try:
        # 確保有 API key
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️ 未設定 OPENAI_API_KEY，跳過實際 API 測試")
        else:
            print("執行實際 API 調用測試...")
            result = classify_and_extract("台積電最近怎麼樣？")
            print(f"分類結果: {result.get('category', 'N/A')}")
    except Exception as e:
        print(f"❌ 實際 API 測試失敗: {e}")
    
    # 測試 5: 匯出報告
    print("\n📄 測試 5: 匯出報告")
    report_file = tracker.export_report()
    print(f"報告已匯出至: {report_file}")
    
    print("\n✅ Token 追蹤器測試完成！")

def test_daily_monthly_usage():
    """測試每日/每月使用量統計"""
    print("\n📅 測試每日/每月使用量統計")
    
    tracker = TokenTracker("test_token_usage.json")
    
    # 模擬多天的使用記錄
    today = datetime.now()
    for i in range(7):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # 模擬當天的使用記錄
        tracker.record_api_call(
            node_name="classify_and_extract",
            model="gpt-3.5-turbo",
            prompt_tokens=100 + i * 10,
            completion_tokens=50 + i * 5,
            total_tokens=150 + i * 15,
            cost=0.0003 + i * 0.0001,
            user_input=f"測試問題 {i}",
            stock_id="2330"
        )
    
    # 取得今天的使用量
    today_str = today.strftime("%Y-%m-%d")
    daily_usage = tracker.get_daily_usage(today_str)
    print(f"今日使用量 ({today_str}):")
    print(f"  調用次數: {daily_usage['total_calls']}")
    print(f"  總成本: ${daily_usage['total_cost']:.4f}")
    
    # 取得本月使用量
    current_month = today.month
    current_year = today.year
    monthly_usage = tracker.get_monthly_usage(current_year, current_month)
    print(f"\n本月使用量 ({current_year}-{current_month:02d}):")
    print(f"  調用次數: {monthly_usage['total_calls']}")
    print(f"  總成本: ${monthly_usage['total_cost']:.4f}")

def show_cost_comparison():
    """顯示不同模型和 token 數量的成本比較"""
    print("\n💡 成本比較表")
    
    tracker = TokenTracker()
    
    # 常見的 token 使用量
    token_scenarios = [
        ("短問題", 100, 50),
        ("中等問題", 300, 200),
        ("長問題", 800, 500),
        ("複雜分析", 1500, 1000),
        ("深度報告", 3000, 2000)
    ]
    
    models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    
    print(f"{'場景':<12} {'輸入':<6} {'輸出':<6} {'總計':<6}", end="")
    for model in models:
        print(f" {model:<15}", end="")
    print()
    
    print("-" * 80)
    
    for scenario, prompt_tokens, completion_tokens in token_scenarios:
        total_tokens = prompt_tokens + completion_tokens
        print(f"{scenario:<12} {prompt_tokens:<6} {completion_tokens:<6} {total_tokens:<6}", end="")
        
        for model in models:
            cost = tracker.calculate_cost(model, prompt_tokens, completion_tokens)
            print(f" ${cost:<14.4f}", end="")
        print()

if __name__ == "__main__":
    print("🚀 Token 追蹤器完整測試")
    print("=" * 50)
    
    # 執行所有測試
    test_token_tracking()
    test_daily_monthly_usage()
    show_cost_comparison()
    
    print("\n" + "=" * 50)
    print("🎉 所有測試完成！")
    print("\n📋 使用建議:")
    print("1. 在每個 OpenAI API 調用後使用 track_openai_call() 函數")
    print("2. 定期檢查 token_usage.json 檔案了解使用情況")
    print("3. 使用 get_usage_summary() 進行成本分析")
    print("4. 設定預算警報避免超支") 