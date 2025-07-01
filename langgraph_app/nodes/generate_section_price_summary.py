import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from finlab import data

def generate_price_summary_section(stock_list: List[int]) -> Dict[str, Any]:
    """
    產生股價摘要 section，計算報酬率並輸出表格
    
    Args:
        stock_list: 自選股清單 (數字 list)
    
    Returns:
        Dict 包含 success 和 section 資訊
    """
    try:
        print(f"[DEBUG] 開始產生股價摘要，股票清單: {stock_list}")
        
        # 確保 finlab 已登入
        try:
            import finlab
            api_token = 'AOl10aUjuRAwxdHjbO25jGoH7c8LOhXqKz/HgT9WlcCPkBwL8Qp6PDlqpd59YuR7#vip_m'
            finlab.login(api_token=api_token)
            
            # 測試 finlab 連線
            test_data = data.get('price:收盤價')
            print(f"[DEBUG] Finlab 連線成功，price:收盤價 shape: {test_data.shape}")
        except Exception as e:
            print(f"[ERROR] Finlab 連線失敗: {e}")
            return {
                "success": False,
                "error": f"Finlab 連線失敗: {e}"
            }
        
        # 取得收盤價資料
        close_data = data.get('price:收盤價')
        print(f"[DEBUG] 取得收盤價資料，shape: {close_data.shape}")
        
        # 取得公司基本資訊（用於取得公司名稱）
        basic_info = data.get('company_basic_info')
        
        # 將 stock_list 轉為字串，用於比對
        stock_list_str = [str(stock_id) for stock_id in stock_list]
        print(f"[DEBUG] 轉換後的股票代號: {stock_list_str}")
        
        # 過濾出有資料的股票
        available_stocks = [stock for stock in stock_list_str if stock in close_data.columns]
        print(f"[DEBUG] 有收盤價資料的股票: {available_stocks}")
        
        if len(available_stocks) == 0:
            return {
                "success": False,
                "error": "找不到指定股票的收盤價資料"
            }
        
        # 計算報酬率
        price_summary_data = []
        
        for stock_id in available_stocks:
            try:
                # 取得該股票的收盤價序列
                stock_prices = close_data[stock_id].dropna()
                
                if len(stock_prices) < 20:  # 至少要有20天資料
                    print(f"[WARNING] 股票 {stock_id} 資料不足，跳過")
                    continue
                
                # 取得最新日期和歷史日期
                latest_date = stock_prices.index[-1]
                latest_price = stock_prices.iloc[-1]

                def get_price_n_days_ago(prices, n):
                    if len(prices) > n:
                        return prices.iloc[-n-1]
                    return None

                price_1d_ago = get_price_n_days_ago(stock_prices, 1)
                price_1w_ago = get_price_n_days_ago(stock_prices, 5)
                price_1m_ago = get_price_n_days_ago(stock_prices, 20)
                price_1y_ago = get_price_n_days_ago(stock_prices, 240)

                def calc_change(now, before):
                    if now is not None and before is not None and before != 0:
                        return (now - before) / before * 100
                    return None

                change_1d = calc_change(latest_price, price_1d_ago)
                change_1w = calc_change(latest_price, price_1w_ago)
                change_1m = calc_change(latest_price, price_1m_ago)
                change_1y = calc_change(latest_price, price_1y_ago)

                # 計算各期間報酬率
                returns = {}
                periods = [1, 5, 20, 60, 240]
                
                for period in periods:
                    if len(stock_prices) > period:
                        historical_price = stock_prices.iloc[-period-1]
                        if historical_price != 0:
                            return_rate = (latest_price - historical_price) / historical_price * 100
                            returns[f"{period}日報酬"] = return_rate
                        else:
                            returns[f"{period}日報酬"] = 0
                    else:
                        returns[f"{period}日報酬"] = None
                
                # 取得公司名稱
                company_name = "未知"
                if stock_id in basic_info['stock_id'].values:
                    company_row = basic_info[basic_info['stock_id'] == stock_id]
                    if len(company_row) > 0:
                        company_name = company_row.iloc[0].get('公司簡稱', company_row.iloc[0].get('公司名稱', '未知'))
                
                # 建立股票資料
                stock_data = {
                    "stock_id": stock_id,
                    "company_name": company_name,
                    "close": latest_price,
                    "close_date": str(latest_date)[:10],
                    "change_1d": change_1d,
                    "change_1w": change_1w,
                    "change_1m": change_1m,
                    "change_1y": change_1y,
                    **returns
                }
                price_summary_data.append(stock_data)
                
            except Exception as e:
                print(f"[ERROR] 處理股票 {stock_id} 時發生錯誤: {e}")
                continue
        
        if len(price_summary_data) == 0:
            return {
                "success": False,
                "error": "無法計算任何股票的報酬率"
            }
        
        # 建立表格內容
        table_content = "股價摘要（變動趨勢）\n\n"
        table_content += "統計區間：1日 / 5日 / 20日 / 60日 / 240日 報酬率\n"
        table_content += "股票代號\t公司名稱\t1日報酬\t5日報酬\t20日報酬\t60日報酬\t240日報酬\n"
        
        for stock_data in price_summary_data:
            table_content += f"{stock_data['stock_id']}\t{stock_data['company_name']}\t"
            
            # 格式化報酬率
            for period in ["1日報酬", "5日報酬", "20日報酬", "60日報酬", "240日報酬"]:
                if stock_data[period] is not None:
                    sign = "+" if stock_data[period] >= 0 else ""
                    table_content += f"{sign}{stock_data[period]:.1f}%\t"
                else:
                    table_content += "N/A\t"
            
            table_content += "\n"
        
        # 建立 section 結構
        section = {
            "title": "股價摘要",
            "content": table_content,
            "cards": [
                {
                    "title": "股價變動趨勢",
                    "content": table_content,
                    "type": "table",
                    "data": price_summary_data  # 原始資料供前端使用
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
        
        # 調試：檢查 section 結構
        print(f"[DEBUG] 股價摘要 section 結構:")
        print(f"[DEBUG] cards[0].type: {section['cards'][0]['type']}")
        print(f"[DEBUG] cards[0].data 存在: {'data' in section['cards'][0]}")
        print(f"[DEBUG] cards[0].data 長度: {len(section['cards'][0]['data']) if 'data' in section['cards'][0] else 'N/A'}")
        print(f"[DEBUG] cards[0].data 範例: {section['cards'][0]['data'][0] if 'data' in section['cards'][0] and len(section['cards'][0]['data']) > 0 else 'N/A'}")
        
        print(f"[DEBUG] 股價摘要 section 建立完成，包含 {len(price_summary_data)} 檔股票")
        return {
            "success": True,
            "section": section,
            "price_data": price_summary_data  # 額外回傳供其他 section 使用
        }
        
    except Exception as e:
        print(f"[ERROR] 產生股價摘要時發生錯誤: {e}")
        return {
            "success": False,
            "error": f"產生股價摘要時發生錯誤: {e}"
        }

# 測試用
if __name__ == "__main__":
    test_stock_list = [2303, 2330]
    result = generate_price_summary_section(test_stock_list)
    print(json.dumps(result, ensure_ascii=False, indent=2)) 