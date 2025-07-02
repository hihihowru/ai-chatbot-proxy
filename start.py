#!/usr/bin/env python3
"""
Railway 啟動腳本
"""

import os
import subprocess
import sys

def main():
    print("🚀 啟動 AI Chatbot Proxy 後端...")
    
    # 獲取端口
    port = os.getenv('PORT', '8000')
    print(f"📡 使用端口: {port}")
    
    # 檢查環境變數
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    for var in required_vars:
        if not os.getenv(var):
            print(f"⚠️  警告: {var} 未設定")
    
    # 啟動 uvicorn
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'langgraph_app.main:app',
        '--host', '0.0.0.0',
        '--port', port
    ]
    
    print(f"🔧 執行命令: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 啟動失敗: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 收到中斷信號，正在關閉...")
        sys.exit(0)

if __name__ == "__main__":
    main() 