#!/usr/bin/env python3
"""
測試分組搜尋功能
"""

import json
from langgraph_app.nodes.search_news import (
    search_news_smart,
    search_news_grouped,
    group_search_keywords,
    generate_search_keywords,
    ALLOWED_SITES
)

def test_grouped_search():
    """測試分組搜尋功能"""
    print("🔍 測試分組搜尋功能")
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
        all_keywords = generate_search_keywords(company_name, stock_id, intent, keywords, "", "")
        print(f"✅ 生成關鍵字數量: {len(all_keywords)}")
        print(f"📝 關鍵字列表:")
        for i, keyword in enumerate(all_keywords, 1):
            print(f"   {i:2d}. {keyword}")
        print()
    except Exception as e:
        print(f"❌ 關鍵字生成失敗: {e}")
        return
    
    # 2. 測試關鍵字分組
    print("2️⃣ 測試關鍵字分組")
    print("-" * 40)
    
    try:
        keyword_groups = group_search_keywords(all_keywords, group_count=4)
        print(f"✅ 分組數量: {len(keyword_groups)}")
        print(f"📝 分組結果:")
        for i, group in enumerate(keyword_groups, 1):
            print(f"   第{i}組 ({len(group)}個):")
            for j, keyword in enumerate(group, 1):
                print(f"     {j}. {keyword}")
            print()
    except Exception as e:
        print(f"❌ 關鍵字分組失敗: {e}")
        return
    
    # 3. 測試分組搜尋
    print("3️⃣ 測試分組搜尋")
    print("-" * 40)
    
    try:
        # 使用分組搜尋
        grouped_result = search_news_smart(
            company_name=company_name,
            stock_id=stock_id,
            intent=intent,
            keywords=keywords,
            use_grouped=True
        )
        
        if grouped_result.get("success"):
            results = grouped_result.get("results", [])
            total_groups = grouped_result.get("total_groups", 0)
            search_keywords = grouped_result.get("search_keywords", [])
            
            print(f"✅ 分組搜尋成功!")
            print(f"📊 分組數量: {total_groups}")
            print(f"📊 搜尋關鍵字數量: {len(search_keywords)}")
            print(f"📊 結果數量: {len(results)}")
            print(f"📝 前5個結果:")
            
            for i, result in enumerate(results[:5], 1):
                title = result.get("title", "無標題")
                site_name = result.get("site_name", "未知網站")
                link = result.get("link", "無連結")
                print(f"   {i}. [{site_name}] {title}")
                print(f"      連結: {link}")
        else:
            print(f"❌ 分組搜尋失敗: {grouped_result.get('error', '未知錯誤')}")
        print()
    except Exception as e:
        print(f"❌ 分組搜尋錯誤: {e}")
        print()
    
    # 4. 比較傳統搜尋和分組搜尋
    print("4️⃣ 比較搜尋方式")
    print("-" * 40)
    
    try:
        # 傳統搜尋
        traditional_result = search_news_smart(
            company_name=company_name,
            stock_id=stock_id,
            intent=intent,
            keywords=keywords,
            use_grouped=False
        )
        
        traditional_results = traditional_result.get("results", []) if traditional_result.get("success") else []
        grouped_results = grouped_result.get("results", []) if grouped_result.get("success") else []
        
        print(f"📊 搜尋結果比較:")
        print(f"   傳統搜尋: {len(traditional_results)} 個結果")
        print(f"   分組搜尋: {len(grouped_results)} 個結果")
        print(f"   差異: {len(grouped_results) - len(traditional_results)} 個結果")
        print()
        
        # 顯示網站分布
        print(f"📊 網站分布比較:")
        traditional_sites = {}
        grouped_sites = {}
        
        for result in traditional_results:
            site = result.get("site_name", "未知")
            traditional_sites[site] = traditional_sites.get(site, 0) + 1
        
        for result in grouped_results:
            site = result.get("site_name", "未知")
            grouped_sites[site] = grouped_sites.get(site, 0) + 1
        
        print(f"   傳統搜尋網站分布:")
        for site, count in traditional_sites.items():
            print(f"     {site}: {count} 個")
        
        print(f"   分組搜尋網站分布:")
        for site, count in grouped_sites.items():
            print(f"     {site}: {count} 個")
        print()
        
    except Exception as e:
        print(f"❌ 比較搜尋方式錯誤: {e}")
        print()
    
    # 5. 統計資訊
    print("5️⃣ 功能統計")
    print("-" * 40)
    print(f"✅ 允許網站數量: {len(ALLOWED_SITES)}")
    print(f"✅ 生成關鍵字數量: {len(all_keywords)}")
    print(f"✅ 分組數量: {len(keyword_groups)}")
    print(f"✅ 平均每組關鍵字: {len(all_keywords) // len(keyword_groups) if keyword_groups else 0}")
    print()
    
    print("🎉 分組搜尋測試完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_grouped_search() 