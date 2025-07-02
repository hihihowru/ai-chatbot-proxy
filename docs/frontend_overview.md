# 前端架構概覽

## 系統概述

前端系統基於 Next.js 14 構建，採用 App Router 架構，提供現代化的台股投資分析介面。系統整合了聊天功能、自選股管理、即時分析等多個模組，提供完整的投資分析體驗。

## 技術棧

### 核心技術
- **框架**：Next.js 14 (App Router)
- **語言**：TypeScript
- **樣式**：Tailwind CSS
- **狀態管理**：React Hooks + Context
- **API 通訊**：Fetch API + Server-Sent Events (SSE)

### 主要依賴
- **UI 組件**：Radix UI、Lucide React
- **圖表**：Chart.js、Recharts
- **表單處理**：React Hook Form
- **日期處理**：date-fns
- **HTTP 客戶端**：Axios

## 目錄結構

```
ai_chat_twstock/
├── app/
│   ├── api/                    # API 路由
│   │   ├── ask-llm/           # LLM 分析 API
│   │   ├── news/              # 新聞搜尋 API
│   │   ├── proxy_login/       # 代理登入
│   │   ├── proxy_custom_group/ # 自選股群組
│   │   └── watchlist-summary/ # 自選股摘要
│   ├── components/            # 共用組件
│   │   ├── AiReplyModal.tsx   # AI 回覆模態框
│   │   ├── AskQuestionBar.tsx # 問題輸入欄
│   │   ├── CardFooter.tsx     # 卡片底部
│   │   ├── CustomGroupSelector.tsx # 自選股選擇器
│   │   ├── LoadingSpinner.tsx # 載入動畫
│   │   ├── MessageCard.tsx    # 訊息卡片
│   │   ├── NewsCard.tsx       # 新聞卡片
│   │   ├── SectionCard.tsx    # 區塊卡片
│   │   ├── StockCard.tsx      # 股票卡片
│   │   ├── TableCard.tsx      # 表格卡片
│   │   └── WatchlistSummaryCard.tsx # 自選股摘要卡片
│   ├── chat/                  # 聊天頁面
│   ├── mvp/                   # MVP 測試頁面
│   ├── threads/               # 對話串頁面
│   ├── watchlist/             # 自選股頁面
│   ├── layout.tsx             # 根佈局
│   ├── page.tsx               # 首頁
│   └── styles/                # 樣式檔案
├── lib/                       # 工具函數
│   ├── alias.ts               # 股票別名處理
│   ├── news.ts                # 新聞處理
│   └── resolveStockId.ts      # 股票代號解析
├── public/                    # 靜態資源
│   ├── data/                  # 資料檔案
│   └── icons/                 # 圖示檔案
└── src/                       # 原始碼
    └── modules/               # 模組
        └── promptBuilder.ts   # 提示詞建構器
```

## 主要頁面

### 1. 首頁 (`/`)
- **功能**：系統入口，提供快速導航
- **組件**：導航選單、功能卡片、快速開始
- **特色**：響應式設計，支援多種螢幕尺寸

### 2. 聊天頁面 (`/chat`)
- **功能**：主要對話介面
- **組件**：
  - `AskQuestionBar`：問題輸入
  - `MessageCard`：訊息顯示
  - `AiReplyModal`：AI 回覆模態框
- **特色**：即時對話、SSE 串流、多種卡片類型

### 3. MVP 測試頁面 (`/mvp`)
- **功能**：功能測試和開發驗證
- **組件**：測試介面、參數調整、結果顯示
- **特色**：開發者友好、快速迭代

### 4. 自選股頁面 (`/watchlist`)
- **功能**：自選股管理和分析
- **組件**：
  - `CustomGroupSelector`：自選股選擇器
  - `WatchlistSummaryCard`：摘要卡片
  - 各種分析圖表
- **特色**：群組管理、即時分析、視覺化呈現

### 5. 對話串頁面 (`/threads`)
- **功能**：歷史對話管理
- **組件**：對話列表、搜尋、篩選
- **特色**：對話歷史、快速重複、組織管理

## 核心組件

### 1. 問題輸入組件 (`AskQuestionBar`)
```typescript
interface AskQuestionBarProps {
  onAsk: (question: string) => void;
  placeholder?: string;
  disabled?: boolean;
}
```
- **功能**：問題輸入和提交
- **特色**：自動完成、歷史記錄、快捷鍵支援

### 2. 訊息卡片組件 (`MessageCard`)
```typescript
interface MessageCardProps {
  message: Message;
  onAction?: (action: string, data: any) => void;
}
```
- **功能**：顯示各種類型的訊息
- **支援類型**：文字、表格、圖表、新聞、股票資訊

### 3. 自選股選擇器 (`CustomGroupSelector`)
```typescript
interface CustomGroupSelectorProps {
  onGroupSelect: (groupName: string, stockIds: string[]) => void;
  groups: CustomGroup[];
}
```
- **功能**：自選股群組選擇和管理
- **特色**：群組預覽、快速選擇、編輯功能

### 4. 摘要卡片組件 (`WatchlistSummaryCard`)
```typescript
interface WatchlistSummaryCardProps {
  sections: Section[];
  loading?: boolean;
}
```
- **功能**：顯示自選股分析摘要
- **支援區塊**：產業分布、股價摘要、報酬率統計、焦點個股

## API 串接方式

### 1. 標準 API 調用
```typescript
const response = await fetch('/api/ask-llm', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: userQuestion,
    context: conversationContext
  })
});
```

### 2. SSE 即時串流
```typescript
const eventSource = new EventSource(`/api/ask-sse?question=${encodeURIComponent(question)}`);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.log) {
    // 更新進度
    updateProgress(data.log);
  } else if (data.result) {
    // 處理結果
    handleResult(data.result);
    eventSource.close();
  }
};
```

### 3. 代理 API 調用
```typescript
const response = await fetch('/api/proxy_custom_group', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    action: 'get_groups',
    userId: currentUser.id
  })
});
```

## 狀態管理

### 1. 全域狀態 (Context)
```typescript
interface AppContextType {
  user: User | null;
  conversation: Message[];
  customGroups: CustomGroup[];
  loading: boolean;
  error: string | null;
}
```

### 2. 本地狀態 (Hooks)
```typescript
// 對話狀態
const [messages, setMessages] = useState<Message[]>([]);
const [isLoading, setIsLoading] = useState(false);

// 自選股狀態
const [selectedGroup, setSelectedGroup] = useState<string>('');
const [stockList, setStockList] = useState<string[]>([]);
```

### 3. 表單狀態
```typescript
const { register, handleSubmit, formState: { errors } } = useForm<FormData>();
```

## UI/UX 流程

### 1. 對話流程
```
用戶輸入 → 驗證 → 發送 API → 顯示進度 → 接收結果 → 渲染卡片
```

### 2. 自選股分析流程
```
選擇群組 → 發送分析請求 → 顯示載入狀態 → 接收各區塊資料 → 渲染摘要
```

### 3. 錯誤處理流程
```
API 錯誤 → 顯示錯誤訊息 → 提供重試選項 → 記錄錯誤日誌
```

## 響應式設計

### 1. 斷點設定
```css
/* Tailwind CSS 斷點 */
sm: 640px   /* 手機橫向 */
md: 768px   /* 平板 */
lg: 1024px  /* 小螢幕桌面 */
xl: 1280px  /* 大螢幕桌面 */
2xl: 1536px /* 超大螢幕 */
```

### 2. 組件適配
- **手機**：單欄佈局，簡化介面
- **平板**：雙欄佈局，適中複雜度
- **桌面**：多欄佈局，完整功能

## 擴充新卡片/Section

### 1. 新增卡片類型
```typescript
// 1. 定義卡片介面
interface NewCardProps {
  data: NewCardData;
  onAction?: (action: string, data: any) => void;
}

// 2. 實作卡片組件
const NewCard: React.FC<NewCardProps> = ({ data, onAction }) => {
  return (
    <div className="card-container">
      {/* 卡片內容 */}
    </div>
  );
};

// 3. 在 MessageCard 中整合
const renderCard = (card: Card) => {
  switch (card.type) {
    case 'new_card':
      return <NewCard data={card.data} onAction={handleCardAction} />;
    // ... 其他卡片類型
  }
};
```

### 2. 新增 Section 類型
```typescript
// 1. 定義 Section 介面
interface NewSection {
  title: string;
  content: string;
  cards: Card[];
  sources: Source[];
}

// 2. 在後端新增對應模組
// 3. 在前端新增渲染邏輯
```

## 效能優化

### 1. 程式碼分割
- **動態導入**：`const Component = dynamic(() => import('./Component'))`
- **路由分割**：Next.js 自動分割頁面
- **組件懶載入**：非關鍵組件延遲載入

### 2. 快取策略
- **API 快取**：使用 SWR 或 React Query
- **靜態資源**：CDN 快取
- **瀏覽器快取**：適當的 Cache-Control 標頭

### 3. 圖片優化
- **Next.js Image**：自動優化和響應式
- **WebP 格式**：現代瀏覽器支援
- **懶載入**：視窗內才載入

## 測試策略

### 1. 單元測試
- **組件測試**：React Testing Library
- **工具函數測試**：Jest
- **API 測試**：MSW (Mock Service Worker)

### 2. 整合測試
- **頁面測試**：Playwright
- **API 整合**：端到端測試
- **用戶流程**：關鍵路徑測試

### 3. 效能測試
- **Lighthouse**：效能評分
- **Bundle 分析**：程式碼大小
- **載入時間**：實際用戶體驗

## 部署配置

### 1. 環境變數
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.example.com
NEXT_PUBLIC_PROXY_URL=https://proxy.example.com
OPENAI_API_KEY=your_openai_key
```

### 2. 建置配置
```json
{
  "scripts": {
    "build": "next build",
    "start": "next start",
    "export": "next export"
  }
}
```

### 3. 部署平台
- **Vercel**：推薦平台，自動部署
- **Netlify**：靜態網站託管
- **自建伺服器**：Docker 容器化

## 未來擴充

### 1. 短期目標
- 新增更多圖表類型
- 優化載入效能
- 增強錯誤處理

### 2. 長期目標
- PWA 支援
- 離線功能
- 多語言支援
- 個人化設定 