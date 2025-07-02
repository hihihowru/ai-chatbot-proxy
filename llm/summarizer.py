# pip install langgraph openai
from langgraph.graph import StateGraph, END
from typing import Dict, Any

def llm_node(state: Dict[str, Any]) -> Dict[str, Any]:
    question = state["question"]
    stockId = state["stockId"]
    role = state["role"]
    # 這裡可串接 OpenAI API，暫時回傳 mock
    # response = openai.ChatCompletion.create(...)
    return {
        "summaryCards": [
            {"type": "新聞", "title": "聯電爆量漲停", "content": f"{question} 的新聞摘要內容..."},
            {"type": "技術", "title": "均線黃金交叉", "content": f"{question} 的技術分析內容..."}
        ]
    }

def summarize_with_llm(question, stockId, role):
    # 創建狀態圖
    workflow = StateGraph(Dict[str, Any])
    
    # 添加節點
    workflow.add_node("llm", llm_node)
    
    # 設置入口點和結束點
    workflow.set_entry_point("llm")
    workflow.add_edge("llm", END)
    
    # 編譯圖
    app = workflow.compile()
    
    # 運行
    result = app.invoke({"question": question, "stockId": stockId, "role": role})
    return result["summaryCards"] 