#!/bin/bash

# Railway 啟動腳本
echo "🚀 啟動 AI Chatbot Proxy 後端..."

# 檢查環境變數
if [ -z "$PORT" ]; then
    echo "⚠️  PORT 環境變數未設定，使用預設端口 8000"
    PORT=8000
fi

echo "📡 使用端口: $PORT"

# 啟動應用
exec uvicorn langgraph_app.main:app --host 0.0.0.0 --port "$PORT" 