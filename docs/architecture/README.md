# 系統架構圖

```mermaid fullWidth="true"
graph TB
    %% 用戶層
    User[👤 用戶] --> Frontend[ 前端 React/Next.js]
    
    %% 前端層
    Frontend --> |SSE 請求| API[🚀 FastAPI 後端]
    Frontend --> |WebSocket| WS[🔌 WebSocket 連接]
    
    %% 後端 API 層
    API --> |/api/ask-sse| SSEHandler[ SSE 事件處理器]
    API --> |/api/ask| SyncHandler[⚡ 同步處理器]
    API --> |/api/query-database| DBHandler[🗄️ 資料庫查詢]
    API --> |/api/query-chart| ChartHandler[ 圖表查詢]
    
    %% 主要資料流處理
    SSEHandler --> MainFlow[🔄 主資料流處理]
    
    %% 同步處理節點 (Sequential Processing)
    subgraph "同步處理節點"
        MainFlow --> DetectStocks[🔍 股票代號偵測]
        DetectStocks --> DetectTime[⏰ 時間偵測]
        DetectTime --> DetectChart[📈 圖表偵測]
        DetectChart --> ClassifyExtract[🧠 問題理解與分類]
        ClassifyExtract --> NewsSearch[ 新聞搜尋]
        NewsSearch --> FinancialData[📊 財務資料獲取]
        FinancialData --> ReportPipeline[ 報告生成 Pipeline]
    end
    
    %% 報告生成 Pipeline (Sequential Section Generation)
    subgraph "報告生成 Pipeline"
        ReportPipeline --> PriceSummary[📉 股價異動總結]
        PriceSummary --> FinancialSection[💰 財務狀況分析]
        FinancialSection --> StrategySection[💡 投資策略建議]
        StrategySection --> NoticeSection[⚠️ 操作注意事項]
        NoticeSection --> SourcesSection[📚 資料來源]
        SourcesSection --> DisclaimerSection[⚖️ 免責聲明]
    end
    
    %% 投資策略建議 Section (包含 summary_table)
    StrategySection --> LLMStrategy[🤖 LLM 策略生成]
    LLMStrategy --> SummaryTable[ Summary Table 生成]
    SummaryTable --> StrategyResult[✅ 策略結果]
    
    %% 外部 API 整合
    NewsSearch --> SerperAPI[🌐 Serper API]
    FinancialData --> YahooFinance[📈 Yahoo Finance API]
    FinancialData --> FinLabAPI[🏦 FinLab API]
    
    %% 資料庫層
    DBHandler --> CMoneyDB[💾 CMoney 資料庫]
    ChartHandler --> CMoneyDB
    
    %% 前端渲染層
    subgraph "前端渲染組件"
        Frontend --> InvestmentCard[📊 InvestmentReportCard]
        InvestmentCard --> SummaryTableComponent[📋 SummaryTableComponent]
        InvestmentCard --> TabsComponent[📑 TabsComponent]
        InvestmentCard --> FinancialScores[📈 FinancialScoresComponent]
    end
    
    %% 資料流回傳
    StrategyResult --> ReportPipeline
    ReportPipeline --> MainFlow
    MainFlow --> SSEHandler
    SSEHandler --> |SSE 串流| Frontend
    
    %% 樣式定義
    classDef userLayer fill:#e1f5fe
    classDef frontendLayer fill:#f3e5f5
    classDef backendLayer fill:#e8f5e8
    classDef apiLayer fill:#fff3e0
    classDef dataLayer fill:#fce4ec
    classDef externalLayer fill:#f1f8e9
    
    class User userLayer
    class Frontend,InvestmentCard,SummaryTableComponent,TabsComponent,FinancialScores frontendLayer
    class API,SSEHandler,SyncHandler,DBHandler,ChartHandler,MainFlow backendLayer
    class DetectStocks,DetectTime,DetectChart,ClassifyExtract,NewsSearch,FinancialData,ReportPipeline apiLayer
    class PriceSummary,FinancialSection,StrategySection,NoticeSection,SourcesSection,DisclaimerSection,LLMStrategy,SummaryTable,StrategyResult dataLayer
    class SerperAPI,YahooFinance,FinLabAPI,CMoneyDB externalLayer

```

## 自選股摘要流程圖

```mermaid fullWidth="true"
graph TB
    %% 用戶層
    User[👤 用戶] --> |選擇自選股清單| Frontend[ 前端 Next.js]
    
    %% 前端 API 層
    Frontend --> |POST /api/watchlist-summary| WatchlistAPI[🚀 Watchlist Summary API]
    Frontend --> |GET /api/watchlist-summary-sse| SSEAPI[ SSE API]
    
    %% 後端處理層
    WatchlistAPI --> |轉發請求| BackendAPI[🏗️ FastAPI 後端]
    SSEAPI --> |轉發 SSE| BackendAPI
    
    %% 自選股摘要 Pipeline
    subgraph "自選股摘要 Pipeline"
        BackendAPI --> WatchlistPipeline[🔄 Watchlist Summary Pipeline]
        
        %% 主要處理節點
        WatchlistPipeline --> IndustryDistribution[📊 產業分布分析]
        IndustryDistribution --> PriceSummary[📈 價格摘要分析]
        PriceSummary --> ReturnAnalysis[📉 報酬率分析]
        ReturnAnalysis --> FocusStocks[⭐ 重點股票分析]
        FocusStocks --> IndustryComparison[🏭 產業比較分析]
        IndustryComparison --> SocialSentiment[💬 社群情緒分析]
        SocialSentiment --> InvestmentStrategy[💡 投資策略建議]
        InvestmentStrategy --> NewsSummary[📰 新聞摘要]
        NewsSummary --> FinalSummary[✅ 最終摘要]
    end
    
    %% 各節點的詳細處理
    subgraph "產業分布分析"
        IndustryDistribution --> IndustryStats[📈 產業統計]
        IndustryStats --> TopIndustries[🏆 主要產業]
        TopIndustries --> IndustryChart[📊 產業圖表]
    end
    
    subgraph "價格摘要分析"
        PriceSummary --> PriceStats[📊 價格統計]
        PriceStats --> PriceChanges[📈 價格變化]
        PriceChanges --> PriceChart[📊 價格圖表]
    end
    
    subgraph "報酬率分析"
        ReturnAnalysis --> ReturnStats[📊 報酬率統計]
        ReturnStats --> BestPerformers[🏆 最佳表現]
        BestPerformers --> WorstPerformers[📉 最差表現]
    end
    
    subgraph "重點股票分析"
        FocusStocks --> StockScreening[🔍 股票篩選]
        StockScreening --> FocusCriteria[📋 重點標準]
        FocusCriteria --> FocusList[📝 重點清單]
    end
    
    subgraph "產業比較分析"
        IndustryComparison --> IndustryMetrics[📊 產業指標]
        IndustryMetrics --> ComparisonTable[📋 比較表格]
        ComparisonTable --> IndustryInsights[💡 產業洞察]
    end
    
    subgraph "社群情緒分析"
        SocialSentiment --> SentimentData[📊 情緒資料]
        SentimentData --> SentimentAnalysis[🧠 情緒分析]
        SentimentAnalysis --> SentimentChart[📊 情緒圖表]
    end
    
    subgraph "投資策略建議"
        InvestmentStrategy --> StrategyAnalysis[🧠 策略分析]
        StrategyAnalysis --> RiskAssessment[⚠️ 風險評估]
        RiskAssessment --> StrategyRecommendations[💡 策略建議]
    end
    
    subgraph "新聞摘要"
        NewsSummary --> NewsSearch[🔍 新聞搜尋]
        NewsSearch --> NewsFiltering[📰 新聞過濾]
        NewsFiltering --> NewsSummarization[📝 新聞摘要]
    end
    
    %% 外部 API 整合
    NewsSearch --> SerperAPI[🌐 Serper API]
    PriceSummary --> YahooFinance[📈 Yahoo Finance API]
    ReturnAnalysis --> YahooFinance
    FocusStocks --> FinLabAPI[🏦 FinLab API]
    IndustryComparison --> FinLabAPI
    SocialSentiment --> SocialAPI[💬 社群 API]
    
    %% 資料庫層
    BackendAPI --> CMoneyDB[💾 CMoney 資料庫]
    IndustryDistribution --> CMoneyDB
    PriceSummary --> CMoneyDB
    
    %% 前端渲染層
    subgraph "前端渲染組件"
        Frontend --> WatchlistCard[📊 WatchlistSummaryCard]
        WatchlistCard --> SectionTabs[📑 Section Tabs]
        WatchlistCard --> IndustryChart[📊 Industry Chart]
        WatchlistCard --> PriceChart[📈 Price Chart]
        WatchlistCard --> SentimentChart[💬 Sentiment Chart]
        WatchlistCard --> StrategyCard[💡 Strategy Card]
    end
    
    %% 資料流回傳
    FinalSummary --> WatchlistPipeline
    WatchlistPipeline --> BackendAPI
    BackendAPI --> |JSON Response| WatchlistAPI
    BackendAPI --> |SSE Stream| SSEAPI
    WatchlistAPI --> Frontend
    SSEAPI --> |SSE Stream| Frontend
    
    %% 樣式定義
    classDef userLayer fill:#e1f5fe
    classDef frontendLayer fill:#f3e5f5
    classDef backendLayer fill:#e8f5e8
    classDef pipelineLayer fill:#fff3e0
    classDef detailLayer fill:#fce4ec
    classDef externalLayer fill:#f1f8e9
    classDef dataLayer fill:#e0f2f1
    
    class User userLayer
    class Frontend,WatchlistCard,SectionTabs,IndustryChart,PriceChart,SentimentChart,StrategyCard frontendLayer
    class WatchlistAPI,SSEAPI,BackendAPI,CMoneyDB backendLayer
    class WatchlistPipeline,IndustryDistribution,PriceSummary,ReturnAnalysis,FocusStocks,IndustryComparison,SocialSentiment,InvestmentStrategy,NewsSummary,FinalSummary pipelineLayer
    class IndustryStats,TopIndustries,IndustryChart,PriceStats,PriceChanges,PriceChart,ReturnStats,BestPerformers,WorstPerformers,StockScreening,FocusCriteria,FocusList,IndustryMetrics,ComparisonTable,IndustryInsights,SentimentData,SentimentAnalysis,SentimentChart,StrategyAnalysis,RiskAssessment,StrategyRecommendations,NewsSearch,NewsFiltering,NewsSummarization detailLayer
    class SerperAPI,YahooFinance,FinLabAPI,SocialAPI externalLayer

```

## 架構說明

* **前端 (Next.js)**：負責用戶互動、頁面渲染、API 請求。
* **後端 (FastAPI + LangGraph)**：負責問題理解、新聞搜尋、資料彙整、投資報告生成。
* **外部 API**：串接 OpenAI、Serper、Yahoo、CMoney 等服務。
* **資料庫/快取**：可選，提升查詢效能。

## 自選股摘要流程說明

### 主要功能

* **產業分布分析**：分析自選股中各產業的分布情況
* **價格摘要分析**：統計各股票的價格變動和趨勢
* **報酬率分析**：計算並比較各股票的報酬率表現
* **重點股票分析**：根據特定標準篩選出重點關注股票
* **產業比較分析**：比較不同產業的表現和指標
* **社群情緒分析**：分析社群對各股票的討論情緒
* **投資策略建議**：基於分析結果提供投資策略建議
* **新聞摘要**：彙整相關新聞並生成摘要

### 技術特點

* **模組化設計**：每個分析節點獨立運作，易於維護和擴展
* **並行處理**：部分分析可以並行執行，提升效能
* **SSE 串流**：支援即時進度回報，提升用戶體驗
* **多源資料整合**：整合多個資料來源，提供全面分析

***

此架構支援高擴展性與模組化開發，方便日後功能擴充。
