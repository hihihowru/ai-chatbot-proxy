"""
圖表偵測模組
"""

import re
from typing import Dict, List, Optional

# 圖表類型映射
CHART_MAPPING = {
    "技術分析": {
        "keywords": ["技術", "技術分析", "技術面", "技術指標", "K線", "KD", "MACD", "RSI", "布林通道", "均線"],
        "table_id": "735975"
    },
    "籌碼分析": {
        "keywords": ["籌碼", "籌碼面", "法人", "外資", "投信", "自營商", "三大法人", "融資融券", "券資比"],
        "table_id": "736028"
    },
    "基本面": {
        "keywords": ["基本面", "財務", "營收", "獲利", "EPS", "本益比", "股價淨值比", "ROE", "ROA"],
        "table_id": "778132"
    },
    "新聞": {
        "keywords": ["新聞", "消息", "公告", "財報", "法說會", "股東會"],
        "table_id": "778134"
    },
    "比較分析": {
        "keywords": ["比較", "對比", "哪個好", "哪個比較好", "優劣", "排名"],
        "table_id": "101779692"
    },
    "趨勢分析": {
        "keywords": ["趨勢", "走勢", "方向", "漲跌", "突破", "支撐", "壓力"],
        "table_id": "101779729"
    }
}

def detect_chart(question: str) -> Optional[Dict]:
    """
    從問題中偵測圖表類型
    
    Args:
        question: 使用者問題
        
    Returns:
        Optional[Dict]: 偵測結果，包含 chart_type 和 table_id
    """
    question = question.lower()
    
    # 計算每個圖表類型的匹配分數
    scores = {}
    
    for chart_type, config in CHART_MAPPING.items():
        score = 0
        for keyword in config["keywords"]:
            if keyword in question:
                score += 1
        
        if score > 0:
            scores[chart_type] = score
    
    # 如果沒有找到匹配，返回 None
    if not scores:
        return None
    
    # 選擇分數最高的圖表類型
    best_chart = max(scores.items(), key=lambda x: x[1])
    chart_type = best_chart[0]
    
    return {
        "chart_type": chart_type,
        "table_id": CHART_MAPPING[chart_type]["table_id"],
        "confidence": best_chart[1] / len(CHART_MAPPING[chart_type]["keywords"])
    }

def detect_multiple_charts(question: str) -> List[Dict]:
    """
    從問題中偵測多個圖表類型
    
    Args:
        question: 使用者問題
        
    Returns:
        List[Dict]: 偵測到的圖表類型列表
    """
    question = question.lower()
    detected_charts = []
    
    for chart_type, config in CHART_MAPPING.items():
        score = 0
        for keyword in config["keywords"]:
            if keyword in question:
                score += 1
        
        if score > 0:
            detected_charts.append({
                "chart_type": chart_type,
                "table_id": config["table_id"],
                "confidence": score / len(config["keywords"]),
                "score": score
            })
    
    # 按分數排序
    detected_charts.sort(key=lambda x: x["score"], reverse=True)
    
    return detected_charts

def get_chart_suggestions(question: str) -> List[str]:
    """
    根據問題提供圖表建議
    
    Args:
        question: 使用者問題
        
    Returns:
        List[str]: 建議的圖表類型列表
    """
    detected = detect_multiple_charts(question)
    
    if not detected:
        # 如果沒有偵測到特定圖表，提供通用建議
        return ["技術分析", "籌碼分析", "基本面"]
    
    # 返回偵測到的圖表類型
    return [chart["chart_type"] for chart in detected[:3]]  # 最多3個建議 