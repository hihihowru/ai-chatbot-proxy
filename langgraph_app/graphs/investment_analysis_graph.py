from langgraph.graph import StateGraph, END
from typing import Dict, List, Any, TypedDict
import json
import sys
import os

# 添加父目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 定義狀態結構
class AnalysisState(TypedDict):
    user_input: str
    intent: str
    keywords: List[str]
    company_name: str
    stock_id: str
    time_info: str
    event_type: str
    search_keywords: List[str]
    search_results: List[Dict]
    summary: str
    summary_points: List[str]
    report: str
    report_sections: List[str]
    logs: List[str]
    error: str

def create_investment_analysis_graph():
    """建立投資分析圖表"""
    
    # 建立狀態圖
    workflow = StateGraph(AnalysisState)
    
    # 添加節點
    workflow.add_node("classify_and_extract", classify_and_extract_node)
    workflow.add_node("search_news", search_news_node)
    workflow.add_node("summarize_results", summarize_results_node)
    workflow.add_node("generate_report", generate_report_node)
    
    # 設定入口點
    workflow.set_entry_point("classify_and_extract")
    
    # 設定邊緣
    workflow.add_edge("classify_and_extract", "search_news")
    workflow.add_edge("search_news", "summarize_results")
    workflow.add_edge("summarize_results", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()

def classify_and_extract_node(state: AnalysisState) -> AnalysisState:
    """問題理解節點"""
    try:
        from langgraph_app.nodes.classify_and_extract import classify_and_extract
        
        # 添加日誌
        logs = state.get("logs", [])
        logs.append("🔍 開始問題理解與分類...")
        
        # 執行分類和提取
        result = classify_and_extract(state["user_input"])
        
        # 更新狀態
        return {
            **state,
            "intent": result.get("intent", ""),
            "keywords": result.get("keywords", []),
            "company_name": result.get("company_name", ""),
            "stock_id": result.get("stock_id", ""),
            "time_info": result.get("time_info", ""),
            "event_type": result.get("event_type", ""),
            "logs": logs + [f"✅ 問題理解完成：{result.get('intent', '')} | {result.get('company_name', '')}({result.get('stock_id', '')})"]
        }
        
    except Exception as e:
        logs = state.get("logs", [])
        logs.append(f"❌ 問題理解失敗: {str(e)}")
        return {
            **state,
            "error": f"問題理解失敗: {str(e)}",
            "logs": logs
        }

def search_news_node(state: AnalysisState) -> AnalysisState:
    """新聞搜尋節點"""
    try:
        from langgraph_app.nodes.search_news import search_news
        
        # 添加日誌
        logs = state.get("logs", [])
        logs.append("🔎 開始搜尋相關新聞...")
        
        # 執行搜尋
        result = search_news(
            company_name=state.get("company_name", ""),
            stock_id=state.get("stock_id", ""),
            intent=state.get("intent", ""),
            keywords=state.get("keywords", [])
        )
        
        # 更新狀態
        return {
            **state,
            "search_keywords": result.get("search_keywords", []),
            "search_results": result.get("results", []),
            "logs": logs + [f"✅ 新聞搜尋完成：找到 {len(result.get('results', []))} 個結果"]
        }
        
    except Exception as e:
        logs = state.get("logs", [])
        logs.append(f"❌ 新聞搜尋失敗: {str(e)}")
        return {
            **state,
            "error": f"新聞搜尋失敗: {str(e)}",
            "logs": logs
        }

def summarize_results_node(state: AnalysisState) -> AnalysisState:
    """結果摘要節點"""
    try:
        from langgraph_app.nodes.summarize_results import summarize_results
        
        # 添加日誌
        logs = state.get("logs", [])
        logs.append("📝 開始摘要搜尋結果...")
        
        # 執行摘要
        result = summarize_results(
            search_results=state.get("search_results", []),
            company_name=state.get("company_name", ""),
            stock_id=state.get("stock_id", "")
        )
        
        # 更新狀態
        return {
            **state,
            "summary": result.get("summary", ""),
            "summary_points": result.get("summary_points", []),
            "logs": logs + ["✅ 結果摘要完成"]
        }
        
    except Exception as e:
        logs = state.get("logs", [])
        logs.append(f"❌ 結果摘要失敗: {str(e)}")
        return {
            **state,
            "error": f"結果摘要失敗: {str(e)}",
            "logs": logs
        }

def generate_report_node(state: AnalysisState) -> AnalysisState:
    """報告生成節點"""
    try:
        from langgraph_app.nodes.generate_report import generate_report
        
        # 添加日誌
        logs = state.get("logs", [])
        logs.append("📊 開始生成投資分析報告...")
        
        # 執行報告生成
        result = generate_report(
            company_name=state.get("company_name", ""),
            stock_id=state.get("stock_id", ""),
            user_input=state.get("user_input", ""),
            summary_points=state.get("summary_points", [])
        )
        
        # 更新狀態
        return {
            **state,
            "report": result.get("report", ""),
            "report_sections": result.get("report_sections", []),
            "logs": logs + ["✅ 投資分析報告生成完成"]
        }
        
    except Exception as e:
        logs = state.get("logs", [])
        logs.append(f"❌ 報告生成失敗: {str(e)}")
        return {
            **state,
            "error": f"報告生成失敗: {str(e)}",
            "logs": logs
        }

# 建立圖表實例
investment_analysis_graph = create_investment_analysis_graph()

def run_analysis(user_input: str) -> Dict[str, Any]:
    """執行完整的投資分析流程"""
    try:
        # 初始化狀態
        initial_state: AnalysisState = {
            "user_input": user_input,
            "intent": "",
            "keywords": [],
            "company_name": "",
            "stock_id": "",
            "time_info": "",
            "event_type": "",
            "search_keywords": [],
            "search_results": [],
            "summary": "",
            "summary_points": [],
            "report": "",
            "report_sections": [],
            "logs": [],
            "error": ""
        }
        
        # 執行圖表
        result = investment_analysis_graph.invoke(initial_state)
        
        # 轉換為字典格式
        return {
            "success": True,
            "user_input": result.get("user_input", ""),
            "intent": result.get("intent", ""),
            "company_name": result.get("company_name", ""),
            "stock_id": result.get("stock_id", ""),
            "time_info": result.get("time_info", ""),
            "event_type": result.get("event_type", ""),
            "search_keywords": result.get("search_keywords", []),
            "search_results": result.get("search_results", []),
            "summary": result.get("summary", ""),
            "summary_points": result.get("summary_points", []),
            "report": result.get("report", ""),
            "report_sections": result.get("report_sections", []),
            "logs": result.get("logs", []),
            "error": result.get("error", "")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"分析流程執行失敗: {str(e)}",
            "logs": [f"❌ 系統錯誤: {str(e)}"]
        }

# 測試用
if __name__ == "__main__":
    test_input = "華碩前天漲停板但今天下跌，是什麼原因"
    result = run_analysis(test_input)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 