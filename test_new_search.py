#!/usr/bin/env python3
"""
測試新的搜尋功能 - 更新版本
"""

import json
from langgraph_app.nodes.search_news import (
    search_news, 
    generate_search_keywords, 
    generate_fallback_keywords,
    filter_results_by_site,
    extract_date_from_result,
    log_search_results,
    ALLOWED_SITES
)

def test_search_functionality():
    """測試搜尋功能"""
    print("🔍 測試新的搜尋功能 - 更新版本")
    print("=" * 60)
    
    # 測試參數
    company_name = "台積電"
    stock_id = "2330"
    intent = "個股分析"
    keywords = ["財報", "EPS"]
    
    print(f"📊 測試參數:")
    print(f"   公司名稱: {company_name}")
    print(f"   股票代號: {stock_id}")
    print(f"   問題類型: {intent}")
    print(f"   關鍵字: {keywords}")
    print()
    
    # 1. 測試關鍵字生成
    print("1️⃣ 測試關鍵字生成")
    print("-" * 40)
    
    try:
        generated_keywords = generate_search_keywords(company_name, stock_id, intent, keywords, "", "")
        print(f"✅ AI 生成關鍵字數量: {len(generated_keywords)}")
        print(f"📝 關鍵字列表:")
        for i, keyword in enumerate(generated_keywords, 1):
            print(f"   {i:2d}. {keyword}")
        print()
    except Exception as e:
        print(f"❌ AI 生成關鍵字失敗: {e}")
        print()
    
    # 2. 測試備用關鍵字生成
    print("2️⃣ 測試備用關鍵字生成")
    print("-" * 40)
    
    try:
        fallback_keywords = generate_fallback_keywords(company_name, stock_id, intent, keywords, "")
        print(f"✅ 備用關鍵字數量: {len(fallback_keywords)}")
        print(f"📝 備用關鍵字列表:")
        for i, keyword in enumerate(fallback_keywords, 1):
            print(f"   {i:2d}. {keyword}")
        print()
    except Exception as e:
        print(f"❌ 備用關鍵字生成失敗: {e}")
        print()
    
    # 3. 測試網站過濾功能
    print("3️⃣ 測試網站過濾功能")
    print("-" * 40)
    
    test_results = [
        {'title': '台積電新聞', 'link': 'https://tw.finance.yahoo.com/news/2330', 'snippet': 'test'},
        {'title': '其他新聞', 'link': 'https://example.com/news', 'snippet': 'test'},
        {'title': '鉅亨網新聞', 'link': 'https://cnyes.com/news/2330', 'snippet': 'test'},
        {'title': 'MoneyDJ新聞', 'link': 'https://moneydj.com/news/2330', 'snippet': 'test'}
    ]
    
    filtered_results = filter_results_by_site(test_results)
    print(f"✅ 原始結果數: {len(test_results)}")
    print(f"✅ 過濾後結果數: {len(filtered_results)}")
    print(f"📝 過濾結果:")
    for i, result in enumerate(filtered_results, 1):
        site_name = result.get("site_name", "未知")
        title = result.get("title", "無標題")
        print(f"   {i}. [{site_name}] {title}")
    print()
    
    # 4. 測試日期提取功能
    print("4️⃣ 測試日期提取功能")
    print("-" * 40)
    
    test_result = {
        'title': '台積電2025年1月15日財報分析',
        'snippet': '2025年第一季財報表現亮眼'
    }
    
    date_info = extract_date_from_result(test_result)
    print(f"✅ 測試標題: {test_result['title']}")
    print(f"✅ 提取日期: {date_info}")
    print()
    
    # 5. 測試完整搜尋流程
    print("5️⃣ 測試完整搜尋流程")
    print("-" * 40)
    
    try:
        search_result = search_news(company_name, stock_id, intent, keywords)
        
        if search_result.get("success"):
            results = search_result.get("results", [])
            print(f"✅ 搜尋成功!")
            print(f"📊 結果數量: {len(results)}")
            print(f"📝 前5個結果:")
            for i, result in enumerate(results[:5], 1):
                title = result.get("title", "無標題")
                site_name = result.get("site_name", "未知網站")
                date_info = extract_date_from_result(result)
                print(f"   {i}. [{site_name}] {title}")
                print(f"      日期: {date_info}")
        else:
            print(f"❌ 搜尋失敗: {search_result.get('error', '未知錯誤')}")
        print()
    except Exception as e:
        print(f"❌ 搜尋流程錯誤: {e}")
        print()
    
    # 6. 顯示允許的網站列表
    print("6️⃣ 允許的來源網站")
    print("-" * 40)
    print(f"📊 總共 {len(ALLOWED_SITES)} 個允許的網站:")
    for i, site in enumerate(ALLOWED_SITES, 1):
        print(f"   {i:2d}. {site}")
    print()
    
    # 7. 統計資訊
    print("7️⃣ 功能統計")
    print("-" * 40)
    print(f"✅ 允許網站數量: {len(ALLOWED_SITES)}")
    print(f"✅ 關鍵字生成數量: {len(generated_keywords) if 'generated_keywords' in locals() else 'N/A'}")
    print(f"✅ 備用關鍵字數量: {len(fallback_keywords) if 'fallback_keywords' in locals() else 'N/A'}")
    print(f"✅ 網站過濾成功率: {len(filtered_results)}/{len(test_results)} = {len(filtered_results)/len(test_results)*100:.1f}%")
    print()
    
    print("🎉 測試完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_search_functionality() 