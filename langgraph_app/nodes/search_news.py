import requests
import json
import openai
from typing import List, Dict
import re
from datetime import datetime
import os

# 定義允許的來源網站
ALLOWED_SITES = [
    "tw.finance.yahoo.com",  # Yahoo奇摩股市
    "cnyes.com",  # 鉅亨網
    "moneydj.com",  # MoneyDJ 理財網
    "cmoney.tw",  # CMoney
    "money.udn.com",  # 經濟日報
    "ctee.com.tw",  # 工商時報
    "finance.ettoday.net",  # ETtoday 財經
    "goodinfo.tw",  # Goodinfo
    "macromicro.me",  # 財經M平方
    "smart.businessweekly.com.tw",  # Smart智富
    "technews.tw",  # 科技新報
    "nownews.com",  # Nownews
    "moneylink.com.tw",  # MoneyLink 富聯網
    "stockfeel.com.tw",  # 股感 StockFeel
    "businessweekly.com.tw",  # 商業周刊
    "businesstoday.com.tw",  # 今周刊
    "pchome.com.tw",  # PChome 股市頻道
]

PROMPT = '''你是一個專業投資分析助理，請根據使用者輸入的問題，自動生成一組精準的搜尋關鍵字，幫助查找最新且與台股相關的財經新聞或數據資訊。

⚠️限制來源：請僅從下列網站中抓取內容（出現在標題、網址或來源中才納入）：
Yahoo奇摩股市、鉅亨網 (cnyes)、MoneyDJ 理財網、CMoney、經濟日報、工商時報、ETtoday 財經、Goodinfo、財經M平方（MacroMicro）、Smart智富、科技新報、Nownews、MoneyLink 富聯網、股感 StockFeel、商業周刊、今周刊、PChome 股市頻道。

🧠使用者輸入會包含「公司名稱 / 股票代碼 + 問題」，請根據這些資訊生成具備高資訊密度的查詢組合，並試著涵蓋以下主題：
- 財報數據（例：EPS、營收、毛利率）
- 股價異動解釋
- 法人籌碼或投信、外資動態
- 分點主力動向
- 最新新聞事件
- ETF、產業輪動、題材發酵
- 分析師預估與目標價

📌請一次回傳 8-12 組具代表性的搜尋關鍵字組合，並充分利用所有允許的網站。每個網站至少生成一個關鍵字。

輸入資訊：
- 公司名稱：{{ company_name }}
- 股票代號：{{ stock_id }}
- 問題類型：{{ intent }}
- 關鍵字：{{ keywords }}
- 時間資訊：{{ time_info }}

輸出格式為 JSON 陣列，請包含以下網站的關鍵字：
[
  "{{ company_name }} {{ stock_id }} 財報 site:tw.finance.yahoo.com",
  "{{ company_name }} 外資買賣 site:cnyes.com",
  "{{ stock_id }} 法人動向 site:moneydj.com",
  "{{ company_name }} EPS 分析 site:cmoney.tw",
  "{{ company_name }} 財經新聞 site:money.udn.com",
  "{{ stock_id }} 工商時報 site:ctee.com.tw",
  "{{ company_name }} 財經報導 site:finance.ettoday.net",
  "{{ company_name }} 基本面 site:goodinfo.tw",
  "{{ company_name }} 總體經濟 site:macromicro.me",
  "{{ company_name }} 投資理財 site:smart.businessweekly.com.tw",
  "{{ company_name }} 科技新聞 site:technews.tw",
  "{{ company_name }} 即時新聞 site:nownews.com"
]
'''

def generate_search_keywords(company_name: str, stock_id: str, intent: str, keywords: List[str], event_type: str = '', time_info: str = '') -> List[str]:
    """生成搜尋關鍵詞，納入事件類型、時間、意圖，去除重複，財報等詞優先"""
    try:
        # 使用 OpenAI 生成更精準的搜尋關鍵字
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 準備 prompt
        prompt = PROMPT.replace("{{ company_name }}", company_name or "")
        prompt = prompt.replace("{{ stock_id }}", stock_id or "")
        prompt = prompt.replace("{{ intent }}", intent or "")
        prompt = prompt.replace("{{ keywords }}", ", ".join(keywords) if keywords else "")
        prompt = prompt.replace("{{ time_info }}", time_info or "")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # 解析 JSON 回應
        try:
            keywords_list = json.loads(content)
            if isinstance(keywords_list, list):
                return keywords_list[:12]  # 增加到最多12個關鍵字
        except json.JSONDecodeError:
            # 如果 JSON 解析失敗，嘗試提取引號內的內容
            import re
            matches = re.findall(r'"([^"]+)"', content)
            if matches:
                return matches[:12]
        
        # 如果 AI 生成失敗，使用預設關鍵字
        return generate_fallback_keywords(company_name, stock_id, intent, keywords, time_info)
        
    except Exception as e:
        print(f"[generate_search_keywords ERROR] {e}")
        return generate_fallback_keywords(company_name, stock_id, intent, keywords, time_info)

def generate_fallback_keywords(company_name: str, stock_id: str, intent: str, keywords: List[str], time_info: str = '') -> List[str]:
    """生成備用的搜尋關鍵字，充分利用所有允許的網站"""
    fallback_keywords = []
    
    # 基礎組合 - 充分利用所有主要網站
    if company_name and stock_id:
        fallback_keywords.extend([
            f"{company_name} {stock_id} 財報 site:tw.finance.yahoo.com",
            f"{company_name} 外資買賣 site:cnyes.com",
            f"{stock_id} 法人動向 site:moneydj.com",
            f"{company_name} EPS 分析 site:cmoney.tw",
            f"{company_name} 財經新聞 site:money.udn.com",
            f"{stock_id} 工商時報 site:ctee.com.tw",
            f"{company_name} 財經報導 site:finance.ettoday.net",
            f"{company_name} 基本面 site:goodinfo.tw",
            f"{company_name} 總體經濟 site:macromicro.me",
            f"{company_name} 投資理財 site:smart.businessweekly.com.tw",
            f"{company_name} 科技新聞 site:technews.tw",
            f"{company_name} 即時新聞 site:nownews.com"
        ])
    
    # 根據意圖添加特定關鍵字
    if "財報" in intent or "基本面" in intent:
        fallback_keywords.extend([
            f"{company_name} 營收 毛利率 site:cmoney.tw",
            f"{stock_id} 損益表 site:goodinfo.tw",
            f"{company_name} 財務分析 site:tw.finance.yahoo.com"
        ])
    
    if "籌碼" in intent or "法人" in intent:
        fallback_keywords.extend([
            f"{stock_id} 三大法人 site:goodinfo.tw",
            f"{company_name} 外資持股 site:cnyes.com",
            f"{stock_id} 投信動向 site:moneydj.com"
        ])
    
    if "技術" in intent:
        fallback_keywords.extend([
            f"{company_name} 技術分析 site:tw.finance.yahoo.com",
            f"{stock_id} 技術線圖 site:cmoney.tw",
            f"{company_name} 技術指標 site:goodinfo.tw"
        ])
    
    # 添加時間相關關鍵字
    if time_info:
        fallback_keywords.extend([
            f"{company_name} {time_info} 新聞 site:cnyes.com",
            f"{stock_id} {time_info} 報導 site:money.udn.com",
            f"{company_name} {time_info} 分析 site:finance.ettoday.net"
        ])
    
    # 添加年份相關關鍵字
    current_year = "2025"
    last_year = "2024"
    if company_name:
        fallback_keywords.extend([
            f"{company_name} {current_year} 財報 site:tw.finance.yahoo.com",
            f"{company_name} {last_year} 損益表 site:cnyes.com",
            f"{stock_id} {current_year} 法人動向 site:moneydj.com"
        ])
    
    # 去除重複並限制數量
    unique_keywords = list(dict.fromkeys(fallback_keywords))
    return unique_keywords[:12]  # 增加到最多12個關鍵字

def filter_results_by_site(results: List[Dict]) -> List[Dict]:
    """過濾結果，只保留允許的網站"""
    filtered_results = []
    
    for result in results:
        link = result.get("link", "").lower()
        title = result.get("title", "").lower()
        
        # 檢查是否來自允許的網站
        is_allowed = False
        site_name = ""
        
        for site in ALLOWED_SITES:
            if site in link or site.replace(".", "") in link:
                is_allowed = True
                site_name = site
                break
        
        if is_allowed:
            # 添加網站資訊到結果中
            result["site_name"] = site_name
            result["filtered"] = True
            filtered_results.append(result)
        else:
            # 標記為被過濾的結果
            result["filtered"] = False
    
    return filtered_results

def extract_date_from_result(result: Dict) -> str:
    """從搜尋結果中提取日期資訊"""
    try:
        # 從標題或摘要中尋找日期模式
        text = f"{result.get('title', '')} {result.get('snippet', '')}"
        
        # 常見的日期模式
        date_patterns = [
            r'(\d{4}年\d{1,2}月\d{1,2}日)',  # 2024年1月1日
            r'(\d{4}/\d{1,2}/\d{1,2})',      # 2024/1/1
            r'(\d{4}-\d{1,2}-\d{1,2})',      # 2024-1-1
            r'(\d{1,2}/\d{1,2})',            # 1/1
            r'(今天|昨天|前天|明天)',         # 相對日期
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return "無日期資訊"
        
    except Exception as e:
        print(f"[extract_date_from_result ERROR] {e}")
        return "無日期資訊"

def log_search_results(search_keywords: List[str], results: List[Dict]):
    """記錄搜尋結果的詳細資訊"""
    print(f"\n🔍 搜尋關鍵字: {search_keywords}")
    print(f"📊 總結果數: {len(results)}")
    
    allowed_count = sum(1 for r in results if r.get("filtered", False))
    filtered_count = len(results) - allowed_count
    
    print(f"✅ 符合網站限制: {allowed_count} 個")
    print(f"❌ 被過濾: {filtered_count} 個")
    
    # 記錄每個結果的詳細資訊
    for i, result in enumerate(results[:10], 1):  # 只記錄前10個
        title = result.get("title", "無標題")
        link = result.get("link", "無連結")
        site_name = result.get("site_name", "未知網站")
        date_info = extract_date_from_result(result)
        filtered = result.get("filtered", False)
        
        status = "✅" if filtered else "❌"
        print(f"{status} {i}. [{site_name}] {title}")
        print(f"   連結: {link}")
        print(f"   日期: {date_info}")
        print()

def group_search_keywords(keywords: List[str], group_count: int = 4) -> List[List[str]]:
    """
    將搜尋關鍵字分組，平均分配到多個搜尋請求中
    
    Args:
        keywords: 所有搜尋關鍵字
        group_count: 分組數量，預設為4組
    
    Returns:
        分組後的關鍵字列表
    """
    if not keywords:
        return []
    
    # 計算每組應該包含的關鍵字數量
    keywords_per_group = max(1, len(keywords) // group_count)
    
    # 分組
    groups = []
    for i in range(0, len(keywords), keywords_per_group):
        group = keywords[i:i + keywords_per_group]
        if group:  # 確保組不為空
            groups.append(group)
    
    # 如果組數不足，用空組填充
    while len(groups) < group_count:
        groups.append([])
    
    # 限制組數
    return groups[:group_count]

def search_news_grouped(company_name: str, stock_id: str, intent: str, keywords: List[str], serper_api_key: str = None, event_type: str = '', time_info: str = '', group_count: int = 4) -> Dict:
    """
    使用分組搜尋的方式執行新聞搜尋
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        intent: 搜尋意圖
        keywords: 搜尋關鍵字列表
        serper_api_key: Serper API 金鑰
        event_type: 事件類型
        time_info: 時間資訊
        group_count: 分組數量，預設為4組
    
    Returns:
        合併後的搜尋結果
    """
    try:
        # 如果沒有提供 API key，嘗試從環境變數讀取
        if not serper_api_key:
            serper_api_key = os.getenv("SERPER_API_KEY")
        
        # 生成搜尋關鍵字
        all_keywords = generate_search_keywords(company_name, stock_id, intent, keywords, event_type, time_info)
        
        # 分組關鍵字
        keyword_groups = group_search_keywords(all_keywords, group_count)
        
        print(f"🔍 分組搜尋 - 總關鍵字數: {len(all_keywords)}")
        print(f"📊 分組數量: {len(keyword_groups)}")
        for i, group in enumerate(keyword_groups, 1):
            print(f"   第{i}組 ({len(group)}個): {group}")
        print()
        
        # 執行分組搜尋
        all_results = []
        all_search_keywords = []
        
        for i, keyword_group in enumerate(keyword_groups, 1):
            if not keyword_group:
                continue
                
            print(f"🔍 執行第{i}組搜尋...")
            
            # 執行單組搜尋
            group_result = search_news_single_group(
                company_name, stock_id, intent, keyword_group, serper_api_key, event_type, time_info
            )
            
            if group_result.get("success"):
                group_results = group_result.get("results", [])
                all_results.extend(group_results)
                all_search_keywords.extend(keyword_group)
                
                print(f"✅ 第{i}組搜尋成功，獲得 {len(group_results)} 個結果")
            else:
                print(f"❌ 第{i}組搜尋失敗: {group_result.get('error', '未知錯誤')}")
        
        # 去重結果
        unique_results = remove_duplicate_results(all_results)
        
        print(f"\n📊 分組搜尋完成:")
        print(f"   總搜尋關鍵字: {len(all_search_keywords)}")
        print(f"   總結果數: {len(all_results)}")
        print(f"   去重後結果數: {len(unique_results)}")
        
        return {
            "success": True,
            "results": unique_results,
            "search_keywords": all_search_keywords,
            "total_groups": len(keyword_groups),
            "message": f"分組搜尋完成，共{len(keyword_groups)}組，獲得{len(unique_results)}個結果"
        }
        
    except Exception as e:
        print(f"[search_news_grouped ERROR] {e}")
        return {
            "success": False,
            "error": f"分組搜尋失敗: {str(e)}",
            "results": []
        }

def search_news_single_group(company_name: str, stock_id: str, intent: str, keywords: List[str], serper_api_key: str = None, event_type: str = '', time_info: str = '') -> Dict:
    """
    執行單組關鍵字的搜尋
    """
    try:
        # 如果沒有提供 API key，嘗試從環境變數讀取
        if not serper_api_key:
            serper_api_key = os.getenv("SERPER_API_KEY")
        
        if not serper_api_key:
            return {
                "success": False,
                "error": "缺少 SERPER_API_KEY",
                "results": []
            }
        
        # 使用第一個關鍵字進行搜尋
        if keywords:
            search_query = keywords[0]
            
            # 發送搜尋請求
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": serper_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": search_query,
                "num": 10  # 每組搜尋10個結果
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                organic_results = data.get("organic", [])
                
                # 過濾結果
                filtered_results = filter_results_by_site(organic_results)
                
                # 記錄搜尋結果
                log_search_results(keywords, filtered_results)
                
                return {
                    "success": True,
                    "results": filtered_results,
                    "search_keywords": keywords,
                    "message": f"單組搜尋成功，關鍵字: {search_query}"
                }
            else:
                return {
                    "success": False,
                    "error": f"API 請求失敗: {response.status_code}",
                    "results": []
                }
        else:
            return {
                "success": False,
                "error": "沒有搜尋關鍵字",
                "results": []
            }
            
    except Exception as e:
        print(f"[search_news_single_group ERROR] {e}")
        return {
            "success": False,
            "error": f"單組搜尋失敗: {str(e)}",
            "results": []
        }

def remove_duplicate_results(results: List[Dict]) -> List[Dict]:
    """
    去除重複的搜尋結果
    """
    seen_urls = set()
    unique_results = []
    
    for result in results:
        url = result.get("link", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    return unique_results

def search_news(company_name: str, stock_id: str, intent: str, keywords: List[str], serper_api_key: str = None, event_type: str = '', time_info: str = '') -> Dict:
    """
    使用 Serper API 搜尋新聞，並過濾來源網站（原始版本）
    """
    try:
        # 生成搜尋關鍵詞
        search_keywords = generate_search_keywords(company_name, stock_id, intent, keywords, event_type, time_info)
        
        print(f"🔍 生成的搜尋關鍵字: {search_keywords}")
        
        # 如果沒有提供 Serper API key，返回模擬結果
        if not serper_api_key:
            mock_results = [
                {
                    "title": f"{company_name} 股價分析 - Yahoo奇摩股市",
                    "snippet": f"根據最新市場資料，{company_name}({stock_id})近期表現...",
                    "link": f"https://tw.finance.yahoo.com/news/{stock_id}",
                    "site_name": "tw.finance.yahoo.com",
                    "filtered": True
                },
                {
                    "title": f"{company_name} 財報分析 - 鉅亨網",
                    "snippet": f"{company_name}最新財報顯示...",
                    "link": f"https://cnyes.com/news/{stock_id}",
                    "site_name": "cnyes.com",
                    "filtered": True
                }
            ]
            
            log_search_results(search_keywords, mock_results)
            
            return {
                "success": True,
                "search_keywords": search_keywords,
                "results": mock_results,
                "message": "使用模擬資料（請設定 Serper API key 以獲取真實搜尋結果）"
            }
        
        # 使用 Serper API 進行搜尋
        all_results = []
        
        for keyword in search_keywords:
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": serper_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": keyword,
                "num": 10  # 每個關鍵詞搜尋10個結果
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "organic" in data:
                    all_results.extend(data["organic"])
            else:
                print(f"Serper API 請求失敗: {response.status_code}")
        
        # 過濾結果
        filtered_results = filter_results_by_site(all_results)
        
        # 記錄搜尋結果
        log_search_results(search_keywords, filtered_results)
        
        return {
            "success": True,
            "search_keywords": search_keywords,
            "results": filtered_results[:15],  # 限制最多15個結果
            "message": f"成功搜尋到 {len(filtered_results)} 個符合條件的結果"
        }
        
    except Exception as e:
        print(f"[search_news ERROR] {e}")
        return {
            "success": False,
            "error": str(e),
            "search_keywords": [],
            "results": []
        }

def search_news_smart(company_name: str, stock_id: str, intent: str, keywords: List[str], serper_api_key: str = None, event_type: str = '', time_info: str = '', use_grouped: bool = True) -> Dict:
    """
    智能選擇搜尋方式
    
    Args:
        company_name: 公司名稱
        stock_id: 股票代號
        intent: 搜尋意圖
        keywords: 搜尋關鍵字列表
        serper_api_key: Serper API 金鑰
        event_type: 事件類型
        time_info: 時間資訊
        use_grouped: 是否使用分組搜尋，預設為True
    
    Returns:
        搜尋結果
    """
    if use_grouped:
        print("🔍 使用分組搜尋模式")
        return search_news_grouped(company_name, stock_id, intent, keywords, serper_api_key, event_type, time_info)
    else:
        print("🔍 使用傳統搜尋模式")
        return search_news(company_name, stock_id, intent, keywords, serper_api_key, event_type, time_info)

# 測試用
if __name__ == "__main__":
    result = search_news(
        company_name="台積電",
        stock_id="2330", 
        intent="個股分析",
        keywords=["財報", "EPS"]
    )
    print(json.dumps(result, ensure_ascii=False, indent=2)) 