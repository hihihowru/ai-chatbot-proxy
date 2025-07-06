# 通用元件 (Common Components)

## 元件概述
本文檔描述整個應用程式中固定會有的通用元件，這些元件在多個頁面中重複使用，提供一致的用戶體驗和導航功能。

## 主要元件

### 1. Sidebar (側邊欄)

#### 元件路徑
`/components/Sidebar.tsx`

#### 功能描述
提供主要導航功能，包含首頁、時段分析、對話管理、自選股等功能快速存取。

#### 主要功能
- **首頁**: 總覽頁面，顯示重要資訊和快速入口
- **時段分析**: 根據時間自動切換或手動選擇分析時段
  - 盤前分析 (06:00-09:00)
  - 盤中分析 (09:00-13:30) 
  - 盤後分析 (13:30-06:00)
- **對話管理**: 
  - 對話記錄: 所有歷史對話
  - Pinned Chats: 標記的重要對話
- **自選股管理**: 管理自選股群組和設定
- **設定入口**: 進入設定頁面
- **用戶資訊**: 顯示用戶頭像和基本資訊

#### 元件結構
```typescript
interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  currentUser?: User;
  recentChats: Chat[];
  pinnedChats: Chat[];
  watchlistGroups: WatchlistGroup[];
  currentTimeSlot: 'pre-market' | 'mid-day' | 'post-market';
}
```

#### 響應式行為
- **桌面版**: 固定顯示在左側，可收合
- **平板版**: 可收合的側邊欄
- **手機版**: 全螢幕覆蓋式側邊欄

#### 時段導航邏輯
- **自動切換**: 根據當前時間自動高亮對應時段
- **手動選擇**: 用戶可以點擊任何時段查看該時段的專屬內容
- **視覺設計**: 
  - 當前時段：藍色高亮
  - 其他時段：灰色
  - 有未讀訊息：紅色小點提示

#### 互動功能
- **拖曳排序**: 支援對話歷史拖曳排序
- **搜尋功能**: 在歷史對話中搜尋
- **快速操作**: 右鍵選單快速操作
- **鍵盤導航**: 支援鍵盤快捷鍵
- **Pin 功能**: 快速標記重要對話

### 2. Header (頁首)

#### 元件路徑
`/components/Header.tsx`

#### 功能描述
提供頁面頂部的導航和功能按鈕，包含設定、主題切換、通知等。

#### 主要功能
- **Pin 按鈕**: 標記當前對話為重要，加入 Pinned Chats
- **分享按鈕**: 分享當前對話內容
- **設定按鈕**: 快速進入設定頁面
- **主題切換**: Light/Dark Mode 切換
- **通知中心**: 顯示通知數量，進入通知頁面
- **自選股**: 快速進入自選股頁面
- **搜尋功能**: 全域搜尋入口
- **用戶選單**: 用戶頭像和下拉選單

#### 元件結構
```typescript
interface HeaderProps {
  title?: string;
  showBackButton?: boolean;
  onBack?: () => void;
  showSearch?: boolean;
  showNotifications?: boolean;
  notificationCount?: number;
}
```

#### 固定功能按鈕
- **設定按鈕** (`/settings`): 齒輪圖示，進入設定頁面
- **主題切換**: 太陽/月亮圖示，切換明暗主題
- **通知按鈕** (`/notifications`): 鈴鐺圖示，顯示通知數量
- **自選股按鈕** (`/watchlist`): 星形圖示，進入自選股頁面
- **搜尋按鈕**: 放大鏡圖示，開啟全域搜尋

#### 響應式設計
- **桌面版**: 完整功能顯示，包含所有按鈕
- **平板版**: 簡化佈局，重點功能優先
- **手機版**: 最小化佈局，只顯示核心功能

### 3. Footer (頁尾)

#### 元件路徑
`/components/Footer.tsx`

#### 功能描述
在對話頁面中提供輸入框和相關功能，在其他頁面提供頁尾資訊。

#### 對話頁面 Footer
- **輸入框**: 文字輸入區域
- **語音輸入**: 語音輸入按鈕
- **發送按鈕**: 發送訊息
- **附件功能**: 檔案上傳、圖片分享
- **快捷指令**: 常用指令快速選擇

#### 其他頁面 Footer
- **版權資訊**: 版權聲明
- **連結**: 隱私政策、服務條款、幫助
- **聯絡資訊**: 客服聯絡方式
- **社交媒體**: 官方社群連結

#### 元件結構
```typescript
interface FooterProps {
  type: 'chat' | 'page';
  onSendMessage?: (message: string) => void;
  onVoiceInput?: () => void;
  onFileUpload?: (file: File) => void;
  disabled?: boolean;
}
```

#### 對話輸入功能
- **文字輸入**: 支援 Markdown 語法
- **語音輸入**: Web Speech API 整合
- **檔案上傳**: 支援圖片、PDF 等格式
- **快捷指令**: 預設常用指令
- **輸入驗證**: 內容長度、格式驗證

### 4. Navigation (導航)

#### 元件路徑
`/components/Navigation.tsx`

#### 功能描述
提供頁面間的導航功能，包含麵包屑導航和頁面標題。

#### 主要功能
- **麵包屑導航**: 顯示當前頁面路徑
- **頁面標題**: 動態頁面標題
- **返回按鈕**: 返回上一頁
- **快速導航**: 常用頁面快速連結

#### 麵包屑映射
```typescript
const breadcrumbMap = {
  '/': '首頁',
  '/chat': '對話',
  '/stock/[id]': '個股K線',
  '/login': '登入',
  '/select-watchlist': '選擇自選股',
  '/saved': '收藏',
  '/settings': '設定',
  '/share': '分享',
  '/export': '匯出',
  '/notifications': '通知中心',
  '/history': '歷史紀錄',
  '/help': '幫助',
  '/news/[id]': '新聞詳情',
  '/sentiment/[id]': '輿情詳情',
  '/industry/[id]': '產業分析',
  '/event/[id]': '事件詳情'
};
```

### 5. Modal (彈窗)

#### 元件路徑
`/components/Modal.tsx`

#### 功能描述
提供各種彈窗功能，包含確認對話框、設定面板、分享面板等。

#### 主要類型
- **確認對話框**: 操作確認
- **設定面板**: 快速設定
- **分享面板**: 內容分享
- **匯出面板**: 匯出選項
- **通知面板**: 系統通知

#### 元件結構
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showCloseButton?: boolean;
  closeOnOverlayClick?: boolean;
}
```

### 6. Loading (載入)

#### 元件路徑
`/components/Loading.tsx`

#### 功能描述
提供各種載入狀態的視覺回饋。

#### 載入類型
- **骨架屏**: 頁面載入時的骨架結構
- **進度條**: 操作進度顯示
- **旋轉載入**: 一般載入狀態
- **打字指示器**: AI 回應載入

#### 元件結構
```typescript
interface LoadingProps {
  type: 'skeleton' | 'progress' | 'spinner' | 'typing';
  message?: string;
  progress?: number;
  size?: 'sm' | 'md' | 'lg';
}
```

### 7. Error (錯誤)

#### 元件路徑
`/components/Error.tsx`

#### 功能描述
提供錯誤狀態的顯示和處理。

#### 錯誤類型
- **網路錯誤**: 連線問題
- **API 錯誤**: 後端服務錯誤
- **驗證錯誤**: 表單驗證錯誤
- **權限錯誤**: 存取權限問題

#### 元件結構
```typescript
interface ErrorProps {
  type: 'network' | 'api' | 'validation' | 'permission';
  message?: string;
  onRetry?: () => void;
  showRetry?: boolean;
}
```

## 響應式設計

### 桌面版 (>1024px)
- **Sidebar**: 固定顯示，寬度 280px
- **Header**: 完整功能，高度 64px
- **Footer**: 完整輸入功能
- **Modal**: 居中顯示，最大寬度 600px

### 平板版 (768px-1024px)
- **Sidebar**: 可收合，覆蓋式顯示
- **Header**: 簡化佈局，重點功能
- **Footer**: 適配觸控操作
- **Modal**: 適配螢幕尺寸

### 手機版 (<768px)
- **Sidebar**: 全螢幕覆蓋
- **Header**: 最小化佈局
- **Footer**: 觸控優化
- **Modal**: 全螢幕顯示

## 主題支援

### Light Mode
- **背景色**: #FFFFFF
- **文字色**: #1F2937
- **邊框色**: #E5E7EB
- **陰影**: 0 1px 3px rgba(0, 0, 0, 0.1)

### Dark Mode
- **背景色**: #111827
- **文字色**: #F9FAFB
- **邊框色**: #374151
- **陰影**: 0 1px 3px rgba(0, 0, 0, 0.3)

## 無障礙支援

### 鍵盤導航
- **Tab 鍵**: 焦點切換
- **Enter 鍵**: 確認操作
- **Escape 鍵**: 關閉彈窗
- **方向鍵**: 選項切換

### 螢幕閱讀器
- **ARIA 標籤**: 完整的無障礙標籤
- **語義化 HTML**: 正確的 HTML 結構
- **焦點管理**: 適當的焦點處理
- **錯誤提示**: 語音錯誤提示

## 效能優化

### 載入優化
- **懶載入**: 非關鍵元件懶載入
- **程式碼分割**: 按需載入
- **圖片優化**: 響應式圖片
- **快取策略**: 適當的快取

### 渲染優化
- **記憶化**: React.memo 使用
- **虛擬化**: 長列表虛擬化
- **防抖節流**: 事件處理優化
- **記憶體管理**: 元件清理

## 測試案例

### 功能測試
- 元件渲染測試
- 互動功能測試
- 響應式測試
- 主題切換測試

### 無障礙測試
- 鍵盤導航測試
- 螢幕閱讀器測試
- 對比度測試
- 焦點管理測試

### 效能測試
- 載入時間測試
- 記憶體使用測試
- 渲染效能測試
- 網路請求測試

## 使用指南

### 開發指南
1. 使用 TypeScript 確保類型安全
2. 遵循 React Hooks 最佳實踐
3. 實作適當的錯誤邊界
4. 確保無障礙支援

### 樣式指南
1. 使用 Tailwind CSS 進行樣式設計
2. 遵循設計系統規範
3. 確保響應式設計
4. 支援主題切換

### 測試指南
1. 撰寫單元測試
2. 實作整合測試
3. 進行無障礙測試
4. 效能測試驗證

## 未來擴展

### 進階功能
- **動畫效果**: 更豐富的動畫
- **手勢支援**: 觸控手勢操作
- **語音控制**: 語音操作支援
- **AI 輔助**: 智能元件建議

### 整合功能
- **第三方整合**: 外部服務整合
- **PWA 支援**: 離線功能
- **多語言**: 國際化支援
- **分析追蹤**: 使用行為分析 