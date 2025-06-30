# pip install langgraph openai
import langgraph

def llm_node(state):
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
    graph = langgraph.Graph()
    graph.add_node("llm", llm_node)
    graph.set_entry_point("llm")
    result = graph.run({"question": question, "stockId": stockId, "role": role})
    return result["summaryCards"] 