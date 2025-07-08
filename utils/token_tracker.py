import json
import time
from typing import Dict, List, Optional
from datetime import datetime
import os

class TokenTracker:
    """
    OpenAI API Token 使用量追蹤器
    記錄每次 API 調用的 token 使用情況和成本
    """
    
    def __init__(self, log_file: str = "token_usage.json"):
        self.log_file = log_file
        self.usage_log = []
        self.load_existing_log()
    
    def load_existing_log(self):
        """載入現有的使用記錄"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.usage_log = json.load(f)
        except Exception as e:
            print(f"載入 token 記錄失敗: {e}")
            self.usage_log = []
    
    def record_api_call(self, 
                       node_name: str,
                       model: str,
                       prompt_tokens: int,
                       completion_tokens: int,
                       total_tokens: int,
                       cost: float,
                       user_input: str = "",
                       stock_id: str = "",
                       success: bool = True,
                       error_message: str = ""):
        """
        記錄一次 API 調用
        
        Args:
            node_name: 節點名稱 (如 classify_and_extract)
            model: 使用的模型 (如 gpt-3.5-turbo)
            prompt_tokens: 輸入 token 數量
            completion_tokens: 輸出 token 數量
            total_tokens: 總 token 數量
            cost: 成本 (美元)
            user_input: 用戶輸入
            stock_id: 股票代號
            success: 是否成功
            error_message: 錯誤訊息
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "node_name": node_name,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost,
            "user_input": user_input[:200],  # 限制長度
            "stock_id": stock_id,
            "success": success,
            "error_message": error_message
        }
        
        self.usage_log.append(record)
        self.save_log()
        
        # 即時輸出
        print(f"🔢 Token 使用記錄: {node_name} | 輸入: {prompt_tokens} | 輸出: {completion_tokens} | 總計: {total_tokens} | 成本: ${cost:.4f}")
    
    def save_log(self):
        """儲存使用記錄到檔案"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_log, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存 token 記錄失敗: {e}")
    
    def get_usage_summary(self, 
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         node_name: Optional[str] = None) -> Dict:
        """
        取得使用量摘要
        
        Args:
            start_date: 開始日期 (ISO 格式)
            end_date: 結束日期 (ISO 格式)
            node_name: 特定節點名稱
        
        Returns:
            使用量摘要字典
        """
        filtered_log = self.usage_log.copy()
        
        # 日期篩選
        if start_date:
            filtered_log = [r for r in filtered_log if r["timestamp"] >= start_date]
        if end_date:
            filtered_log = [r for r in filtered_log if r["timestamp"] <= end_date]
        
        # 節點篩選
        if node_name:
            filtered_log = [r for r in filtered_log if r["node_name"] == node_name]
        
        if not filtered_log:
            return {
                "total_calls": 0,
                "total_prompt_tokens": 0,
                "total_completion_tokens": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "success_rate": 0.0,
                "node_breakdown": {}
            }
        
        # 計算統計
        total_calls = len(filtered_log)
        total_prompt_tokens = sum(r["prompt_tokens"] for r in filtered_log)
        total_completion_tokens = sum(r["completion_tokens"] for r in filtered_log)
        total_tokens = sum(r["total_tokens"] for r in filtered_log)
        total_cost = sum(r["cost_usd"] for r in filtered_log)
        success_calls = sum(1 for r in filtered_log if r["success"])
        success_rate = success_calls / total_calls if total_calls > 0 else 0
        
        # 節點細分
        node_breakdown = {}
        for record in filtered_log:
            node = record["node_name"]
            if node not in node_breakdown:
                node_breakdown[node] = {
                    "calls": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "cost": 0.0
                }
            
            node_breakdown[node]["calls"] += 1
            node_breakdown[node]["prompt_tokens"] += record["prompt_tokens"]
            node_breakdown[node]["completion_tokens"] += record["completion_tokens"]
            node_breakdown[node]["total_tokens"] += record["total_tokens"]
            node_breakdown[node]["cost"] += record["cost_usd"]
        
        return {
            "total_calls": total_calls,
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "success_rate": success_rate,
            "node_breakdown": node_breakdown
        }
    
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """
        計算 API 調用成本
        
        Args:
            model: 模型名稱
            prompt_tokens: 輸入 token 數量
            completion_tokens: 輸出 token 數量
        
        Returns:
            成本 (美元)
        """
        # OpenAI 定價 (2024年)
        pricing = {
            "gpt-3.5-turbo": {
                "input": 0.0015,   # $0.0015 per 1K tokens
                "output": 0.002    # $0.002 per 1K tokens
            },
            "gpt-4": {
                "input": 0.03,     # $0.03 per 1K tokens
                "output": 0.06     # $0.06 per 1K tokens
            },
            "gpt-4-turbo": {
                "input": 0.01,     # $0.01 per 1K tokens
                "output": 0.03     # $0.03 per 1K tokens
            }
        }
        
        if model not in pricing:
            # 預設使用 gpt-3.5-turbo 定價
            model = "gpt-3.5-turbo"
        
        input_cost = (prompt_tokens / 1000) * pricing[model]["input"]
        output_cost = (completion_tokens / 1000) * pricing[model]["output"]
        
        return input_cost + output_cost
    
    def get_daily_usage(self, date: str) -> Dict:
        """取得特定日期的使用量"""
        start_date = f"{date}T00:00:00"
        end_date = f"{date}T23:59:59"
        return self.get_usage_summary(start_date, end_date)
    
    def get_monthly_usage(self, year: int, month: int) -> Dict:
        """取得特定月份的使用量"""
        start_date = f"{year:04d}-{month:02d}-01T00:00:00"
        if month == 12:
            end_date = f"{year+1:04d}-01-01T00:00:00"
        else:
            end_date = f"{year:04d}-{month+1:02d}-01T00:00:00"
        return self.get_usage_summary(start_date, end_date)
    
    def export_report(self, filename: str = None) -> str:
        """匯出使用報告"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"token_usage_report_{timestamp}.json"
        
        summary = self.get_usage_summary()
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "detailed_log": self.usage_log
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filename

# 全域實例
token_tracker = TokenTracker()

def track_openai_call(node_name: str, 
                     response, 
                     user_input: str = "",
                     stock_id: str = "",
                     success: bool = True,
                     error_message: str = ""):
    """
    追蹤 OpenAI API 調用的便捷函數
    
    Args:
        node_name: 節點名稱
        response: OpenAI API 回應物件
        user_input: 用戶輸入
        stock_id: 股票代號
        success: 是否成功
        error_message: 錯誤訊息
    """
    try:
        if hasattr(response, 'usage'):
            usage = response.usage
            model = response.model if hasattr(response, 'model') else "gpt-3.5-turbo"
            
            cost = token_tracker.calculate_cost(
                model,
                usage.prompt_tokens,
                usage.completion_tokens
            )
            
            token_tracker.record_api_call(
                node_name=node_name,
                model=model,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
                cost=cost,
                user_input=user_input,
                stock_id=stock_id,
                success=success,
                error_message=error_message
            )
        else:
            print(f"⚠️ 無法追蹤 token 使用量: {node_name} - 回應物件缺少 usage 屬性")
            
    except Exception as e:
        print(f"❌ Token 追蹤失敗: {e}")

# 測試用
if __name__ == "__main__":
    # 模擬測試
    tracker = TokenTracker("test_token_usage.json")
    
    # 模擬記錄
    tracker.record_api_call(
        node_name="classify_and_extract",
        model="gpt-3.5-turbo",
        prompt_tokens=150,
        completion_tokens=50,
        total_tokens=200,
        cost=0.0004,
        user_input="台積電怎麼樣？",
        stock_id="2330"
    )
    
    # 顯示摘要
    summary = tracker.get_usage_summary()
    print("Token 使用摘要:")
    print(json.dumps(summary, ensure_ascii=False, indent=2)) 