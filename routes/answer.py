from fastapi import APIRouter, Form, Header
from typing import Optional
import sys
import os

# 添加專案根目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from schemas import AnswerRequest, AnswerResponse, WatchlistRequest, WatchlistResponse
    from utils.log_generator import generate_logs
    from llm.summarizer import summarize_with_llm
    from langgraph_app.nodes.generate_watchlist_summary_pipeline import generate_watchlist_summary_pipeline
except ImportError as e:
    print(f"Import error: {e}")
    # 如果相對導入失敗，嘗試絕對導入
    sys.path.append(os.path.join(project_root, '..'))
    from schemas import AnswerRequest, AnswerResponse, WatchlistRequest, WatchlistResponse
    from utils.log_generator import generate_logs
    from llm.summarizer import summarize_with_llm
    from langgraph_app.nodes.generate_watchlist_summary_pipeline import generate_watchlist_summary_pipeline

import httpx

router = APIRouter()

@router.post("/answer", response_model=AnswerResponse)
async def answer(req: AnswerRequest):
    logs = list(generate_logs())
    summary_cards = summarize_with_llm(req.question, req.stockId, req.role)
    return AnswerResponse(
        logs=logs,
        summaryCards=summary_cards
    )

@router.post("/watchlist-summary", response_model=WatchlistResponse)
async def watchlist_summary(req: WatchlistRequest):
    """
    產生自選股摘要
    """
    try:
        print(f"[DEBUG] 收到自選股摘要請求，股票清單: {req.stock_list}")
        print(f"[DEBUG] 用戶ID: {req.userId}")
        
        # 讀取股票別名字典來轉換股票代號為中文名稱
        try:
            import json
            with open('data/stock_alias_dict.json', 'r', encoding='utf-8') as f:
                stock_alias_dict = json.load(f)
            
            stock_names = []
            for stock_id in req.stock_list:
                stock_id_str = str(stock_id)
                if stock_id_str in stock_alias_dict and stock_alias_dict[stock_id_str]:
                    stock_names.append(f"{stock_id_str} {stock_alias_dict[stock_id_str][0]}")
                else:
                    stock_names.append(stock_id_str)
            
            print(f"[DEBUG] 股票清單（含中文名稱）: {stock_names}")
        except Exception as e:
            print(f"[WARNING] 無法讀取股票別名字典: {e}")
            stock_names = [str(stock_id) for stock_id in req.stock_list]
        
        # 調用自選股摘要 pipeline
        result = generate_watchlist_summary_pipeline(req.stock_list)
        
        if result.get("success"):
            return WatchlistResponse(
                success=True,
                sections=result["sections"],
                logs=result["logs"]
            )
        else:
            return WatchlistResponse(
                success=False,
                sections=[],
                logs=result.get("logs", []),
                error=result.get("error", "未知錯誤")
            )
            
    except Exception as e:
        print(f"[ERROR] 自選股摘要處理時發生錯誤: {e}")
        return WatchlistResponse(
            success=False,
            sections=[],
            logs=[],
            error=f"處理時發生錯誤: {e}"
        )

@router.post("/login")
async def login(
    grant_type: str = Form(...),
    login_method: str = Form(...),
    client_id: str = Form(...),
    account: str = Form(...),
    password: str = Form(...)
):
    """
    呼叫 CMoney 會員登入 API
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://www.cmoney.tw/member/api/v1.0/Token",
                data={
                    "grant_type": grant_type,
                    "login_method": login_method,
                    "client_id": client_id,
                    "account": account,
                    "password": password
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            return resp.json(), resp.status_code
    except Exception as e:
        print(f"[ERROR] 登入處理時發生錯誤: {e}")
        return {
            "error": "internal_server_error",
            "error_description": "登入失敗"
        }, 500

@router.post("/custom-group")
async def custom_group(
    Action: str = Form(...),
    docType: str = Form(...),
    authorization: Optional[str] = Header(None)
):
    """
    取得自選股群組
    """
    try:
        print(f"[DEBUG] 收到自選股群組請求: {Action}, {docType}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://www.cmoney.tw/member/api/v1.0/CustomGroup",
                data={
                    "Action": Action,
                    "docType": docType
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": authorization or ""
                }
            )
            return resp.json(), resp.status_code
    except Exception as e:
        print(f"[ERROR] 自選股群組處理時發生錯誤: {e}")
        return {
            "error": "internal_server_error",
            "error_description": "取得自選股群組時發生錯誤"
        }, 500 