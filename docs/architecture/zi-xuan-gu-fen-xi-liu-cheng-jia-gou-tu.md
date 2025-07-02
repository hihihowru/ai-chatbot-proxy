# 自選股分析流程架構圖

```mermaid
// Some code
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
