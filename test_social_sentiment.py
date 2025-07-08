#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
測試同學會輿情分析功能
"""

import sys
import os
import json

# 添加父目錄到 path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph_app.nodes.generate_section_social_sentiment import (
    crawl_cmoney_forum,
    analyze_sentiment,
    generate_social_sentiment_section
)

def test_crawl_cmoney_forum():
    """測試爬取同學會討論區功能"""
    print("=" * 50)
    print("🧪 測試爬取同學會討論區功能")
    print("=" * 50)
    
    test_stocks = ["2330", "2317", "2454"]  # 台積電、鴻海、聯發科
    
    for stock_id in test_stocks:
        print(f"\n📊 測試股票代號: {stock_id}")
        print("-" * 30)
        
        try:
            result = crawl_cmoney_forum(stock_id)
            
            if result.get("success"):
                posts = result.get("posts", [])
                print(f"✅ 爬取成功，共 {len(posts)} 個貼文")
                
                # 顯示前3個貼文
                for i, post in enumerate(posts[:3], 1):
                    print(f"  {i}. 標題: {post.get('title', '無標題')[:50]}...")
                    print(f"     內容: {post.get('content', '無內容')[:100]}...")
                    print(f"     時間: {post.get('time', '未知')}")
                    print(f"     留言數: {post.get('reply_count', 0)}")
                    print()
            else:
                print(f"❌ 爬取失敗: {result.get('error', '未知錯誤')}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")

def test_sentiment_analysis():
    """測試情緒分析功能"""
    print("=" * 50)
    print("🧪 測試情緒分析功能")
    print("=" * 50)
    
    test_texts = [
        "台積電今天表現很棒，看好未來發展！",
        "這支股票跌得很慘，建議避開",
        "台積電的財報怎麼樣？",
        "AI概念股大漲，台積電領軍上攻",
        "外資大賣台積電，股價重挫",
        "台積電基本面穩健，長期看好",
        "台積電今天開盤價多少？",
        "台積電法說會內容如何？"
    ]
    
    for text in test_texts:
        sentiment = analyze_sentiment(text)
        print(f"文本: {text}")
        print(f"情緒: {sentiment}")
        print("-" * 40)

def test_social_sentiment_section():
    """測試完整的輿情分析 section 生成"""
    print("=" * 50)
    print("🧪 測試完整的輿情分析 section 生成")
    print("=" * 50)
    
    test_cases = [
        {"company_name": "台積電", "stock_id": "2330"},
        {"company_name": "鴻海", "stock_id": "2317"},
        {"company_name": "聯發科", "stock_id": "2454"}
    ]
    
    for case in test_cases:
        company_name = case["company_name"]
        stock_id = case["stock_id"]
        
        print(f"\n📊 測試 {company_name}({stock_id})")
        print("-" * 40)
        
        try:
            result = generate_social_sentiment_section(company_name, stock_id)
            
            if result.get("success"):
                section = result.get("section", {})
                print(f"✅ 生成成功")
                print(f"Section 標題: {section.get('section', '無標題')}")
                print(f"卡片數量: {len(section.get('cards', []))}")
                
                # 顯示卡片內容
                for i, card in enumerate(section.get("cards", []), 1):
                    print(f"  卡片 {i}: {card.get('title', '無標題')}")
                    for j, content in enumerate(card.get("content", []), 1):
                        text = content.get("text", "")
                        print(f"    內容 {j}: {text[:100]}...")
                
                # 顯示調試資訊
                debug_info = result.get("debug_info", {})
                if debug_info:
                    print(f"  調試資訊:")
                    print(f"    總貼文數: {debug_info.get('total_posts', 0)}")
                    print(f"    總留言數: {debug_info.get('total_replies', 0)}")
                    print(f"    情緒分布: {debug_info.get('sentiment_counts', {})}")
                    print(f"    熱門貼文數: {debug_info.get('hot_posts_count', 0)}")
                
            else:
                print(f"❌ 生成失敗: {result.get('error', '未知錯誤')}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")

def test_integration_with_pipeline():
    """測試與報告生成流程的整合"""
    print("=" * 50)
    print("🧪 測試與報告生成流程的整合")
    print("=" * 50)
    
    try:
        from langgraph_app.nodes.generate_report_pipeline import generate_report_pipeline
        
        test_news = """
        1. 台積電今日股價上漲，外資買超，市場看好其AI發展前景。
        2. 台積電法說會釋出樂觀展望，預期下半年營收將有顯著成長。
        """
        
        test_sources = [
            {"title": "台積電股價上漲", "link": "https://tw.finance.yahoo.com/news/example1"},
            {"title": "台積電法說會", "link": "https://www.cmoney.tw/notes/example2"}
        ]
        
        print("📊 測試完整報告生成流程")
        print("-" * 40)
        
        result = generate_report_pipeline(
            company_name="台積電",
            stock_id="2330",
            intent="個股分析",
            news_summary=test_news,
            news_sources=test_sources
        )
        
        if result.get("success"):
            sections = result.get("sections", [])
            print(f"✅ 報告生成成功，共 {len(sections)} 個 section")
            
            # 檢查是否包含輿情分析 section
            sentiment_section = None
            for section in sections:
                if section.get("title") == "爆料同學會輿情分析":
                    sentiment_section = section
                    break
            
            if sentiment_section:
                print("✅ 成功包含爆料同學會輿情分析 section")
                print(f"  卡片數量: {len(sentiment_section.get('cards', []))}")
            else:
                print("❌ 未找到爆料同學會輿情分析 section")
            
            # 顯示所有 section 標題
            print("📋 所有 section 標題:")
            for i, section in enumerate(sections, 1):
                    print(f"  {i}. {section.get('title', '無標題')}")
                
        else:
            print(f"❌ 報告生成失敗: {result.get('error', '未知錯誤')}")
            
    except Exception as e:
        print(f"❌ 整合測試失敗: {e}")

def main():
    """主測試函數"""
    print("🚀 開始測試同學會輿情分析功能")
    print("=" * 60)
    
    # 1. 測試爬取功能
    test_crawl_cmoney_forum()
    
    # 2. 測試情緒分析
    test_sentiment_analysis()
    
    # 3. 測試 section 生成
    test_social_sentiment_section()
    
    # 4. 測試整合
    test_integration_with_pipeline()
    
    print("\n" + "=" * 60)
    print("🎉 測試完成")

if __name__ == "__main__":
    main() 