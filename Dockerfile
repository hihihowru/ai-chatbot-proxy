# syntax=docker/dockerfile:1
FROM python:3.9-slim AS base

WORKDIR /app

# 安裝系統依賴（如有需要可加）
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements 先安裝依賴，加快快取
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . .

# 預設 uvicorn port
EXPOSE 8000

# 使用 uvicorn 啟動 FastAPI app，確保 PORT 可被 Railway 設定
CMD ["python", "start_simple.py"]

