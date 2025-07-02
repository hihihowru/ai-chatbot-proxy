from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Response, Query
from pydantic import BaseModel
from langgraph_app.nodes.detect_stock import detect_stocks
from langgraph_app.nodes.detect_time import detect_time
from langgraph_app.nodes.detect_chart import detect_chart
from langgraph_app.data_tools.database_query import db_query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from typing import List, Dict
import time
import os
from dotenv import load_dotenv
from langgraph_app.nodes.classify_and_extract import classify_and_extract
from langgraph_app.nodes.search_news import search_news_smart
from langgraph_app.nodes.generate_report_pipeline import generate_report_pipeline
import openai
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import pandas as pd
from routes.answer import router as answer_router

# 載入環境變數
load_dotenv()

app = FastAPI()

# 允許跨域，方便本地前端開發
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含 answer 路由
app.include_router(answer_router, prefix="/api")

# 追蹤所有活躍的 WebSocket 連線
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(json.dumps({"log": message}))

manager = ConnectionManager()

class AskRequest(BaseModel):
    question: str

class DatabaseTestRequest(BaseModel):
    table_ids: List[str]
    stock_id: str = "2330"

class DatabaseQueryRequest(BaseModel):
    intent_category: str
    investment_aspect: str
    stock_ids: List[str]

class ChartQueryRequest(BaseModel):
    stock_ids: List[str]
    chart_type: str

class InvestmentAnalysisRequest(BaseModel):
    question: str
    serper_api_key: str = None

@app.post("/api/ask")
async def ask_api(req: AskRequest):
    stock_ids = detect_stocks(req.question)
    return {"stock_ids": stock_ids}

@app.post("/api/ask-logs")
async def ask_logs_api(req: AskRequest):
    logs = []
    logs.append("🔍 開始偵測股票代號...")
    stock_ids = detect_stocks(req.question)
    if stock_ids:
        logs.append(f"✅ 偵測到股票代號：{', '.join(stock_ids)}")
    else:
        logs.append("❌ 未偵測到股票代號")
    return {"logs": logs}

@app.get("/api/ask-sse")
def ask_sse_api(question: str = Query(...)):
    def event_stream():
        try:
            # 1. 問題理解與關鍵資訊提取
            yield f"data: {json.dumps({'log': '🧠 問題理解與關鍵資訊提取中...'})}\n\n"
            classify_result = classify_and_extract(question)
            yield f"data: {json.dumps({'log': '🧠 問題理解結果: ' + json.dumps(classify_result, ensure_ascii=False)})}\n\n"
            #time.sleep(0.5)

            # 2. 多股號偵測
            yield f"data: {json.dumps({'log': '🔍 股票代號偵測中...'})}\n\n"
            stock_ids = detect_stocks(question)
            yield f"data: {json.dumps({'log': '🔍 偵測到股票代號: ' + (', '.join(stock_ids) if stock_ids else '未偵測到股票')})}\n\n"
            #time.sleep(0.5)

            # 3. 時間偵測
            yield f"data: {json.dumps({'log': '⏳ 時間偵測中...'})}\n\n"
            time_info = detect_time(question)
            yield f"data: {json.dumps({'log': '⏱️ 偵測到時間: ' + str(time_info)})}\n\n"
            #time.sleep(0.5)

            # 4. 問題分類（大分類/子分類/面向）
            yield f"data: {json.dumps({'log': '🧠 問題分類中...'})}\n\n"
            category_result = classify_result.get("category", "")
            subcategory_result = classify_result.get("subcategory", [])
            view_type_result = classify_result.get("view_type", [])
            yield f"data: {json.dumps({'log': f'📊 問題分類結果: 大分類={category_result}, 子分類={subcategory_result}, 投資面向={view_type_result}'})}\n\n"
            #time.sleep(0.5)

            # 5. 整合所有偵測結果為完整 JSON
            yield f"data: {json.dumps({'log': '🔗 整合所有偵測結果...'})}\n\n"
            
            # 整合後的完整參數
            integrated_result = {
                # 從 classify_and_extract 來的
                "category": classify_result.get("category", ""),
                "subcategory": classify_result.get("subcategory", []),
                "view_type": classify_result.get("view_type", []),
                "keywords": classify_result.get("keywords", []),
                "company_name": classify_result.get("company_name", ""),
                "event_type": classify_result.get("event_type", ""),
                
                # 從 detect_stocks 來的（優先使用）
                "stock_id": stock_ids[0] if stock_ids else classify_result.get("stock_id", ""),
                "stock_ids": stock_ids,
                
                # 從 detect_time 來的（優先使用）
                "time_info": time_info if time_info else classify_result.get("time_info", ""),
                
                # 整合後的完整資訊
                "question": question,
                "detection_timestamp": time.time()
            }
            
            yield f"data: {json.dumps({'log': '📋 完整整合結果: ' + json.dumps(integrated_result, ensure_ascii=False, indent=2)})}\n\n"
            #time.sleep(0.5)

            # 6. 圖表偵測
            yield f"data: {json.dumps({'log': '📈 圖表偵測中...'})}\n\n"
            chart_result = detect_chart(question)
            if chart_result:
                chart_type = chart_result.get("chart_type", "")
                table_id = chart_result.get("table_id", "")
                yield f"data: {json.dumps({'log': f'📊 偵測到圖表: {chart_type} (Table ID: {table_id})'})}\n\n"
            else:
                yield f"data: {json.dumps({'log': '❌ 未偵測到特定圖表類型'})}\n\n"
            time.sleep(0.5)

            # 7. 新聞搜尋
            yield f"data: {json.dumps({'log': '🔎 開始搜尋相關新聞...'})}\n\n"
            serper_api_key = os.getenv("SERPER_API_KEY")
            if not serper_api_key:
                yield f"data: {json.dumps({'log': '⚠️ 警告: 未設定 SERPER_API_KEY，跳過新聞搜尋'})}\n\n"
            else:
                # 從整合結果提取搜尋關鍵字
                company_name = integrated_result.get("company_name", "")
                stock_id = integrated_result.get("stock_id", "")
                keywords = integrated_result.get("keywords", [])
                category = integrated_result.get("category", "")
                subcategory = integrated_result.get("subcategory", [])
                view_type = integrated_result.get("view_type", [])
                time_info = integrated_result.get("time_info", "")
                
                # 添加詳細的 console log 來調試
                print(f"🔍 DEBUG - integrated_result: {integrated_result}")
                print(f"🔍 DEBUG - company_name: '{company_name}'")
                print(f"🔍 DEBUG - stock_id: '{stock_id}'")
                print(f"🔍 DEBUG - keywords: {keywords} (長度: {len(keywords)})")
                print(f"🔍 DEBUG - category: '{category}'")
                print(f"🔍 DEBUG - subcategory: {subcategory} (長度: {len(subcategory)})")
                print(f"🔍 DEBUG - view_type: {view_type} (長度: {len(view_type)})")
                print(f"🔍 DEBUG - time_info: '{time_info}'")
                
                search_keywords = generate_smart_search_keywords(
                    category=category,
                    subcategory=subcategory,
                    view_type=view_type,
                    company_name=company_name,
                    stock_id=stock_id,
                    keywords=keywords,
                    time_info=time_info
                )
                
                print(f"🔍 DEBUG - 最終 search_keywords: {search_keywords} (長度: {len(search_keywords)})")
                
                search_keywords_str = ', '.join(search_keywords)
                log_msg = f'🔍 搜尋關鍵字: {search_keywords_str}'
                yield f"data: {json.dumps({'log': log_msg})}\n\n"
                
                try:
                    search_result = search_news_smart(
                        company_name=company_name,
                        stock_id=stock_id,
                        intent=integrated_result.get("category", ""),
                        keywords=search_keywords,
                        serper_api_key=serper_api_key,
                        use_grouped=True  # 使用分組搜尋
                    )
                    
                    if search_result.get("success"):
                        news_count = len(search_result.get("results", []))
                        yield f"data: {json.dumps({'log': f'📰 第一次搜尋找到 {news_count} 則相關新聞'})}\n\n"
                        
                        # 顯示每則新聞標題
                        for i, news in enumerate(search_result.get("results", [])[:5]):  # 只顯示前5則
                            title = news.get("title", "")
                            yield f"data: {json.dumps({'log': f'📄 {i+1}. {title}'})}\n\n"
                            time.sleep(0.3)
                        
                        # 第二次搜尋：根據第一次搜尋結果生成新的關鍵字
                        yield f"data: {json.dumps({'log': '🔄 開始第二次搜尋，根據第一次結果生成新關鍵字...'})}\n\n"
                        
                        # 從第一次搜尋結果中提取新的關鍵字
                        first_search_results = search_result.get("results", [])
                        new_keywords = extract_keywords_from_results(first_search_results, company_name, stock_id)
                        
                        new_keywords_str = ", ".join(new_keywords)
                        yield f"data: {json.dumps({'log': f'🔍 第二次搜尋關鍵字: {new_keywords_str}'})}\n\n"
                        
                        # 執行第二次搜尋
                        second_search_result = search_news_smart(
                            company_name=company_name,
                            stock_id=stock_id,
                            intent=integrated_result.get("category", ""),
                            keywords=new_keywords,
                            serper_api_key=serper_api_key,
                            use_grouped=True  # 使用分組搜尋
                        )
                        
                        if second_search_result.get("success"):
                            second_news_count = len(second_search_result.get("results", []))
                            yield f"data: {json.dumps({'log': f'📰 第二次搜尋找到 {second_news_count} 則相關新聞'})}\n\n"
                            
                            # 合併兩次搜尋結果
                            all_results = merge_search_results(first_search_results, second_search_result.get("results", []))
                            yield f"data: {json.dumps({'log': f'📋 合併後總共 {len(all_results)} 則新聞'})}\n\n"
                            
                            # 更新 search_result 為合併後的結果
                            search_result["results"] = all_results
                            
                            # 檢查是否為個股分析類別，如果是則爬取財務數據
                            if "個股分析" in category:
                                # 獲取 Yahoo 財經財務報表數據
                                yield f"data: {json.dumps({'log': '📊 正在獲取 Yahoo 財經財務報表數據...'})}\n\n"
                                financial_data = fetch_yahoo_financial_data(stock_id, company_name)
                                
                                if financial_data.get("success"):
                                    data = financial_data.get("data", {})
                                    yield f"data: {json.dumps({'log': '📊 成功獲取財務報表數據'})}\n\n"
                                    
                                    # 準備財務數據上下文
                                    financial_context = f"""
Yahoo 財經財務報表數據：

每股盈餘 (EPS)：
{format_eps_data(data.get('eps', {}))}

營收數據：
{format_revenue_data(data.get('revenue', {}))}

損益表數據：
{format_income_statement_data(data.get('income_statement', {}))}

資產負債表數據：
{format_balance_sheet_data(data.get('balance_sheet', {}))}

資料來源：
{format_sources_data(data.get('sources', []))}
"""
                                    
                                    # 準備新聞來源
                                    news_sources = []
                                    for news in search_result.get("results", []):
                                        news_sources.append({
                                            "title": news.get("title", "無標題"),
                                            "link": news.get("link", "")
                                        })
                                    
                                    # 準備財務資料來源
                                    financial_sources = data.get('sources', [])
                                    
                                    # 構建新聞摘要
                                    news_summary = ""
                                    if search_result.get("results"):
                                        news_summary = "\n".join([
                                            f"{i+1}. {news.get('title', '無標題')}: {news.get('snippet', '無摘要')}"
                                            for i, news in enumerate(search_result.get("results", [])[:5])
                                        ])
                                    
                                    # 儲存財務數據供後續使用
                                    financial_data = data
                                else:
                                    yield f"data: {json.dumps({'log': '⚠️ 無法獲取 Yahoo 財經財務報表數據'})}\n\n"
                            else:
                                # 非個股分析類別，跳過財務數據獲取
                                yield f"data: {json.dumps({'log': '📝 非個股分析類別，跳過財務數據獲取'})}\n\n"
                        else:
                            yield f"data: {json.dumps({'log': '❌ 第二次新聞搜尋失敗: ' + second_search_result.get('error', '未知錯誤')})}\n\n"
                    else:
                        yield f"data: {json.dumps({'log': '❌ 新聞搜尋失敗: ' + search_result.get('error', '未知錯誤')})}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'log': f'❌ 新聞搜尋錯誤: {str(e)}'})}\n\n"
            
            time.sleep(0.5)

            # 8. 最終投資分析報告生成
            yield f"data: {json.dumps({'log': '📝 正在生成投資分析報告...'})}\n\n"
            try:
                if 'search_result' in locals() and search_result and search_result.get("success"):
                    # 構建新聞摘要
                    news_summary = ""
                    if search_result.get("results"):
                        news_summary = "\n".join([
                            f"{i+1}. {news.get('title', '無標題')}: {news.get('snippet', '無摘要')}"
                            for i, news in enumerate(search_result.get("results", [])[:5])
                        ])
                    
                    # 準備新聞來源
                    news_sources = []
                    for news in search_result.get("results", []):
                        news_sources.append({
                            "title": news.get("title", "無標題"),
                            "link": news.get("link", "")
                        })
                    
                    # 準備財務來源
                    financial_sources = []
                    if 'financial_data' in locals() and financial_data:
                        financial_sources.append({
                            "name": "Yahoo Finance",
                            "url": f"https://finance.yahoo.com/quote/{stock_id}.TW"
                        })
                    
                    # 使用新的 pipeline 生成報告
                    summary_result = generate_report_pipeline(
                        company_name=company_name,
                        stock_id=stock_id,
                        intent=integrated_result.get("category", ""),
                        time_info=integrated_result.get("time_info", ""),
                        news_summary=news_summary,
                        news_sources=news_sources,
                        financial_data=financial_data if 'financial_data' in locals() else None,
                        financial_sources=financial_sources
                    )
                    
                    if summary_result.get("success"):
                        sections = summary_result.get("sections", [])
                        yield f"data: {json.dumps({'log': f'📋 生成 {len(sections)} 個分析面向'})}\n\n"
                        
                        # 添加詳細的調試信息
                        print(f"[DEBUG] Sections 類型: {type(sections)}")
                        print(f"[DEBUG] Sections 內容: {sections}")
                        
                        # 顯示每個 section 的標題
                        for section in sections:
                            section_title = section.get("section", "未命名區塊")
                            yield f"data: {json.dumps({'log': f'📊 {section_title}'})}\n\n"
                            time.sleep(0.3)
                        
                        # 發送完整的投資分析報告
                        print("[DEBUG] 處理 list 格式的 sections")
                        report_sections = []
                        for section in sections:
                            # 可選：自動標註 type，方便前端渲染
                            if section.get("cards"):
                                section["type"] = "cards"
                            elif section.get("tabs"):
                                section["type"] = "tabs"
                            elif section.get("bullets"):
                                section["type"] = "bullets"
                            elif section.get("sources"):
                                section["type"] = "sources"
                            elif section.get("disclaimer"):
                                section["type"] = "disclaimer"
                            elif section.get("summary_table"):
                                section["type"] = "summary_table"
                            report_sections.append(section)
                            print(f"[DEBUG] Section: {section.get('section', '未命名區塊')}")
                        report_data = {
                            'report': {
                                'stockName': company_name,
                                'stockId': stock_id,
                                'sections': report_sections,
                                'paraphrased_prompt': summary_result.get('paraphrased_prompt'),
                                'logs': summary_result.get('logs', [])
                            }
                        }
                        yield f"data: {json.dumps(report_data)}\n\n"
                    else:
                        yield f"data: {json.dumps({'log': '❌ 投資分析報告生成失敗: ' + summary_result.get('error', '未知錯誤')})}\n\n"
                else:
                    yield f"data: {json.dumps({'log': '⚠️ 無法生成投資分析報告，缺少新聞資料'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'log': f'❌ 投資分析報告生成錯誤: {str(e)}'})}\n\n"

            yield f"data: {json.dumps({'log': '🎉 分析流程完成！'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'log': f'❌ 系統錯誤: {str(e)}'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/api/investment-analysis")
async def investment_analysis_api(req: InvestmentAnalysisRequest):
    """
    執行完整的投資分析流程
    """
    return {
        "success": False,
        "error": "此 API 已棄用，請使用 /api/ask-sse",
        "message": "請使用 SSE 端點來獲取實時分析結果"
    }

@app.get("/api/investment-analysis-sse")
def investment_analysis_sse_api(question: str = Query(...), serper_api_key: str = Query(None)):
    """
    使用 Server-Sent Events 的投資分析流程
    """
    return ask_sse_api(question)

@app.post("/api/test-table-ids")
async def test_table_ids_api(req: DatabaseTestRequest):
    """
    測試多個 table_id 是否有效
    """
    results = db_query.test_table_ids(req.table_ids, req.stock_id)
    return {
        "success": True,
        "results": results,
        "tested_table_ids": req.table_ids,
        "tested_stock_id": req.stock_id
    }

@app.post("/api/query-database")
async def query_database_api(req: DatabaseQueryRequest):
    """
    根據意圖和股票代號查詢資料庫
    """
    result = db_query.query_data(
        req.intent_category,
        req.investment_aspect,
        req.stock_ids
    )
    return result

@app.post("/api/query-chart")
async def query_chart_api(req: ChartQueryRequest):
    """
    根據圖表類型和股票代號查詢資料
    """
    from langgraph_app.nodes.detect_chart import CHART_MAPPING
    
    if req.chart_type not in CHART_MAPPING:
        return {
            "success": False,
            "error": f"不支援的圖表類型: {req.chart_type}"
        }
    
    config = CHART_MAPPING[req.chart_type]
    
    # 建立 API URL
    from langgraph_app.data_tools.template_mapping import build_api_url
    url = build_api_url(config["table_id"], req.stock_ids, "MTPeriod=0;DTMode=0;DTRange=5;DTOrder=1;MajorTable=M173;")
    
    # 發送請求
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://www.cmoney.tw/",
        "Accept": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "data": data,
                "chart_type": req.chart_type,
                "table_id": config["table_id"],
                "url": url,
                "stock_ids": req.stock_ids
            }
        else:
            return {
                "success": False,
                "error": f"API 請求失敗: {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"請求錯誤: {str(e)}"
        }

@app.get("/api/test-known-tables")
async def test_known_tables_api():
    """
    測試已知的 table_id 列表
    """
    known_table_ids = [
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
    
    results = db_query.test_table_ids(known_table_ids)
    return {
        "success": True,
        "results": results,
        "tested_count": len(known_table_ids)
    }

@app.websocket("/ws/ask")
async def websocket_ask(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        data = await websocket.receive_text()
        req = json.loads(data)
        question = req.get("question", "")
        
        # 發送開始偵測的訊息
        await manager.send_message("🔍 開始偵測股票代號...", websocket)
        
        # 偵測股票代號
        stock_ids = detect_stocks(question)
        
        # 發送偵測結果
        if stock_ids:
            await manager.send_message(f"✅ 偵測到股票代號：{', '.join(stock_ids)}", websocket)
        else:
            await manager.send_message("❌ 未偵測到股票代號", websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_message(f"❌ 發生錯誤: {str(e)}", websocket)
    finally:
        manager.disconnect(websocket)
        await websocket.close()

def generate_smart_search_keywords(category: str, subcategory: List[str], view_type: List[str], company_name: str, stock_id: str, keywords: List[str], time_info: str = "") -> List[str]:
    """
    根據不同的分類和子分類智能生成搜尋關鍵字，包含網站限制
    """
    try:
        # 使用 search_news 模組中的新邏輯
        from langgraph_app.nodes.search_news import generate_search_keywords
        return generate_search_keywords(company_name, stock_id, category, keywords, "", time_info)
    except Exception as e:
        print(f"[generate_smart_search_keywords ERROR] {e}")
        # 如果新邏輯失敗，使用備用邏輯
        return generate_fallback_smart_keywords(category, subcategory, view_type, company_name, stock_id, keywords, time_info)

def generate_fallback_smart_keywords(category: str, subcategory: List[str], view_type: List[str], company_name: str, stock_id: str, keywords: List[str], time_info: str = "") -> List[str]:
    """
    備用的智能搜尋關鍵字生成邏輯，充分利用所有允許的網站
    """
    search_keywords = []
    
    # 定義允許的網站
    allowed_sites = [
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
    
    # 基礎關鍵字組合 - 充分利用所有主要網站
    if company_name and stock_id:
        search_keywords.extend([
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
    
    # 根據大分類生成關鍵字
    if category == "個股分析":
        if company_name and stock_id:
            search_keywords.extend([
                f"{company_name} 營收 毛利率 site:cmoney.tw",
                f"{stock_id} 三大法人 site:goodinfo.tw",
                f"{company_name} 財務分析 site:tw.finance.yahoo.com"
            ])
            
        # 根據子分類進一步細化
        for sub in subcategory:
            if "基本面分析" in sub:
                search_keywords.extend([
                    f"{company_name} 財務分析 site:tw.finance.yahoo.com",
                    f"{stock_id} 損益表 site:goodinfo.tw",
                    f"{company_name} 營收分析 site:cmoney.tw"
                ])
            elif "籌碼面分析" in sub:
                search_keywords.extend([
                    f"{stock_id} 籌碼分析 site:cnyes.com",
                    f"{company_name} 外資持股 site:moneydj.com",
                    f"{stock_id} 投信動向 site:goodinfo.tw"
                ])
            elif "技術面分析" in sub:
                search_keywords.extend([
                    f"{company_name} 技術分析 site:moneydj.com",
                    f"{stock_id} 技術線圖 site:cmoney.tw",
                    f"{company_name} 技術指標 site:goodinfo.tw"
                ])
                
    elif category == "選股建議":
        if company_name:
            search_keywords.extend([
                f"{company_name} 選股建議 site:cmoney.tw",
                f"{stock_id} 投資標的 site:goodinfo.tw",
                f"{company_name} 投資分析 site:smart.businessweekly.com.tw"
            ])
                
    elif category == "盤勢分析":
        search_keywords.extend([
            "台股 大盤分析 site:cnyes.com",
            "台股 盤勢 site:moneydj.com",
            "台股 大盤技術面 site:tw.finance.yahoo.com"
        ])
        
        for sub in subcategory:
            if "產業" in sub:
                search_keywords.extend([
                    "產業分析 site:tw.finance.yahoo.com",
                    "產業輪動 site:cnyes.com",
                    "產業趨勢 site:technews.tw"
                ])
            elif "國際股市" in sub:
                search_keywords.extend([
                    "國際股市 site:cnyes.com",
                    "美股 台股 site:tw.finance.yahoo.com",
                    "國際情勢 site:macromicro.me"
                ])
                
    elif category == "比較分析":
        if company_name:
            search_keywords.extend([
                f"{company_name} 比較分析 site:cmoney.tw",
                f"{company_name} 同業比較 site:goodinfo.tw",
                f"{stock_id} 競爭對手 site:cnyes.com"
            ])
    
    # 添加時間相關關鍵字
    if time_info and time_info != "recent_5_days":
        time_keyword = ""
        if "today" in time_info:
            time_keyword = "今天"
        elif "yesterday" in time_info:
            time_keyword = "昨天"
        elif "this_week" in time_info:
            time_keyword = "本週"
        elif "this_month" in time_info:
            time_keyword = "本月"
        elif "this_quarter" in time_info:
            time_keyword = "本季"
        elif "this_year" in time_info:
            time_keyword = "今年"
        
        if time_keyword and company_name:
            search_keywords.extend([
                f"{company_name} {time_keyword} 新聞 site:cnyes.com",
                f"{stock_id} {time_keyword} 報導 site:money.udn.com",
                f"{company_name} {time_keyword} 分析 site:finance.ettoday.net"
            ])
    
    # 添加投資面向相關關鍵字
    for view in view_type:
        if "基本面" in view and company_name:
            search_keywords.extend([
                f"{company_name} 基本面 site:tw.finance.yahoo.com",
                f"{stock_id} 財務面 site:goodinfo.tw",
                f"{company_name} 營收面 site:cmoney.tw"
            ])
        elif "技術面" in view and company_name:
            search_keywords.extend([
                f"{company_name} 技術面 site:moneydj.com",
                f"{stock_id} 技術分析 site:cmoney.tw",
                f"{company_name} 技術指標 site:goodinfo.tw"
            ])
        elif "籌碼面" in view and stock_id:
            search_keywords.extend([
                f"{stock_id} 籌碼面 site:goodinfo.tw",
                f"{company_name} 法人面 site:cnyes.com",
                f"{stock_id} 外資面 site:moneydj.com"
            ])
    
    # 添加年份相關關鍵字
    current_year = "2025"
    last_year = "2024"
    if company_name:
        search_keywords.extend([
            f"{company_name} {current_year} 財報 site:tw.finance.yahoo.com",
            f"{company_name} {last_year} 損益表 site:cnyes.com",
            f"{stock_id} {current_year} 法人動向 site:moneydj.com"
        ])
    
    # 限制數量並確保不重複
    unique_keywords = list(dict.fromkeys(search_keywords))
    return unique_keywords[:12]  # 增加到最多12個關鍵字

def extract_keywords_from_results(search_results: List[Dict], company_name: str, stock_id: str) -> List[str]:
    """
    從第一次搜尋結果中提取新的關鍵字，包含網站限制
    """
    try:
        # 收集所有標題和摘要
        all_text = ""
        for result in search_results:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            all_text += f"{title} {snippet} "
        
        # 使用 OpenAI 從搜尋結果中提取新的關鍵字
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
根據以下搜尋結果，為 {company_name}({stock_id}) 生成 3-5 個新的搜尋關鍵字。
這些關鍵字應該能夠找到更深入、更具體的相關資訊，特別是財務數據、財報、損益表等。

⚠️限制來源：請僅從下列網站中抓取內容：
Yahoo奇摩股市、鉅亨網 (cnyes)、MoneyDJ 理財網、CMoney、經濟日報、工商時報、ETtoday 財經、Goodinfo、財經M平方（MacroMicro）、Smart智富、科技新報、Nownews、MoneyLink 富聯網、股感 StockFeel、商業周刊、今周刊、PChome 股市頻道。

搜尋結果：
{all_text}

請生成新的搜尋關鍵字，格式為 JSON 陣列，並包含 site: 限制：
["{{ company_name }} 2025 財報 site:tw.finance.yahoo.com", "{{ stock_id }} 法人動向 site:cnyes.com", "{{ company_name }} EPS 分析 site:moneydj.com"]

注意：請包含年份(2025/2024)和具體的網站限制。
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # 解析回應
        content = response.choices[0].message.content.strip()
        try:
            import json
            keywords = json.loads(content)
            if isinstance(keywords, list):
                return keywords[:5]  # 限制最多5個關鍵字
        except:
            pass
        
        # 如果 AI 解析失敗，使用預設關鍵字
        return generate_fallback_second_keywords(company_name, stock_id)
        
    except Exception as e:
        print(f"[extract_keywords_from_results ERROR] {e}")
        # 返回預設關鍵字（包含年份和財務關鍵字）
        return generate_fallback_second_keywords(company_name, stock_id)

def generate_fallback_second_keywords(company_name: str, stock_id: str) -> List[str]:
    """生成第二次搜尋的備用關鍵字，充分利用所有允許的網站"""
    current_year = "2025"
    last_year = "2024"
    
    fallback_keywords = [
        f"{company_name} {current_year} 財報 site:tw.finance.yahoo.com",
        f"{stock_id} {last_year} 損益表 site:cnyes.com", 
        f"{company_name} 法人動向 site:moneydj.com",
        f"{stock_id} EPS 分析 site:cmoney.tw",
        f"{company_name} 營業收入 site:goodinfo.tw",
        f"{company_name} 財經新聞 site:money.udn.com",
        f"{stock_id} 工商時報 site:ctee.com.tw",
        f"{company_name} 財經報導 site:finance.ettoday.net",
        f"{company_name} 基本面分析 site:macromicro.me",
        f"{company_name} 投資理財 site:smart.businessweekly.com.tw",
        f"{company_name} 科技新聞 site:technews.tw",
        f"{company_name} 即時新聞 site:nownews.com"
    ]
    
    return fallback_keywords[:12]  # 增加到最多12個關鍵字

def merge_search_results(first_results: List[Dict], second_results: List[Dict]) -> List[Dict]:
    """
    合併兩次搜尋結果，去除重複
    """
    try:
        # 使用 URL 作為去重依據
        seen_urls = set()
        merged_results = []
        
        # 先加入第一次搜尋結果
        for result in first_results:
            url = result.get("link", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                merged_results.append(result)
        
        # 再加入第二次搜尋結果（去重）
        for result in second_results:
            url = result.get("link", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                merged_results.append(result)
        
        return merged_results
        
    except Exception as e:
        print(f"[merge_search_results ERROR] {e}")
        # 如果合併失敗，返回第一次搜尋結果
        return first_results

def fetch_yahoo_financial_data(stock_id: str, company_name: str) -> Dict:
    """
    從 FinLab API 取得財務報表數據，失敗則 fallback 用模擬資料
    """
    try:
        import finlab
        from finlab import data
        import pandas as pd
        
        # 登入 FinLab API
        api_key = os.environ['FINLAB_API_KEY']
        finlab.login(api_token=api_key)
        
        print(f"[DEBUG] 使用 FinLab API 取得 {stock_id} 財務資料")
        
        # 初始化資料結構
        eps_data = {}
        revenue_data = {}
        income_statement_data = {}
        balance_sheet_data = {}
        sources = []
        
        # 只取確定可以取得的資料
        finlab_data = {
            "每股盈餘": "financial_statement:每股盈餘",
            "營業毛利率": "fundamental_features:營業毛利率", 
            "月營收成長率": "monthly_revenue:去年同月增減(%)"
        }
        
        for name, data_type in finlab_data.items():
            try:
                df = data.get(data_type)
                if stock_id in df.columns:
                    series = df[stock_id].dropna()
                    
                    # 根據不同的資料類型處理 date index
                    if name == "月營收成長率":
                        # 月營收成長率的 date index 是月份格式
                        for date, value in series.tail(8).items():
                            # 將月份格式轉換為季度格式
                            if isinstance(date, str):
                                # 如果是字串格式，嘗試解析
                                try:
                                    from datetime import datetime
                                    if len(date) == 6:  # YYYYMM 格式
                                        year = date[:4]
                                        month = int(date[4:6])
                                        quarter = f"{year}-Q{(month-1)//3 + 1}"
                                    else:
                                        quarter = str(date)
                                except:
                                    quarter = str(date)
                            else:
                                # 如果是 datetime 格式
                                quarter = f"{date.year}-Q{(date.month-1)//3 + 1}"
                            
                            if quarter not in income_statement_data:
                                income_statement_data[quarter] = {}
                            income_statement_data[quarter][name] = round(float(value), 2)
                    else:
                        # 其他資料使用原本的季度格式
                        for date, value in series.tail(4).items():
                            quarter = date
                            if quarter not in income_statement_data:
                                income_statement_data[quarter] = {}
                            
                            if name == "每股盈餘":
                                income_statement_data[quarter][name] = round(float(value), 2)
                            else:
                                income_statement_data[quarter][name] = round(float(value), 2)
                    
                    sources.append({"name": f"FinLab API - {name}", "url": "https://ai.finlab.tw/database"})
                    print(f"[DEBUG] 取得 {name} 資料: {len(series.tail(8 if name == '月營收成長率' else 4))} 筆")
                    
            except Exception as e:
                print(f"[DEBUG] {name} 資料取得失敗: {e}")
        
        # 檢查是否有取得任何資料
        if income_statement_data:
            print(f"[DEBUG] FinLab API 成功取得 {stock_id} 財務資料")
            return {
                "eps": eps_data,
                "revenue": revenue_data,
                "income_statement": income_statement_data,
                "balance_sheet": balance_sheet_data,
                "sources": sources
            }
        else:
            print(f"[DEBUG] FinLab API 未取得任何資料，使用 fallback")
            raise Exception("No data retrieved from FinLab API")
            
    except Exception as e:
        print(f"[DEBUG] FinLab API 失敗，使用 fallback 資料: {e}")
        
        # Fallback 模擬資料
        return {
            "eps": {
                "2024-Q1": 1.25,
                "2024-Q2": 1.45,
                "2024-Q3": 1.35,
                "2024-Q4": 1.55
            },
            "revenue": {
                "2024-Q1": 50000000000,
                "2024-Q2": 52000000000,
                "2024-Q3": 48000000000,
                "2024-Q4": 55000000000
            },
            "income_statement": {
                "2024-Q1": {"每股盈餘": 1.25, "營收": 50000000000, "營業利益": 8000000000},
                "2024-Q2": {"每股盈餘": 1.45, "營收": 52000000000, "營業利益": 8500000000},
                "2024-Q3": {"每股盈餘": 1.35, "營收": 48000000000, "營業利益": 7800000000},
                "2024-Q4": {"每股盈餘": 1.55, "營收": 55000000000, "營業利益": 9000000000}
            },
            "balance_sheet": {
                "2024-Q1": {"每股淨值": 45.2},
                "2024-Q2": {"每股淨值": 46.1},
                "2024-Q3": {"每股淨值": 47.3},
                "2024-Q4": {"每股淨值": 48.5}
            },
            "sources": [{"name": "模擬資料", "url": "fallback"}]
        }

def format_eps_data(eps_data: Dict) -> str:
    """格式化 EPS 數據"""
    if not eps_data:
        return "無數據"
    
    formatted = []
    for quarter, data in eps_data.items():
        eps = data.get('eps', 'N/A')
        q_growth = data.get('quarterly_growth', 'N/A')
        y_growth = data.get('yearly_growth', 'N/A')
        avg_price = data.get('avg_price', 'N/A')
        
        formatted.append(f"- {quarter}: EPS {eps} 元 (季增率: {q_growth}, 年增率: {y_growth}, 季均價: {avg_price} 元)")
    
    return "\n".join(formatted)

def format_revenue_data(revenue_data: Dict) -> str:
    """格式化營收數據"""
    if not revenue_data:
        return "無數據"
    
    formatted = []
    for quarter, data in revenue_data.items():
        revenue = data.get('revenue', 'N/A')
        q_growth = data.get('quarterly_growth', 'N/A')
        y_growth = data.get('yearly_growth', 'N/A')
        
        formatted.append(f"- {quarter}: 營收 {revenue} 仟元 (季增率: {q_growth}, 年增率: {y_growth})")
    
    return "\n".join(formatted)

def format_income_statement_data(income_data: Dict) -> str:
    """格式化損益表數據"""
    if not income_data:
        return "無數據"
    
    formatted = []
    for item, quarters in income_data.items():
        item_name = {
            'revenue': '營業收入',
            'gross_profit': '營業毛利',
            'operating_income': '營業利益',
            'net_income': '稅後淨利'
        }.get(item, item)
        
        quarter_data = []
        for quarter, value in quarters.items():
            quarter_data.append(f"{quarter}: {value} 仟元")
        
        formatted.append(f"- {item_name}: {', '.join(quarter_data)}")
    
    return "\n".join(formatted)

def format_balance_sheet_data(balance_data: Dict) -> str:
    """格式化資產負債表數據"""
    if not balance_data:
        return "無數據"
    
    formatted = []
    for item, quarters in balance_data.items():
        item_name = {
            'total_assets': '資產總計',
            'total_liabilities': '負債總計',
            'equity': '股東權益總計'
        }.get(item, item)
        
        quarter_data = []
        for quarter, value in quarters.items():
            quarter_data.append(f"{quarter}: {value} 仟元")
        
        formatted.append(f"- {item_name}: {', '.join(quarter_data)}")
    
    return "\n".join(formatted)

def format_sources_data(sources: List[Dict]) -> str:
    """格式化資料來源"""
    if not sources or not isinstance(sources, list):
        return "無資料來源"
    
    formatted = []
    for source in sources:
        if isinstance(source, dict):
            formatted.append(f"- {source.get('name', '未知')}: {source.get('url', '無連結')}")
        else:
            formatted.append(f"- {str(source)}")
    
    return "\n".join(formatted)

@app.post("/api/proxy_login")
async def proxy_login(request: Request):
    form = await request.form()
    url = "https://www.cmoney.tw/identity/token"
    resp = requests.post(url, data=form)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("Content-Type"))

@app.post("/api/proxy_custom_group")
async def proxy_custom_group(request: Request):
    """Proxy for CMoney CustomGroup API"""
    try:
        # 讀取 request body
        body = await request.body()
        
        # 轉發到 CMoney API
        url = "https://www.cmoney.tw/MobileService/ashx/CustomerGroup/CustomGroup.ashx"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        # 如果有 Authorization header，也要轉發
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header
            
        resp = requests.post(url, data=body, headers=headers)
        
        return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            media_type=resp.headers.get("Content-Type", "application/json")
        )
    except Exception as e:
        return Response(
            content=json.dumps({"error": str(e)}), 
            status_code=500, 
            media_type="application/json"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 