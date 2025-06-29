import json

def generate_disclaimer_section() -> dict:
    """
    產生免責聲明 section
    
    Returns:
        免責聲明 section 的 JSON 格式
    """
    try:
        print(f"[DEBUG] 開始產生 section: 免責聲明")
        
        disclaimer_section = {
            "section": "免責聲明",
            "disclaimer": "本報告僅供參考，投資需謹慎，一切風險自負。本報告所載資料來源於公開資訊，我們不保證其準確性、完整性或及時性。投資決策應基於個人風險承受能力和投資目標，建議在投資前諮詢專業投資顧問。"
        }
        
        print(f"[DEBUG] 解析後內容：{json.dumps(disclaimer_section, ensure_ascii=False, indent=2)}")
        print(f"[DEBUG] 合併 section: 免責聲明")
        
        return {
            "success": True,
            "section": disclaimer_section,
            "raw_content": "固定模板，無需 LLM"
        }
        
    except Exception as e:
        print(f"[generate_disclaimer_section ERROR] {e}")
        # 回傳預設內容
        default_section = {
            "section": "免責聲明",
            "disclaimer": "本報告僅供參考，投資需謹慎，一切風險自負。"
        }
        return {
            "success": False,
            "section": default_section,
            "error": str(e)
        }

# 測試用
if __name__ == "__main__":
    result = generate_disclaimer_section()
    print(json.dumps(result, ensure_ascii=False, indent=2)) 