# 系統架構圖

```mermaid
graph TD
  subgraph Client
    A[🧑‍💻 使用者瀏覽器]
  end

  subgraph Frontend
    B[💻 前端 (Next.js)]
  end

  subgraph Backend
    C[🔧 後端 FastAPI + LangGraph]
  end

  subgraph External APIs
    D[🧠 OpenAI / LLM]
    E[📰 Serper (新聞)]
    F[📊 Yahoo / CMoney (財報、籌碼)]
  end

  subgraph Database
    G[(📂 DB / 快取)]
  end

  A -->|HTTP 請求| B
  B -->|API 請求| C

  C -->|呼叫 LLM| D
  C -->|查新聞| E
  C -->|查籌碼/財報| F
  C -->|寫入快取| G
  G -->|讀取資料| C

  C -->|結果回傳| B
  B -->|渲染畫面| A
```

## 架構說明

* **前端 (Next.js)**：負責用戶互動、頁面渲染、API 請求。
* **後端 (FastAPI + LangGraph)**：負責問題理解、新聞搜尋、資料彙整、投資報告生成。
* **外部 API**：串接 OpenAI、Serper、Yahoo、CMoney 等服務。
* **資料庫/快取**：可選，提升查詢效能。

***

此架構支援高擴展性與模組化開發，方便日後功能擴充。
