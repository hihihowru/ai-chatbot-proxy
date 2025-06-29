"""
時間偵測模組
"""

import re
from datetime import datetime, timedelta

def detect_time(question: str) -> str:
    """
    從問題中偵測時間表達
    
    Args:
        question: 使用者問題
        
    Returns:
        str: 偵測到的時間表達
    """
    # 移除空白
    question = question.strip()
    
    # 時間關鍵字映射
    time_patterns = {
        r'今天|今日|本日': 'today',
        r'昨天|昨日': 'yesterday', 
        r'明天|明日': 'tomorrow',
        r'上週|上周': 'last_week',
        r'本週|本周|這週|这周': 'this_week',
        r'下週|下周': 'next_week',
        r'上個月|上月': 'last_month',
        r'這個月|这個月|本月': 'this_month',
        r'下個月|下月': 'next_month',
        r'上季|上一季': 'last_quarter',
        r'本季|這一季|这一季': 'this_quarter',
        r'下季|下一季': 'next_quarter',
        r'去年': 'last_year',
        r'今年': 'this_year',
        r'明年': 'next_year',
        r'最近(\d+)天': 'recent_days',
        r'最近(\d+)週': 'recent_weeks',
        r'最近(\d+)個月': 'recent_months',
        r'最近(\d+)年': 'recent_years',
    }
    
    # 檢查每個時間模式
    for pattern, time_type in time_patterns.items():
        match = re.search(pattern, question)
        if match:
            if time_type.startswith('recent_'):
                # 提取數字
                number = int(match.group(1))
                return f"{time_type}_{number}"
            else:
                return time_type
    
    # 如果沒有找到特定時間表達，返回預設值
    return "today"

def get_date_range(time_expression: str) -> tuple:
    """
    根據時間表達取得日期範圍
    
    Args:
        time_expression: 時間表達
        
    Returns:
        tuple: (開始日期, 結束日期) 格式為 YYYYMMDD
    """
    today = datetime.now()
    
    if time_expression == 'today':
        start_date = today
        end_date = today
    elif time_expression == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = start_date
    elif time_expression == 'tomorrow':
        start_date = today + timedelta(days=1)
        end_date = start_date
    elif time_expression == 'last_week':
        start_date = today - timedelta(weeks=1)
        end_date = today
    elif time_expression == 'this_week':
        # 本週開始（週一）
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif time_expression == 'next_week':
        start_date = today
        end_date = today + timedelta(weeks=1)
    elif time_expression == 'last_month':
        # 上個月
        if today.month == 1:
            start_date = today.replace(year=today.year-1, month=12)
        else:
            start_date = today.replace(month=today.month-1)
        end_date = today
    elif time_expression == 'this_month':
        start_date = today.replace(day=1)
        end_date = today
    elif time_expression == 'next_month':
        start_date = today
        if today.month == 12:
            end_date = today.replace(year=today.year+1, month=1)
        else:
            end_date = today.replace(month=today.month+1)
    elif time_expression == 'last_quarter':
        # 上一季
        quarter = (today.month - 1) // 3
        if quarter == 0:
            start_date = today.replace(year=today.year-1, month=10)
        else:
            start_date = today.replace(month=(quarter-1)*3+1)
        end_date = today
    elif time_expression == 'this_quarter':
        # 本季
        quarter = (today.month - 1) // 3
        start_date = today.replace(month=quarter*3+1, day=1)
        end_date = today
    elif time_expression == 'next_quarter':
        # 下一季
        quarter = (today.month - 1) // 3
        if quarter == 3:
            start_date = today.replace(year=today.year+1, month=1)
        else:
            start_date = today.replace(month=(quarter+1)*3+1)
        end_date = start_date + timedelta(days=90)
    elif time_expression == 'last_year':
        start_date = today.replace(year=today.year-1)
        end_date = today
    elif time_expression == 'this_year':
        start_date = today.replace(month=1, day=1)
        end_date = today
    elif time_expression == 'next_year':
        start_date = today
        end_date = today.replace(year=today.year+1)
    elif time_expression.startswith('recent_days_'):
        days = int(time_expression.split('_')[-1])
        start_date = today - timedelta(days=days)
        end_date = today
    elif time_expression.startswith('recent_weeks_'):
        weeks = int(time_expression.split('_')[-1])
        start_date = today - timedelta(weeks=weeks)
        end_date = today
    elif time_expression.startswith('recent_months_'):
        months = int(time_expression.split('_')[-1])
        # 簡化處理，每個月算30天
        start_date = today - timedelta(days=months*30)
        end_date = today
    elif time_expression.startswith('recent_years_'):
        years = int(time_expression.split('_')[-1])
        start_date = today.replace(year=today.year-years)
        end_date = today
    else:
        # 預設最近5天
        start_date = today - timedelta(days=5)
        end_date = today
    
    # 格式化為 YYYYMMDD
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    return start_str, end_str 