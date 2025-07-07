# Table of contents

* [🗑️ 台股投資分析助理系統 - 部署指南](README.md)
* [🗑️ 更新日誌 (CHANGELOG)](CHANGELOG.md)
* [🗑️ 🗺 網站地圖 (Sitemap)](docs/sitemap.md)
* [🗑️ 投資分析系統 - Serper API 整合](README_INVESTMENT_ANALYSIS.md)
* [🗑️ 搜尋功能更新說明](README_SEARCH_UPDATE.md)
* [🗑️ 自選股摘要功能](README_WATCHLIST.md)

## 📊 用戶旅程與設計

* [🗑️ 用戶旅程總覽](user_journey_map/README.md)
  * [🗑️ 旅程一：每日追蹤持股健康狀況](user_journey_map/yong-hulcheng-yi.md)
  * [🗑️ 旅程二：初步觀察市場與持股動態](user_journey_map/yong-hulcheng-er.md)
  * [🗑️ 旅程三：深入理解個股漲跌與基本面](user_journey_map/yong-hulcheng-san.md)
  * [🗑️ 旅程四：情緒參考與社群觀點](user_journey_map/yong-hulcheng-si.md)
  * [🗑️ 旅程五：決策思考與投資建議](user_journey_map/yong-hulcheng-wu.md)
  * [🗑️ 旅程六：延伸行動與收藏追蹤](user_journey_map/yong-hulcheng-liu.md)
  * [🗑️ 旅程七：滿足回饋與二次互動](user_journey_map/yong-hulcheng-qi.md)
  * [🗑️ Wireframe 設計文件](user_journey_map/wireframe_design.md)

## 系統架構 系統架構文檔

* [🗑️ 台股投資分析助理系統](docs/README.md)
  * [🗑️ 前端架構概覽](docs/frontend_overview.md)
  * [🗑️ main.py - 系統主架構](docs/main.md)
  * [🗑️ 模組化回覆功能說明](docs/modularized_responses.md)
  * [🗑️ Prompting 設計與範例](docs/prompting.md)
  * [🗑️ 回覆模組系統](docs/response_modules.md)

### 🏛 系統架構圖

* [🗑️ 系統架構總覽](docs/architecture/README.md)
  * [🗑️ 個股分析流程架構圖](docs/architecture/ge-gu-fen-xi-liu-cheng-jia-gou-tu.md)
  * [🗑️ 自選股分析流程架構圖](docs/architecture/zi-xuan-gu-fen-xi-liu-cheng-jia-gou-tu.md)

###  節點模組文檔

* [🗑️ 節點模組總覽](docs/nodes/README.md)
  * [🗑️ classify_and_extract - 分類與提取](docs/nodes/classify_and_extract.md)
  * [🗑️ detect_chart - 圖表檢測](docs/nodes/detect_chart.md)
  * [🗑️ detect_intent - 意圖檢測](docs/nodes/detect_intent.md)
  * [🗑️ detect_stock - 股票檢測](docs/nodes/detect_stock.md)
  * [🗑️ detect_time - 時間檢測](docs/nodes/detect_time.md)
  * [🗑️ generate_report - 報告生成](docs/nodes/generate_report.md)
  * [🗑️ generate_section_financial - 財務分析](docs/nodes/generate_section_financial.md)
  * [🗑️ generate_section_price_summary - 價格摘要](docs/nodes/generate_section_price_summary.md)
  * [🗑️ generate_section_return_analysis - 報酬分析](docs/nodes/generate_section_return_analysis.md)
  * [🗑️ generate_section_social_sentiment - 社群情緒](docs/nodes/generate_section_social_sentiment.md)
  * [🗑️ generate_section_strategy - 策略建議](docs/nodes/generate_section_strategy.md)
  * [🗑️ generate_watchlist_summary_pipeline - 自選股摘要](docs/nodes/generate_watchlist_summary_pipeline.md)
  * [🗑️ search_news - 新聞搜尋](docs/nodes/search_news.md)
  * [🗑️ summarize - 摘要生成](docs/nodes/summarize.md)
  * [🗑️ summarize_results - 結果摘要](docs/nodes/summarize_results.md)

##  產品規劃

* [🗑️ 產品規劃總覽](產品規劃總覽.md)
* [🗑️ 產品規劃總覽](docs/pages/pages/README.md)
* [🗑️ 首頁](docs/pages/pages/home.md)
* [🗑️ 對話頁面](docs/pages/pages/chat.md)
* [🗑️ 個股K線頁面](docs/pages/pages/stock.md)
* [🗑️ 登入頁面](docs/pages/pages/login.md)
* [🗑️ 選擇自選股](docs/pages/pages/select-watchlist.md)
* [🗑️ 收藏頁面](docs/pages/pages/saved.md)
* [🗑️ 設定頁面](docs/pages/pages/settings.md)
* [🗑️ 通用元件](docs/pages/pages/components.md)
