import json
from typing import List, Dict

def generate_sources_section(news_sources: List[Dict] = None, financial_sources: List[Dict] = None) -> Dict:
    """
    產生資料來源 section
    
    Args:
        news_sources: 新聞來源列表
        financial_sources: 財務資料來源列表
    
    Returns:
        資料來源 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 開始產生 section: 資料來源")
        print(f"[DEBUG] 新聞來源數量: {len(news_sources) if news_sources else 0}")
        print(f"[DEBUG] 財務來源數量: {len(financial_sources) if financial_sources else 0}")
        
        sources = []
        
        # 添加新聞來源
        if news_sources and isinstance(news_sources, list):
            for source in news_sources:
                if isinstance(source, dict):
                    title = source.get('title', '無標題')
                    link = source.get('link', '無連結')
                    # 提取網站名稱
                    site_name = extract_site_name(link)
                    # 使用物件格式，支援前端連結功能
                    sources.append({
                        "title": f"{title} - {site_name}",
                        "link": link
                    })
        
        # 添加財務資料來源
        if financial_sources and isinstance(financial_sources, list):
            for source in financial_sources:
                if isinstance(source, dict):
                    name = source.get('name', '未知來源')
                    url = source.get('url', '無連結')
                    sources.append({
                        "title": f"{name}",
                        "link": url
                    })
        
        # 如果沒有來源，添加預設來源
        if not sources:
            sources = [
                {
                    "title": "Yahoo奇摩股市",
                    "link": "https://tw.finance.yahoo.com/"
                },
                {
                    "title": "CMoney",
                    "link": "https://www.cmoney.tw/"
                },
                {
                    "title": "鉅亨網",
                    "link": "https://www.cnyes.com/"
                }
            ]
        
        # 限制來源數量，避免過多
        sources = sources[:10]  # 最多顯示10個來源
        
        sources_section = {
            "section": "資料來源",
            "sources": sources
        }
        
        print(f"[DEBUG] 解析後內容：{json.dumps(sources_section, ensure_ascii=False, indent=2)}")
        print(f"[DEBUG] 合併 section: 資料來源")
        
        return {
            "success": True,
            "section": sources_section,
            "raw_content": "直接整理來源資料，無需 LLM"
        }
        
    except Exception as e:
        print(f"[generate_sources_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "資料來源",
            "sources": [
                {
                    "title": "Yahoo奇摩股市",
                    "link": "https://tw.finance.yahoo.com/"
                },
                {
                    "title": "CMoney",
                    "link": "https://www.cmoney.tw/"
                },
                {
                    "title": "鉅亨網",
                    "link": "https://www.cnyes.com/"
                }
            ]
        }
        return {
            "success": False,
            "section": default_section,
            "error": str(e)
        }

def extract_site_name(url: str) -> str:
    """從 URL 中提取網站名稱"""
    if not url or url == '無連結':
        return '未知網站'
    
    try:
        # 簡單的網站名稱提取
        if 'yahoo.com' in url:
            return 'Yahoo奇摩股市'
        elif 'cmoney.tw' in url:
            return 'CMoney'
        elif 'cnyes.com' in url:
            return '鉅亨網'
        elif 'moneydj.com' in url:
            return 'MoneyDJ'
        elif 'money.udn.com' in url:
            return '經濟日報'
        elif 'ctee.com.tw' in url:
            return '工商時報'
        elif 'ettoday.net' in url:
            return 'ETtoday'
        elif 'goodinfo.tw' in url:
            return 'Goodinfo'
        elif 'macromicro.me' in url:
            return '財經M平方'
        elif 'businessweekly.com.tw' in url:
            return '商業周刊'
        elif 'technews.tw' in url:
            return '科技新報'
        elif 'nownews.com' in url:
            return 'Nownews'
        else:
            # 嘗試從 URL 提取域名
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
    except:
        return '未知網站'

# 測試用
if __name__ == "__main__":
    test_news_sources = [
        {"title": "台股反彈大漲", "link": "https://tw.finance.yahoo.com/news/example1"},
        {"title": "聯電法說會重點", "link": "https://www.cmoney.tw/notes/example2"},
        {"title": "外資買賣動向", "link": "https://www.cnyes.com/news/example3"}
    ]
    
    test_financial_sources = [
        {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/quote/2303.TW"}
    ]
    
    result = generate_sources_section(test_news_sources, test_financial_sources)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 