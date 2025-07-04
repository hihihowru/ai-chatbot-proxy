# 📋 更新日誌 (CHANGELOG)

## [未發布] - 2025-01-XX

### 🎨 UI/UX 與產品規劃
- **用戶旅程重新設計**
  - 採用 MECE 框架重新定義目標用戶
  - 按時段分段：盤前、盤中、盤後
  - 建立完整的用戶旅程地圖
  - 設計對應的 wireframe 原型

- **Wireframe 設計完成**
  - 盤前首頁：健康度檢查、國際觀點、市場環境
  - 盤中首頁：即時監控、熱門股排行、異動提醒
  - 盤後首頁：今日總結、籌碼分析、明日重點
  - 個股分析頁：大師觀點切換、多維度分析
  - 對話框設計：智能助理、語音輸入、上下文記憶

- **互動設計優化**
  - 每個元件點擊都可帶入相關提問
  - 智能對話框支援多輪對話
  - 語音輸入功能提升使用便利性
  - 上下文感知的建議問題系統

### 🚀 新增功能
- **輿情分析功能升級**
  - 標題改為"爆料同學會輿情分析"
  - 重新設計卡片結構，包含過去48小時統計
  - 新增情緒分布表格（正面/負面/中性貼文數和留言數）
  - 新增市場標籤功能（如"市場過熱警示"/"市場悲觀"）
  - 新增用戶討論貼文縮圖功能

- **分組搜尋功能**
  - 實現多關鍵字分組搜尋
  - 提升搜尋結果的相關性和準確性

- **關鍵字生成擴展**
  - 擴展關鍵字生成數量
  - 優化關鍵字相關性算法

- **日誌記錄系統**
  - 完善日誌記錄功能
  - 新增詳細的調試信息記錄

- **測試腳本**
  - 新增多個測試腳本
  - 包含輿情分析、搜尋功能等測試

### 🔧 技術改進
- **部署配置優化**
  - 修正 Railway 部署的 PORT 環境變數問題
  - 添加 nixpacks.toml 配置
  - 更新 railway.toml 配置
  - 修正 Dockerfile 和 Procfile 配置

- **Vercel 本地開發支持**
  - 添加 vercel.json 配置文件
  - 支持本地開發模式
  - 配置 FastAPI 路由

### 🐛 錯誤修復
- 修正 uvicorn 啟動時的 PORT 環境變數錯誤
- 修復 nixpacks builder 的 pip 命令找不到問題
- 修正 app 路徑配置問題

### 📚 文檔更新
- 新增 CHANGELOG.md 版本控制文檔
- 更新部署相關文檔
- 完善 API 文檔

---

## [v1.0.0] - 2025-06-25

### 🚀 初始版本
- **台股投資分析助理系統**
  - 基於 LangGraph 的投資分析流程
  - 整合 Serper API 搜尋功能
  - 支援個股分析和自選股分析

- **核心功能**
  - 股票代號識別和解析
  - 財務數據分析
  - 技術分析報告
  - 投資策略建議
  - 社群輿情觀察

- **技術架構**
  - FastAPI 後端框架
  - LangGraph 工作流程管理
  - OpenAI GPT 模型整合
  - 多數據源整合（CMoney、Yahoo Finance等）

---

## 📝 版本命名規則

### 語義化版本 (Semantic Versioning)
- **主版本號 (Major)**: 不兼容的 API 修改
- **次版本號 (Minor)**: 向下兼容的功能性新增
- **修訂號 (Patch)**: 向下兼容的問題修正

### 版本類型
- **Alpha**: 內部測試版本
- **Beta**: 公開測試版本
- **RC (Release Candidate)**: 發布候選版本
- **Stable**: 穩定發布版本

---

## 🔗 相關連結

- [GitHub 倉庫](https://github.com/your-username/ai-chatbot-proxy)
- [部署地址](https://your-app.railway.app)
- [API 文檔](https://your-app.railway.app/docs)
- [開發文檔](docs/README.md)

---

## 📞 聯絡資訊

如有問題或建議，請透過以下方式聯絡：
- GitHub Issues: [創建 Issue](https://github.com/your-username/ai-chatbot-proxy/issues)
- Email: your-email@example.com

---

*最後更新: 2025-07-01* 