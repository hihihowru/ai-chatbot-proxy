# 台股投資分析助理系統 - 部署指南

## 系統架構
- **前端**: Next.js (部署到 Vercel)
- **後端**: FastAPI (部署到 Render)

## 後端部署 (Render)

### 1. 準備工作
1. 將 `ai-chatbot-proxy` 目錄推送到 GitHub
2. 確保已移除所有硬編碼的 API Key

### 2. Render 部署步驟
1. 登入 [Render](https://render.com/)
2. 點擊 "New" → "Web Service"
3. 連接 GitHub 倉庫
4. 設定：
   - **Name**: `ai-chatbot-proxy` (或自定義)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn langgraph_app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (或付費方案)

### 3. 環境變數設定
在 Render 的 Environment Variables 中設定：
```
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 4. 部署完成
- 取得後端 URL: `https://your-app-name.onrender.com`

## 前端部署 (Vercel)

### 1. 準備工作
1. 將 `ai_chat_twstock` 目錄推送到 GitHub
2. 確保 API 調用使用環境變數

### 2. Vercel 部署步驟
1. 登入 [Vercel](https://vercel.com/)
2. 點擊 "New Project"
3. 導入 GitHub 倉庫
4. 設定：
   - **Framework Preset**: Next.js
   - **Root Directory**: `ai_chat_twstock`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3. 環境變數設定
在 Vercel 的 Environment Variables 中設定：
```
NEXT_PUBLIC_API_BASE_URL=https://your-app-name.onrender.com
OPENAI_API_KEY=your_openai_api_key_here
NEXT_PUBLIC_PROXY_URL=https://your-app-name.onrender.com
```

### 4. 部署完成
- 取得前端 URL: `https://your-project-name.vercel.app`

## 本地開發

### 後端啟動
```bash
cd ai-chatbot-proxy
pip install -r requirements.txt
uvicorn langgraph_app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端啟動
```bash
cd ai_chat_twstock
npm install
npm run dev
```

## 注意事項

1. **API Key 安全**: 確保所有 API Key 都設定為環境變數，不要硬編碼
2. **CORS 設定**: 後端已設定允許所有來源，生產環境可限制特定域名
3. **冷啟動**: Render 免費方案有冷啟動延遲，建議使用付費方案
4. **監控**: 定期檢查 API 使用量和錯誤日誌

## 故障排除

### 常見問題
1. **ModuleNotFoundError**: 檢查 requirements.txt 是否包含所有依賴
2. **API Key 錯誤**: 確認環境變數設定正確
3. **CORS 錯誤**: 檢查前端 API URL 設定
4. **冷啟動超時**: 考慮升級到付費方案或使用其他平台

### 日誌查看
- Render: 在 Web Service 頁面查看 Logs
- Vercel: 在 Functions 頁面查看 Function Logs 