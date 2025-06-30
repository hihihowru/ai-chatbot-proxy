# 系統架構圖

```mermaid
graph TD
    A[使用者瀏覽器] -->|HTTP/HTTPS| B[前端 Next.js]
    B -->|API 請求| C[後端 FastAPI (LangGraph)]
    C -->|OpenAI API| D[OpenAI/LLM]
    C -->|Serper API| E[新聞搜尋]
    C -->|Yahoo/CMoney API| F[財經數據]
    C -->|資料庫查詢| G[DB/快取]
    C -->|API 回應| B
    B -->|渲染投資報告| A
```

## 架構說明

- **前端 (Next.js)**：負責用戶互動、頁面渲染、API 請求。
- **後端 (FastAPI + LangGraph)**：負責問題理解、新聞搜尋、資料彙整、投資報告生成。
- **外部 API**：串接 OpenAI、Serper、Yahoo、CMoney 等服務。
- **資料庫/快取**：可選，提升查詢效能。

---

此架構支援高擴展性與模組化開發，方便日後功能擴充。 