"""
資料庫查詢模組
"""

import requests
import json
from typing import List, Dict, Any
from .template_mapping import get_table_id, build_api_url, validate_template

class DatabaseQuery:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.cmoney.tw/",
            "Accept": "application/json",
        }
    
    def test_table_id(self, table_id: str, stock_id: str = "2330") -> Dict[str, Any]:
        """
        測試單一 table_id 是否有效
        
        Args:
            table_id: 要測試的 table_id
            stock_id: 測試用的股票代號
            
        Returns:
            Dict: 測試結果
        """
        try:
            # 建立 API URL
            url = build_api_url(table_id, [stock_id], "MTPeriod=0;DTMode=0;DTRange=5;DTOrder=1;MajorTable=M173;")
            
            # 發送請求
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return {
                        "table_id": table_id,
                        "status": "success",
                        "has_data": bool(data.get("Data")),
                        "data_count": len(data.get("Data", [])),
                        "title": data.get("Title", []),
                        "url": url
                    }
                except json.JSONDecodeError:
                    return {
                        "table_id": table_id,
                        "status": "error",
                        "error": "JSON 解析失敗",
                        "url": url
                    }
            else:
                return {
                    "table_id": table_id,
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "url": url
                }
                
        except Exception as e:
            return {
                "table_id": table_id,
                "status": "error",
                "error": str(e),
                "url": url if 'url' in locals() else "N/A"
            }
    
    def test_table_ids(self, table_ids: List[str], stock_id: str = "2330") -> List[Dict[str, Any]]:
        """
        測試多個 table_id 是否有效
        
        Args:
            table_ids: 要測試的 table_id 列表
            stock_id: 測試用的股票代號
            
        Returns:
            List[Dict]: 測試結果列表
        """
        results = []
        for table_id in table_ids:
            result = self.test_table_id(table_id, stock_id)
            results.append(result)
        return results
    
    def query_data(self, intent_category: str, investment_aspect: str, stock_ids: List[str]) -> Dict[str, Any]:
        """
        根據意圖和股票代號查詢資料
        
        Args:
            intent_category: 意圖類別
            investment_aspect: 投資面向
            stock_ids: 股票代號列表
            
        Returns:
            Dict: 查詢結果
        """
        # 驗證模板
        if not validate_template(intent_category, investment_aspect):
            return {
                "success": False,
                "error": f"不支援的模板: {intent_category} - {investment_aspect}"
            }
        
        # 取得 table_id
        table_id = get_table_id(intent_category, investment_aspect)
        
        try:
            # 建立 API URL
            url = build_api_url(table_id, stock_ids, "MTPeriod=0;DTMode=0;DTRange=5;DTOrder=1;MajorTable=M173;")
            
            # 發送請求
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return {
                        "success": True,
                        "data": data,
                        "table_id": table_id,
                        "intent_category": intent_category,
                        "investment_aspect": investment_aspect,
                        "stock_ids": stock_ids,
                        "url": url
                    }
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "JSON 解析失敗",
                        "url": url
                    }
            else:
                return {
                    "success": False,
                    "error": f"API 請求失敗: {response.status_code}",
                    "url": url
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"請求錯誤: {str(e)}",
                "url": url if 'url' in locals() else "N/A"
            }
    
    def query_by_table_id(self, table_id: str, stock_ids: List[str], additional_params: str = "") -> Dict[str, Any]:
        """
        直接使用 table_id 查詢資料
        
        Args:
            table_id: 表格ID
            stock_ids: 股票代號列表
            additional_params: 額外參數
            
        Returns:
            Dict: 查詢結果
        """
        try:
            # 建立 API URL
            url = build_api_url(table_id, stock_ids, additional_params)
            
            # 發送請求
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return {
                        "success": True,
                        "data": data,
                        "table_id": table_id,
                        "stock_ids": stock_ids,
                        "url": url
                    }
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "JSON 解析失敗",
                        "url": url
                    }
            else:
                return {
                    "success": False,
                    "error": f"API 請求失敗: {response.status_code}",
                    "url": url
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"請求錯誤: {str(e)}",
                "url": url if 'url' in locals() else "N/A"
            }

# 建立全域實例
db_query = DatabaseQuery() 