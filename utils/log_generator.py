import time

def generate_logs():
    logs = [
        "擷取新聞資料中...",
        "分析籌碼變化中...",
        "總結觀點中..."
    ]
    for log in logs:
        yield log
        time.sleep(0.5) 