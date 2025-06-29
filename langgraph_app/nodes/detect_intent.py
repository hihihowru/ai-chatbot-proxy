import openai
import os

PROMPT = '''你是一位金融語意分類專家。請針對使用者的提問，標註出以下三項資訊：

1️⃣ 問題大分類（Question Category）：請從以下選出一個最主要類別：
- 個股分析
- 選股建議
- 盤勢分析
- 比較分析
- 複雜問題查找
- 金融知識詢問
- 無效問題（排除）

2️⃣ 問題子分類（Sub Category）：可複選
（依照大分類自動列出可選範圍）

3️⃣ 投資面向（Aspect）：
- 籌碼面 / 技術面 / 基本面 / 無明確面向

請以以下格式輸出：
---
問題：「最近投信買最多的是哪幾檔 AI 概念股？」

問題大分類：[選股建議]  
問題子分類：[法人追蹤選股]  
投資面向：[籌碼面]
---

問題：「你覺得士電明天會漲嗎？」

問題大分類：[無效問題]  
問題子分類：[不合理預測]  
投資面向：[無明確面向]
---

問題：「請幫我比較長榮與華航的近期營收與股價表現」

問題大分類：[比較分析]  
問題子分類：[兩檔個股比較]  
投資面向：[基本面]
---

請針對以下提問進行標註：
問題：「（這裡填入使用者問題）」
'''

def detect_intent(question: str, model: str = "gpt-3.5-turbo"):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        user_prompt = PROMPT.replace("（這裡填入使用者問題）", question)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[detect_intent ERROR] {e}")
        return f"語意分類失敗: {e}"

# 測試用
if __name__ == "__main__":
    q = "台積電這季財報怎麼樣？"
    print(detect_intent(q)) 