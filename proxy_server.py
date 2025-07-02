from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
from flask import Flask, request, Response
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')

@app.get("/proxy-news")
def proxy_news(stockId: str = Query(...)):
    url = (
        "https://www.cmoney.tw/MobileService/ashx/GetDtnoData.ashx"
        "?action=getdtnodata"
        "&DtNo=105567992"
        f"&ParamStr=AssignID={stockId};MTPeriod=0;DTMode=0;DTRange=5;DTOrder=1;MajorTable=M173;"
        "&AssignSPID=&KeyMap=&FilterNo=0"  # ✅ 放在 ParamStr 外面
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.cmoney.tw/",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/proxy_login', methods=['POST'])
def proxy_login():
    url = 'https://www.cmoney.tw/identity/token'
    resp = requests.post(url, data=request.form)
    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
