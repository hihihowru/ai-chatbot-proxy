import json
import pandas as pd
import os
from typing import Dict, Any, List
from finlab import data

def generate_industry_distribution_section(stock_list: List[int]) -> Dict[str, Any]:
    """
    產生產業分布統計 section
    
    Args:
        stock_list: 自選股清單 (數字 list)
    
    Returns:
        Dict 包含 success 和 section 資訊
    """
    try:
        print(f"[DEBUG] 開始產生產業分布統計，股票清單: {stock_list}")
        
        # 確保 finlab 已登入
        try:
            import finlab
            api_token = 'AOl10aUjuRAwxdHjbO25jGoH7c8LOhXqKz/HgT9WlcCPkBwL8Qp6PDlqpd59YuR7#vip_m'
            finlab.login(api_token=api_token)
            
            # 測試 finlab 連線
            test_data = data.get('company_basic_info')
            print(f"[DEBUG] Finlab 連線成功，company_basic_info shape: {test_data.shape}")
        except Exception as e:
            print(f"[ERROR] Finlab 連線失敗: {e}")
            return {
                "success": False,
                "error": f"Finlab 連線失敗: {e}"
            }
        
        # 取得公司基本資訊
        basic_info = data.get('company_basic_info')
        print(f"[DEBUG] 取得 company_basic_info，shape: {basic_info.shape}")
        
        # 將 stock_list 轉為字串，用於比對
        stock_list_str = [str(stock_id) for stock_id in stock_list]
        print(f"[DEBUG] 轉換後的股票代號: {stock_list_str}")
        
        # 過濾出自選股的公司資訊
        filtered_info = basic_info[basic_info['stock_id'].isin(stock_list_str)]
        print(f"[DEBUG] 過濾後的公司數量: {len(filtered_info)}")
        
        if len(filtered_info) == 0:
            return {
                "success": False,
                "error": "找不到指定的股票資訊"
            }
        
        # 統計產業分布
        industry_counts = filtered_info['產業類別'].value_counts()
        print(f"[DEBUG] 產業分布統計: {industry_counts.to_dict()}")
        
        # 建立產業分布內容
        industry_content = "🏷️ 產業分布統計\n"
        for industry, count in industry_counts.items():
            industry_content += f"\t•\t{industry}：{count} 檔\n"
        
        # 建立 section 結構
        section = {
            "title": "產業分布統計",
            "content": industry_content,
            "cards": [
                {
                    "title": "產業分布",
                    "content": industry_content,
                    "type": "text"
                }
            ],
            "sources": [
                {
                    "name": "Finlab 公司基本資訊",
                    "url": "https://finlab.tw/",
                    "description": "公司產業分類資料"
                }
            ]
        }
        
        print(f"[DEBUG] 產業分布統計 section 建立完成")
        return {
            "success": True,
            "section": section
        }
        
    except Exception as e:
        print(f"[ERROR] 產生產業分布統計時發生錯誤: {e}")
        return {
            "success": False,
            "error": f"產生產業分布統計時發生錯誤: {e}"
        } 