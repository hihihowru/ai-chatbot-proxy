import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List

def generate_return_analysis_section(price_data: List[Dict]) -> Dict[str, Any]:
    """
    產生報酬率統計分析 section
    
    Args:
        price_data: 股價摘要資料（來自 generate_price_summary_section）
    
    Returns:
        Dict 包含 success 和 section 資訊
    """
    try:
        print(f"[DEBUG] 開始產生報酬率統計分析，股票數量: {len(price_data)}")
        
        if not price_data:
            return {
                "success": False,
                "error": "沒有股價資料可供分析"
            }
        
        # 分析各期間的統計資料
        analysis_results = {}
        periods = ["1日報酬", "5日報酬", "20日報酬"]
        
        for period in periods:
            # 收集該期間的有效報酬率資料
            valid_returns = []
            for stock in price_data:
                if stock.get(period) is not None:
                    valid_returns.append(stock[period])
            
            if valid_returns:
                valid_returns = np.array(valid_returns)
                
                # 計算統計資料
                up_count = np.sum(valid_returns > 0)
                down_count = np.sum(valid_returns < 0)
                flat_count = np.sum(valid_returns == 0)
                avg_return = np.mean(valid_returns)
                max_return = np.max(valid_returns)
                min_return = np.min(valid_returns)
                
                # 找出最大漲幅和最大跌幅的股票
                max_stock = None
                min_stock = None
                
                for stock in price_data:
                    if stock.get(period) is not None:
                        if stock[period] == max_return:
                            max_stock = stock
                        if stock[period] == min_return:
                            min_stock = stock
                
                analysis_results[period] = {
                    "up_count": int(up_count),
                    "down_count": int(down_count),
                    "flat_count": int(flat_count),
                    "avg_return": float(avg_return),
                    "max_return": float(max_return),
                    "min_return": float(min_return),
                    "max_stock": max_stock,
                    "min_stock": min_stock,
                    "total_count": len(valid_returns)
                }
        
        # 建立分析內容
        analysis_content = "📊 報酬率統計分析\n"
        
        # 1日報酬分析
        if "1日報酬" in analysis_results:
            day1 = analysis_results["1日報酬"]
            analysis_content += f"\t•\t**過去一日：**上漲 {day1['up_count']} 檔，下跌 {day1['down_count']} 檔\n"
        
        # 5日報酬分析（一週）
        if "5日報酬" in analysis_results:
            day5 = analysis_results["5日報酬"]
            analysis_content += f"\t•\t平均一週漲幅：{day5['avg_return']:+.1f}%\n"
            
            if day5['max_stock']:
                analysis_content += f"\t•\t**最大漲幅：**{day5['max_stock']['company_name']}（{day5['max_return']:+.1f}%，5 日）\n"
        
        # 20日報酬分析
        if "20日報酬" in analysis_results:
            day20 = analysis_results["20日報酬"]
            if day20['max_stock']:
                analysis_content += f"\t•\t**最大漲幅：**{day20['max_stock']['company_name']}（{day20['max_return']:+.1f}%，20 日）\n"
        
        # 建立詳細統計表格
        table_content = "報酬率統計詳情\n\n"
        table_content += "期間\t上漲檔數\t下跌檔數\t平均報酬\t最大漲幅\t最大跌幅\n"
        
        for period in periods:
            if period in analysis_results:
                data = analysis_results[period]
                period_name = period.replace("日報酬", "日")
                table_content += f"{period_name}\t{data['up_count']}\t{data['down_count']}\t{data['avg_return']:+.1f}%\t{data['max_return']:+.1f}%\t{data['min_return']:+.1f}%\n"
        
        # 建立 section 結構
        section = {
            "title": "報酬率統計分析",
            "content": analysis_content,
            "cards": [
                {
                    "title": "報酬率統計",
                    "content": analysis_content,
                    "type": "text"
                },
                {
                    "title": "詳細統計表格",
                    "content": table_content,
                    "type": "table",
                    "data": analysis_results
                }
            ],
            "sources": [
                {
                    "name": "Finlab 收盤價資料",
                    "url": "https://finlab.tw/",
                    "description": "台股收盤價歷史資料"
                }
            ]
        }
        
        print(f"[DEBUG] 報酬率統計分析 section 建立完成")
        return {
            "success": True,
            "section": section,
            "analysis_data": analysis_results
        }
        
    except Exception as e:
        print(f"[ERROR] 產生報酬率統計分析時發生錯誤: {e}")
        return {
            "success": False,
            "error": f"產生報酬率統計分析時發生錯誤: {e}"
        } 