import requests

url = "https://www.cmoney.tw/forum/stock/2330"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
resp.raise_for_status()

with open("cmoney_2330_forum.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

print("HTML 已儲存為 cmoney_2330_forum.html") 