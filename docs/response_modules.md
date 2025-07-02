# 回覆模組系統

## 系統概述

回覆模組系統是台股投資分析助理的核心回應機制，採用高度模組化的設計，每個回覆/圖卡都是獨立的模組，可以動態調整、擴充和組合。系統支援多種內容類型，包括文字、表格、圖表、新聞、股票資訊等。

## 模組化設計理念

### 1. 獨立性
- **單一職責**：每個模組只負責一種特定類型的內容呈現
- **鬆耦合**：模組間不直接依賴，通過標準化介面通信
- **可替換**：可以輕鬆替換或升級單一模組而不影響其他部分

### 2. 可組合性
- **動態組合**：可以根據需求動態組合多個模組
- **條件渲染**：根據內容類型自動選擇合適的模組
- **層級結構**：支援巢狀模組結構

### 3. 擴充性
- **插件式架構**：新增模組只需實作標準介面
- **配置驅動**：通過配置檔案控制模組行為
- **熱更新**：支援運行時動態載入新模組

## 核心模組類型

### 1. 文字模組 (Text Module)
```typescript
interface TextModule {
  type: 'text';
  content: string;
  format?: 'markdown' | 'plain' | 'html';
  style?: TextStyle;
}
```
- **功能**：顯示純文字內容
- **支援格式**：Markdown、純文字、HTML
- **應用場景**：分析摘要、說明文字、注意事項

### 2. 表格模組 (Table Module)
```typescript
interface TableModule {
  type: 'table';
  headers: string[];
  rows: any[][];
  style?: TableStyle;
  sortable?: boolean;
  pagination?: boolean;
}
```
- **功能**：顯示結構化表格資料
- **特色**：支援排序、分頁、自訂樣式
- **應用場景**：股價摘要、財務數據、比較分析

### 3. 圖表模組 (Chart Module)
```typescript
interface ChartModule {
  type: 'chart';
  chartType: 'line' | 'bar' | 'pie' | 'scatter';
  data: ChartData;
  options?: ChartOptions;
  responsive?: boolean;
}
```
- **功能**：顯示各種類型的圖表
- **支援類型**：折線圖、長條圖、圓餅圖、散點圖
- **應用場景**：股價走勢、產業分布、報酬率分析

### 4. 新聞模組 (News Module)
```typescript
interface NewsModule {
  type: 'news';
  articles: NewsArticle[];
  layout?: 'list' | 'grid' | 'carousel';
  maxItems?: number;
}
```
- **功能**：顯示新聞文章列表
- **特色**：支援多種佈局、來源標示、時間排序
- **應用場景**：相關新聞、市場動態、公司消息

### 5. 股票資訊模組 (Stock Module)
```typescript
interface StockModule {
  type: 'stock';
  stockId: string;
  companyName: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
}
```
- **功能**：顯示股票基本資訊
- **特色**：即時價格、漲跌幅、成交量
- **應用場景**：股票概覽、即時報價

### 6. 區塊模組 (Section Module)
```typescript
interface SectionModule {
  type: 'section';
  title: string;
  content: string;
  cards: Card[];
  sources: Source[];
  collapsible?: boolean;
}
```
- **功能**：組織多個子模組
- **特色**：標題、內容、子卡片、資料來源
- **應用場景**：分析報告區塊、功能分組

## 模組實作範例

### 1. 文字模組實作
```typescript
const TextCard: React.FC<TextCardProps> = ({ content, format, style }) => {
  const renderContent = () => {
    switch (format) {
      case 'markdown':
        return <ReactMarkdown>{content}</ReactMarkdown>;
      case 'html':
        return <div dangerouslySetInnerHTML={{ __html: content }} />;
      default:
        return <p className="whitespace-pre-wrap">{content}</p>;
    }
  };

  return (
    <div className={`text-card ${style?.className || ''}`}>
      {renderContent()}
    </div>
  );
};
```

### 2. 表格模組實作
```typescript
const TableCard: React.FC<TableCardProps> = ({ headers, rows, sortable, pagination }) => {
  const [sortConfig, setSortConfig] = useState<SortConfig | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  const sortedRows = useMemo(() => {
    if (!sortConfig) return rows;
    
    return [...rows].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      
      if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, [rows, sortConfig]);

  return (
    <div className="table-card">
      <table className="w-full">
        <thead>
          <tr>
            {headers.map((header, index) => (
              <th 
                key={index}
                onClick={() => sortable && handleSort(index)}
                className={sortable ? 'cursor-pointer' : ''}
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### 3. 圖表模組實作
```typescript
const ChartCard: React.FC<ChartCardProps> = ({ chartType, data, options, responsive }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const ctx = chartRef.current.getContext('2d');
      if (ctx) {
        chartInstance.current = new Chart(ctx, {
          type: chartType,
          data: data,
          options: {
            responsive: responsive,
            ...options
          }
        });
      }
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [chartType, data, options, responsive]);

  return <canvas ref={chartRef} />;
};
```

## 模組註冊系統

### 1. 模組註冊器
```typescript
class ModuleRegistry {
  private modules: Map<string, ModuleConstructor> = new Map();

  register(type: string, constructor: ModuleConstructor) {
    this.modules.set(type, constructor);
  }

  get(type: string): ModuleConstructor | undefined {
    return this.modules.get(type);
  }

  getAll(): string[] {
    return Array.from(this.modules.keys());
  }
}

const moduleRegistry = new ModuleRegistry();

// 註冊模組
moduleRegistry.register('text', TextCard);
moduleRegistry.register('table', TableCard);
moduleRegistry.register('chart', ChartCard);
moduleRegistry.register('news', NewsCard);
moduleRegistry.register('stock', StockCard);
moduleRegistry.register('section', SectionCard);
```

### 2. 動態模組載入
```typescript
const DynamicCard: React.FC<DynamicCardProps> = ({ card }) => {
  const ModuleComponent = moduleRegistry.get(card.type);
  
  if (!ModuleComponent) {
    console.warn(`Unknown card type: ${card.type}`);
    return <div>Unsupported card type: {card.type}</div>;
  }

  return <ModuleComponent {...card.props} />;
};
```

## 配置驅動系統

### 1. 模組配置
```json
{
  "modules": {
    "text": {
      "enabled": true,
      "defaultFormat": "markdown",
      "maxLength": 10000
    },
    "table": {
      "enabled": true,
      "defaultPageSize": 10,
      "sortable": true
    },
    "chart": {
      "enabled": true,
      "defaultHeight": 400,
      "responsive": true
    }
  }
}
```

### 2. 樣式配置
```json
{
  "styles": {
    "text": {
      "default": "text-gray-800 leading-relaxed",
      "highlight": "text-blue-600 font-semibold",
      "warning": "text-red-600 font-medium"
    },
    "table": {
      "header": "bg-gray-100 font-semibold",
      "row": "border-b border-gray-200",
      "cell": "px-4 py-2"
    }
  }
}
```

## 擴充新模組

### 1. 定義模組介面
```typescript
interface CustomModuleProps {
  type: 'custom';
  data: CustomData;
  options?: CustomOptions;
}

interface CustomData {
  // 自訂資料結構
}

interface CustomOptions {
  // 自訂選項
}
```

### 2. 實作模組組件
```typescript
const CustomCard: React.FC<CustomModuleProps> = ({ data, options }) => {
  return (
    <div className="custom-card">
      {/* 自訂內容 */}
    </div>
  );
};
```

### 3. 註冊模組
```typescript
// 註冊新模組
moduleRegistry.register('custom', CustomCard);

// 更新配置
const config = {
  modules: {
    custom: {
      enabled: true,
      // 自訂配置
    }
  }
};
```

## 效能優化

### 1. 懶載入
```typescript
const LazyChartCard = lazy(() => import('./ChartCard'));
const LazyTableCard = lazy(() => import('./TableCard'));

// 根據需要動態載入
const loadModule = async (type: string) => {
  switch (type) {
    case 'chart':
      return await import('./ChartCard');
    case 'table':
      return await import('./TableCard');
    default:
      return null;
  }
};
```

### 2. 虛擬化
```typescript
// 大量資料的表格使用虛擬化
const VirtualizedTable: React.FC<VirtualizedTableProps> = ({ rows }) => {
  return (
    <FixedSizeList
      height={400}
      itemCount={rows.length}
      itemSize={50}
      itemData={rows}
    >
      {Row}
    </FixedSizeList>
  );
};
```

### 3. 快取策略
```typescript
const useModuleCache = (key: string, data: any) => {
  const cache = useRef(new Map());
  
  if (!cache.current.has(key)) {
    cache.current.set(key, data);
  }
  
  return cache.current.get(key);
};
```

## 測試策略

### 1. 單元測試
```typescript
describe('TextCard', () => {
  it('should render markdown content correctly', () => {
    const content = '**Bold text** and *italic text*';
    render(<TextCard content={content} format="markdown" />);
    
    expect(screen.getByText('Bold text')).toBeInTheDocument();
    expect(screen.getByText('italic text')).toBeInTheDocument();
  });
});
```

### 2. 整合測試
```typescript
describe('ModuleRegistry', () => {
  it('should register and retrieve modules correctly', () => {
    const registry = new ModuleRegistry();
    registry.register('test', TestComponent);
    
    expect(registry.get('test')).toBe(TestComponent);
  });
});
```

## 未來擴充

### 1. 短期目標
- 新增更多圖表類型（雷達圖、熱力圖等）
- 支援互動式圖表
- 優化載入效能

### 2. 長期目標
- 支援 3D 圖表
- 實時資料更新
- 自訂主題系統
- 多語言支援 