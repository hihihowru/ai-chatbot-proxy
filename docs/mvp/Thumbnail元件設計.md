# Thumbnail 元件設計

## 元件概述
Thumbnail 元件是 MVP 首頁的核心視覺元素，用於展示股票、指數等金融數據的簡化視圖。

## 設計規格

### 基本尺寸
- **長寬比**: 3:2
- **手機版寬度**: 160px (一排兩個)
- **平板版寬度**: 200px (一排三個)
- **桌面版寬度**: 240px (一排四個)

### 視覺結構
```
┌─────────────────────────────────┐
│ 股票名稱                股票代碼 │
│ 價格 (漲跌幅)          產業類別 │
│                                 │
│ ┌─────────────────────────────┐ │
│ │                             │ │
│ │        K線圖區域            │ │
│ │     (OHLC + Volume)        │ │
│ │                             │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

## 元件類型

### 1. 個股 Thumbnail
**適用場景**: 自選股清單、熱門股排行

**數據結構**:
```typescript
interface StockThumbnailProps {
  name: string;           // 股票名稱
  code: string;           // 股票代碼
  price: number;          // 當前價格
  change: number;         // 漲跌金額
  changePercent: number;  // 漲跌幅
  industry: string;       // 產業類別
  chartData: OHLCVData[]; // K線圖數據
}
```

**視覺範例**:
```
┌─────────────────────────────────┐
│ 長榮                   2603     │
│ 197.5 (+2.3%)    航運業        │
│                                 │
│ ┌─────────────────────────────┐ │
│ │                             │ │
│ │      K線圖區域              │ │
│ │   (OHLC + Volume)          │ │
│ │                             │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

### 2. 指數 Thumbnail
**適用場景**: 國際市場動態

**數據結構**:
```typescript
interface IndexThumbnailProps {
  name: string;           // 指數名稱
  code: string;           // 指數代碼
  price: number;          // 當前點數
  change: number;         // 漲跌點數
  changePercent: number;  // 漲跌幅
  market: string;         // 市場名稱
  chartData: OHLCVData[]; // K線圖數據
}
```

**視覺範例**:
```
┌─────────────────────────────────┐
│ 道瓊指數               DJI      │
│ 38,790 (+1.2%)    美股          │
│                                 │
│ ┌─────────────────────────────┐ │
│ │                             │ │
│ │      K線圖區域              │ │
│ │   (OHLC + Volume)          │ │
│ │                             │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

## 視覺設計規範

### 顏色系統
- **背景色**: #FFFFFF
- **邊框色**: #E5E7EB
- **漲色**: #10B981 (綠色)
- **跌色**: #EF4444 (紅色)
- **文字主色**: #232323
- **文字次要**: #6B7280
- **K線圖背景**: #F9FAFB

### 字體規範
- **股票名稱**: 14px, font-semibold, #232323
- **股票代碼**: 12px, font-medium, #6B7280
- **價格**: 16px, font-bold, #232323
- **漲跌幅**: 14px, font-medium, 漲跌色
- **產業類別**: 12px, font-normal, #6B7280

### 間距規範
- **外邊距**: 8px
- **內邊距**: 12px
- **元素間距**: 8px
- **K線圖區域**: 上方留 16px 間距

## 互動設計

### 點擊行為
1. **整個 Thumbnail**: 進入詳細分析頁面
2. **K線圖區域**: 放大顯示 K線圖
3. **股票名稱**: 快速搜尋該股票

### 懸停效果
- **背景色**: 輕微變暗 (#F9FAFB)
- **邊框**: 主色調邊框 (#2563EB)
- **陰影**: 輕微陰影效果

### 載入狀態
- **骨架屏**: 顯示基本結構
- **載入動畫**: 淡入效果
- **錯誤狀態**: 顯示預設圖示

## 響應式設計

### 手機版 (320px-768px)
```css
.thumbnail {
  width: 160px;
  height: 107px;
  margin: 8px;
}
```

### 平板版 (768px-1024px)
```css
.thumbnail {
  width: 200px;
  height: 133px;
  margin: 12px;
}
```

### 桌面版 (1024px+)
```css
.thumbnail {
  width: 240px;
  height: 160px;
  margin: 16px;
}
```

## 技術實作

### React 元件結構
```typescript
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface ThumbnailProps {
  type: 'stock' | 'index';
  data: StockThumbnailProps | IndexThumbnailProps;
  onClick?: () => void;
  onChartClick?: () => void;
}

const Thumbnail: React.FC<ThumbnailProps> = ({
  type,
  data,
  onClick,
  onChartClick
}) => {
  // 元件實作
};
```

### CSS 類別結構
```css
.thumbnail {
  @apply bg-white rounded-lg border border-gray-200 p-3 cursor-pointer;
  @apply hover:bg-gray-50 hover:border-blue-500 transition-all duration-200;
  @apply shadow-sm hover:shadow-md;
}

.thumbnail-header {
  @apply flex justify-between items-start mb-2;
}

.thumbnail-info {
  @apply flex justify-between items-end mb-3;
}

.thumbnail-chart {
  @apply bg-gray-50 rounded border border-gray-100;
  @apply cursor-pointer hover:bg-gray-100 transition-colors;
}
```

## 數據整合

### K線圖數據格式
```typescript
interface OHLCVData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

### API 整合
- **股票數據**: 使用 FinLab API
- **K線圖**: 使用 TradingView 或自建圖表庫
- **即時更新**: WebSocket 連接

## 效能優化

### 圖片優化
- **K線圖**: 使用 Canvas 或 SVG 渲染
- **快取策略**: 本地快取 + 伺服器快取
- **懶載入**: 視窗內才載入 K線圖

### 記憶體管理
- **元件回收**: 離開視窗時清理資源
- **數據清理**: 定期清理過期數據
- **事件監聽**: 正確移除事件監聽器

## 測試策略

### 單元測試
- 元件渲染測試
- 點擊事件測試
- 數據顯示測試

### 視覺測試
- 不同螢幕尺寸測試
- 不同數據狀態測試
- 載入狀態測試

### 效能測試
- 大量 Thumbnail 渲染測試
- 記憶體使用量測試
- 滾動效能測試 