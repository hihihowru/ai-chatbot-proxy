#!/usr/bin/env python3
"""
檢查環境變數設定
"""

import os
from dotenv import load_dotenv

# 載入 .env 檔案（如果存在）
load_dotenv()

def check_environment_variables():
    """檢查必需的環境變數"""
    
    print("🔧 環境變數檢查")
    print("=" * 50)
    
    # 必需的環境變數
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API 金鑰",
        "SERPER_API_KEY": "Serper API 金鑰",
        "PORT": "端口號（Railway 自動設定）",
        "ENVIRONMENT": "環境標識"
    }
    
    all_good = True
    
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        
        if value:
            # 隱藏敏感資訊
            if "API_KEY" in var_name:
                masked_value = value[:10] + "..." + value[-4:] if len(value) > 14 else "***"
            else:
                masked_value = value
                
            print(f"✅ {var_name}: {masked_value}")
            print(f"   說明: {description}")
        else:
            print(f"❌ {var_name}: 未設定")
            print(f"   說明: {description}")
            if var_name in ["OPENAI_API_KEY", "SERPER_API_KEY"]:
                all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 所有必需的環境變數都已設定！")
    else:
        print("⚠️  請設定缺少的環境變數")
        print("\n📋 設定步驟：")
        print("1. 登入 Railway 控制台")
        print("2. 選擇您的專案")
        print("3. 點擊 'Variables' 標籤")
        print("4. 添加缺少的環境變數")
    
    return all_good

if __name__ == "__main__":
    check_environment_variables() 