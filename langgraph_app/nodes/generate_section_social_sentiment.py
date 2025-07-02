import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from bs4 import BeautifulSoup
import openai
import time

def crawl_cmoney_forum(stock_id: str) -> Dict:
    """
    爬取 CMoney 同學會討論區的貼文
    
    Args:
        stock_id: 股票代號
    
    Returns:
        包含貼文列表的字典
    """
    try:
        print(f"[DEBUG] 🔍 開始爬取同學會討論區，股票代號: {stock_id}")
        
        # 構建 URL
        url = f"https://www.cmoney.tw/forum/stock/{stock_id}"
        
        # 設置 headers 模擬瀏覽器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        print(f"[DEBUG] 📡 發送請求到: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"[DEBUG] ❌ 請求失敗，狀態碼: {response.status_code}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "posts": []
            }
        
        print(f"[DEBUG] ✅ 請求成功，開始解析頁面")
        
        # 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尋找討論貼文
        posts = []
        
        # 嘗試多種可能的選擇器來找到貼文
        selectors = [
            '.article-item',  # 可能的文章項目選擇器
            '.post-item',     # 可能的貼文項目選擇器
            '.discussion-item', # 可能的討論項目選擇器
            'article',        # 文章標籤
            '.content-item',  # 內容項目
        ]
        
        found_posts = False
        for selector in selectors:
            post_elements = soup.select(selector)
            if post_elements:
                print(f"[DEBUG] 🔍 使用選擇器 '{selector}' 找到 {len(post_elements)} 個元素")
                found_posts = True
                
                for i, element in enumerate(post_elements[:20]):  # 限制前20個
                    try:
                        # 提取標題
                        title_element = element.select_one('h1, h2, h3, .title, .post-title')
                        title = title_element.get_text(strip=True) if title_element else f"貼文 {i+1}"
                        
                        # 提取內容摘要
                        content_element = element.select_one('.content, .post-content, .summary, p')
                        content = content_element.get_text(strip=True) if content_element else ""
                        
                        # 提取時間
                        time_element = element.select_one('.time, .date, .post-time, time')
                        post_time = time_element.get_text(strip=True) if time_element else "未知時間"
                        
                        # 提取留言數
                        reply_element = element.select_one('.reply-count, .comment-count, .count')
                        reply_count = reply_element.get_text(strip=True) if reply_element else "0"
                        
                        # 清理留言數
                        reply_count = re.sub(r'[^\d]', '', reply_count)
                        reply_count = int(reply_count) if reply_count.isdigit() else 0
                        
                        post = {
                            "title": title,
                            "content": content,
                            "time": post_time,
                            "reply_count": reply_count,
                            "sentiment": "neutral"  # 預設為中立
                        }
                        
                        posts.append(post)
                        print(f"[DEBUG] 📝 提取貼文 {i+1}: {title[:50]}... (留言數: {reply_count})")
                        
                    except Exception as e:
                        print(f"[DEBUG] ⚠️ 提取貼文 {i+1} 時發生錯誤: {e}")
                        continue
                
                break
        
        if not found_posts:
            print(f"[DEBUG] ⚠️ 未找到貼文，嘗試提取頁面文字內容")
            # 如果找不到特定結構，嘗試提取頁面中的文字內容
            text_content = soup.get_text()
            
            # 尋找可能的討論內容
            lines = text_content.split('\n')
            for line in lines:
                line = line.strip()
                if len(line) > 20 and any(keyword in line for keyword in ['討論', '分享', '分析', '看法', '建議']):
                    posts.append({
                        "title": "討論內容",
                        "content": line[:200] + "..." if len(line) > 200 else line,
                        "time": "未知時間",
                        "reply_count": 0,
                        "sentiment": "neutral"
                    })
        
        print(f"[DEBUG] 📊 總共提取到 {len(posts)} 個貼文")
        
        return {
            "success": True,
            "posts": posts,
            "total_count": len(posts)
        }
        
    except Exception as e:
        print(f"[DEBUG] ❌ 爬取同學會討論區失敗: {e}")
        return {
            "success": False,
            "error": str(e),
            "posts": []
        }

def analyze_sentiment(text: str) -> str:
    """
    分析文本情緒
    
    Args:
        text: 要分析的文本
    
    Returns:
        情緒標籤: positive, negative, neutral
    """
    try:
        # 正向關鍵詞
        positive_keywords = [
            '看漲', '利多', '加碼', 'AI', '營收創高', '成長', '看好', '強勢', '突破',
            '買進', '推薦', '機會', '樂觀', '上漲', '漲停', '好', '棒', '讚', '厲害',
            '賺錢', '獲利', '豐收', '成功', '優秀', '傑出', '亮眼', '驚艷'
        ]
        
        # 負向關鍵詞
        negative_keywords = [
            '看空', '跌', '爆量倒貨', '爛', '轉弱', '賣出', '避開', '風險', '下跌',
            '跌停', '壞', '糟', '差', '虧損', '賠錢', '失敗', '糟糕', '失望', '擔憂',
            '恐慌', '恐懼', '悲觀', '看衰', '不看好', '問題', '困難', '挑戰'
        ]
        
        text_lower = text.lower()
        
        # 計算正向和負向關鍵詞出現次數
        positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
        
        # 判斷情緒
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
            
    except Exception as e:
        print(f"[DEBUG] ⚠️ 情緒分析失敗: {e}")
        return "neutral"

def generate_social_sentiment_section(company_name: str, stock_id: str) -> Dict:
    """
    產生同學會輿情分析 section
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
    
    Returns:
        輿情分析 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 🎯 開始產生同學會輿情分析 section")
        print(f"[DEBUG] 公司名稱: {company_name}")
        print(f"[DEBUG] 股票代號: {stock_id}")
        
        # 1. 爬取同學會討論區
        crawl_result = crawl_cmoney_forum(stock_id)
        
        if not crawl_result.get("success"):
            print(f"[DEBUG] ❌ 爬取失敗，使用預設內容")
            return {
                "success": False,
                "section": {
                    "section": "社群輿情觀察",
                    "cards": [
                        {
                            "title": "社群討論熱度",
                            "content": [
                                {
                                    "text": f"目前 {company_name}({stock_id}) 在股市爆料同學會的討論熱度不高，暫無明確的社群輿情觀察。"
                                }
                            ]
                        }
                    ]
                },
                "error": crawl_result.get("error", "爬取失敗")
            }
        
        posts = crawl_result.get("posts", [])
        print(f"[DEBUG] 📊 成功爬取 {len(posts)} 個貼文")
        
        # 2. 分析情緒
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        analyzed_posts = []
        
        for post in posts:
            # 分析標題和內容的情緒
            title_sentiment = analyze_sentiment(post.get("title", ""))
            content_sentiment = analyze_sentiment(post.get("content", ""))
            
            # 綜合情緒判斷
            if title_sentiment == content_sentiment:
                final_sentiment = title_sentiment
            elif title_sentiment != "neutral" and content_sentiment == "neutral":
                final_sentiment = title_sentiment
            elif content_sentiment != "neutral" and title_sentiment == "neutral":
                final_sentiment = content_sentiment
            else:
                final_sentiment = "neutral"
            
            post["sentiment"] = final_sentiment
            sentiment_counts[final_sentiment] += 1
            analyzed_posts.append(post)
        
        print(f"[DEBUG] 📈 情緒分析結果: 正向 {sentiment_counts['positive']}, 負向 {sentiment_counts['negative']}, 中立 {sentiment_counts['neutral']}")
        
        # 3. 找出熱門討論
        sorted_posts = sorted(analyzed_posts, key=lambda x: x.get("reply_count", 0), reverse=True)
        hot_posts = sorted_posts[:3]  # 取前3個最熱門的
        
        # 4. 計算討論熱度
        total_posts = len(posts)
        total_replies = sum(post.get("reply_count", 0) for post in posts)
        
        # 5. 生成輿情摘要
        sentiment_summary = ""
        if total_posts > 0:
            positive_ratio = sentiment_counts["positive"] / total_posts
            negative_ratio = sentiment_counts["negative"] / total_posts
            neutral_ratio = sentiment_counts["neutral"] / total_posts
            
            if positive_ratio > 0.5:
                sentiment_summary = "社群對該股偏樂觀"
            elif negative_ratio > 0.5:
                sentiment_summary = "社群對該股偏保守"
            elif positive_ratio > negative_ratio:
                sentiment_summary = "社群對該股略偏樂觀"
            elif negative_ratio > positive_ratio:
                sentiment_summary = "社群對該股略偏保守"
            else:
                sentiment_summary = "社群對該股意見分歧"
        else:
            sentiment_summary = "社群討論熱度不高"
        
        # 6. 使用 LLM 生成最終報告
        hot_posts_text = ""
        for i, post in enumerate(hot_posts, 1):
            hot_posts_text += f"{i}. 標題: {post.get('title', '無標題')}\n"
            hot_posts_text += f"   內容: {post.get('content', '無內容')[:100]}...\n"
            hot_posts_text += f"   情緒: {post.get('sentiment', 'neutral')}\n"
            hot_posts_text += f"   留言數: {post.get('reply_count', 0)}\n\n"
        
        prompt = f"""
你是一位專業的投資分析師，請根據以下同學會討論區的資料，為 {company_name}({stock_id}) 生成社群輿情觀察報告。

討論統計：
- 總貼文數: {total_posts}
- 總留言數: {total_replies}
- 情緒分布: 正向 {sentiment_counts['positive']} 篇, 負向 {sentiment_counts['negative']} 篇, 中立 {sentiment_counts['neutral']} 篇

熱門討論：
{hot_posts_text}

請生成客觀、中立的輿情觀察報告，包含：
1. 討論熱度分析
2. 情緒分布分析
3. 熱門討論主題摘要
4. 社群觀察結論

請回傳 JSON 格式：
{{
  "section": "社群輿情觀察",
  "cards": [
    {{
      "title": "討論熱度分析",
      "content": [
        {{
          "text": "過去48小時內，{company_name}({stock_id})在股市爆料同學會共有{total_posts}篇相關討論，總留言數達{total_replies}則。"
        }},
        {{
          "text": "相比平均討論熱度，目前討論熱度{'偏高' if total_posts > 10 else '偏低'}。"
        }}
      ]
    }},
    {{
      "title": "情緒分布分析",
      "content": [
        {{
          "text": "社群情緒分布：正向 {sentiment_counts['positive']}篇({positive_ratio:.1%})、負向 {sentiment_counts['negative']}篇({negative_ratio:.1%})、中立 {sentiment_counts['neutral']}篇({neutral_ratio:.1%})。"
        }},
        {{
          "text": "整體而言，{sentiment_summary}。"
        }}
      ]
    }},
    {{
      "title": "熱門討論主題",
      "content": [
        {{
          "text": "最受關注的討論主題包括："
        }}
      ]
    }}
  ]
}}

請根據實際資料調整內容，保持客觀中立。
"""
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        raw_content = response.choices[0].message.content.strip()
        print(f"[DEBUG] 🤖 LLM 原始回傳內容：\n{raw_content}")
        
        # 解析 JSON
        try:
            result = json.loads(raw_content)
            
            # 添加熱門討論的詳細內容
            if result.get("cards") and len(result["cards"]) >= 3:
                hot_discussion_card = result["cards"][2]
                if hot_discussion_card.get("title") == "熱門討論主題":
                    for i, post in enumerate(hot_posts, 1):
                        hot_discussion_card["content"].append({
                            "text": f"**{i}. {post.get('title', '無標題')}**\n{post.get('content', '無內容')[:150]}...\n(留言數: {post.get('reply_count', 0)}, 情緒: {post.get('sentiment', 'neutral')})"
                        })
            
            print(f"[DEBUG] ✅ 同學會輿情分析產生成功")
            return {
                "success": True,
                "section": result,
                "debug_info": {
                    "total_posts": total_posts,
                    "total_replies": total_replies,
                    "sentiment_counts": sentiment_counts,
                    "hot_posts_count": len(hot_posts)
                }
            }
            
        except json.JSONDecodeError as e:
            print(f"[DEBUG] ❌ JSON 解析失敗: {e}")
            # 返回預設內容
            return {
                "success": False,
                "section": {
                    "section": "社群輿情觀察",
                    "cards": [
                        {
                            "title": "討論熱度分析",
                            "content": [
                                {
                                    "text": f"過去48小時內，{company_name}({stock_id})在股市爆料同學會共有{total_posts}篇相關討論。"
                                }
                            ]
                        },
                        {
                            "title": "情緒分布分析",
                            "content": [
                                {
                                    "text": f"社群情緒分布：正向 {sentiment_counts['positive']}篇、負向 {sentiment_counts['negative']}篇、中立 {sentiment_counts['neutral']}篇。"
                                },
                                {
                                    "text": f"整體而言，{sentiment_summary}。"
                                }
                            ]
                        }
                    ]
                },
                "error": f"JSON 解析失敗: {e}"
            }
        
    except Exception as e:
        print(f"[DEBUG] ❌ 同學會輿情分析失敗: {e}")
        return {
            "success": False,
            "section": {
                "section": "社群輿情觀察",
                "cards": [
                    {
                        "title": "社群討論熱度",
                        "content": [
                            {
                                "text": f"目前 {company_name}({stock_id}) 在股市爆料同學會的討論熱度不高，暫無明確的社群輿情觀察。"
                            }
                        ]
                    }
                ]
            },
            "error": str(e)
        }

# 測試用
if __name__ == "__main__":
    test_result = generate_social_sentiment_section("台積電", "2330")
    print(json.dumps(test_result, ensure_ascii=False, indent=2)) 