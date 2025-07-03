import pandas as pd
import numpy as np
from finlab import data
from typing import List, Dict, Any

def generate_industry_comparison_section(stock_list: List[int]) -> Dict[str, Any]:
    try:
        company_info = data.get('company_basic_info').set_index('stock_id')
        close = data.get('price:收盤價')
        index_price = data.get('stock_index_price:收盤指數')
        periods = ['1日報酬','5日報酬','20日報酬','60日報酬','240日報酬']
        def get_industry(stock_id):
            try:
                industry = company_info.loc[stock_id, '產業類別']
                if pd.isna(industry):
                    return '無對應'
                if industry == '水泥工業':
                    return '水泥'
                if industry == '食品工業':
                    return '食品'
                if industry.endswith('工業'):
                    return '無對應'
                if industry.endswith('業'):
                    industry = industry[:-1]
                return industry
            except Exception:
                return '無對應'
        def get_index_col(industry):
            if industry == '無對應':
                return '無對應'
            col = f'上市{industry}類指數'
            if col in index_price.columns:
                return col
            else:
                return '無對應'
        def calc_return(series, periods=periods):
            returns = {}
            for p in periods:
                try:
                    n = int(p.split('日')[0])
                except Exception:
                    returns[f'{p}'] = None
                    continue
                if len(series) < n+1 or series.isnull().any():
                    returns[f'{p}'] = None
                else:
                    ret = (series.iloc[-1] / series.iloc[-(n+1)] - 1) * 100
                    returns[f'{p}'] = round(ret, 2)
            return returns
        print(f"[DEBUG] index_price.columns: {list(index_price.columns)}")
        result = []
        for stock_id in stock_list:
            stock_id_str = str(stock_id)
            industry = get_industry(stock_id_str)
            index_col = get_index_col(industry)
            print(f"[DEBUG] {stock_id_str}: 產業={industry}, 指數欄位={index_col}")
            stock_name = company_info.loc[stock_id_str, '公司名稱'] if stock_id_str in company_info.index else stock_id_str
            stock_close = close[stock_id_str].dropna() if stock_id_str in close.columns else pd.Series(dtype=float)
            stock_ret = calc_return(stock_close)
            if index_col != '無對應':
                ind_close = index_price[index_col].dropna()
                ind_ret = calc_return(ind_close)
            else:
                ind_ret = {k: None for k in periods}
            lead_lag = {}
            for p in periods:
                if stock_ret[p] is None or ind_ret[p] is None:
                    lead_lag[p] = '無對應'
                elif stock_ret[p] > ind_ret[p]:
                    lead_lag[p] = '領先'
                elif stock_ret[p] < ind_ret[p]:
                    lead_lag[p] = '落後'
                else:
                    lead_lag[p] = '持平'
            result.append({
                '股票代號': stock_id_str,
                '公司名稱': stock_name,
                '產業類別': industry,
                '產業指數': index_col,
                **{f'個股{p}': stock_ret[p] for p in periods},
                **{f'產業{p}': ind_ret[p] for p in periods},
                **{f'領先狀態{p}': lead_lag[p] for p in periods}
            })
        section = {
            "title": "自選股 vs 同產業指數表現",
            "content": "下表比較你的自選股與同產業指數在不同期間的報酬率，幫助你判斷個股在同產業中的相對表現。若產業指數無對應，則顯示『無對應』。領先：個股報酬率高於產業指數；落後：低於產業指數；持平：相同。",
            "cards": [
                {
                    "type": "table",
                    "title": "自選股 vs 同產業指數表現",
                    "content": "自選股與同產業指數各期間報酬率對比表",
                    "data": result
                }
            ],
            "sources": [
                {
                    "name": "Finlab 指數資料",
                    "url": "https://finlab.tw/",
                    "description": "台股產業指數與公司基本資料"
                }
            ]
        }
        return {"success": True, "section": section}
    except Exception as e:
        return {"success": False, "error": str(e)} 