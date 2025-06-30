"""
模板映射模組
"""

from typing import List, Dict

# 模板映射配置
TEMPLATE_MAPPING = {
    "個股分析": {
        "籌碼": {
            "table_id": "735975",
            "description": "籌碼面分析"
        },
        "技術": {
            "table_id": "736028", 
            "description": "技術面分析"
        },
        "基本面": {
            "table_id": "778132",
            "description": "基本面分析"
        }
    },
    "個股比較": {
        "籌碼": {
            "table_id": "778134",
            "description": "籌碼面比較"
        },
        "技術": {
            "table_id": "101779692",
            "description": "技術面比較"
        },
        "基本面": {
            "table_id": "101779729",
            "description": "基本面比較"
        }
    },
    "大盤分析": {
        "籌碼": {
            "table_id": "101780120",
            "description": "大盤籌碼分析"
        },
        "技術": {
            "table_id": "101780121",
            "description": "大盤技術分析"
        }
    },
    "產業分析": {
        "籌碼": {
            "table_id": "101300620",
            "description": "產業籌碼分析"
        },
        "技術": {
            "table_id": "101780872",
            "description": "產業技術分析"
        }
    }
}

def get_table_id(intent_category: str, investment_aspect: str) -> str:
    """
    根據意圖類別和投資面向取得 table_id
    
    Args:
        intent_category: 意圖類別
        investment_aspect: 投資面向
        
    Returns:
        str: table_id
    """
    if intent_category in TEMPLATE_MAPPING:
        if investment_aspect in TEMPLATE_MAPPING[intent_category]:
            return TEMPLATE_MAPPING[intent_category][investment_aspect]["table_id"]
    
    # 預設返回籌碼分析
    return "735975"

def build_api_url(table_id: str, stock_ids: List[str], additional_params: str = "") -> str:
    """
    建立 CMoney API URL
    
    Args:
        table_id: 表格ID
        stock_ids: 股票代號列表
        additional_params: 額外參數
        
    Returns:
        str: API URL
    """
    base_url = "https://www.cmoney.tw/MobileService/ashx/GetDtnoData.ashx"
    
    # 建立股票代號參數
    stock_param = ""
    if stock_ids:
        stock_param = f"AssignID={','.join(stock_ids)};"
    
    # 組合參數
    param_str = f"{stock_param}{additional_params}"
    
    # 建立完整 URL
    url = f"{base_url}?action=getdtnodata&DtNo={table_id}&ParamStr={param_str}&AssignSPID=&KeyMap=&FilterNo=0"
    
    return url

def get_available_templates() -> Dict:
    """
    取得可用的模板列表
    
    Returns:
        Dict: 模板配置
    """
    return TEMPLATE_MAPPING

def validate_template(intent_category: str, investment_aspect: str) -> bool:
    """
    驗證模板是否存在
    
    Args:
        intent_category: 意圖類別
        investment_aspect: 投資面向
        
    Returns:
        bool: 是否有效
    """
    return (intent_category in TEMPLATE_MAPPING and 
            investment_aspect in TEMPLATE_MAPPING[intent_category]) 