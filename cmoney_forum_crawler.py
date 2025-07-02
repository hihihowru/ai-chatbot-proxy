import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.cmoney.tw/forum/stock/2330"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_forum_posts():
    resp = requests.get(BASE_URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    posts = []
    for post in soup.select(".post-list .post-item"):
        title = post.select_one(".post-title").get_text(strip=True) if post.select_one(".post-title") else ""
        link = post.select_one("a")['href'] if post.select_one("a") else ""
        comments = post.select_one(".comment-count").get_text(strip=True) if post.select_one(".comment-count") else "0"
        likes = post.select_one(".like-count").get_text(strip=True) if post.select_one(".like-count") else "0"
        time = post.select_one(".post-time").get_text(strip=True) if post.select_one(".post-time") else ""
        posts.append({
            "title": title,
            "link": link,
            "comments": int(comments.replace(",", "") or 0),
            "likes": int(likes.replace(",", "") or 0),
            "time": time
        })
    # 依熱門度排序（留言數+按讚數）
    posts.sort(key=lambda x: (x["comments"] + x["likes"]), reverse=True)
    return posts

if __name__ == "__main__":
    posts = fetch_forum_posts()
    print(f"共抓到 {len(posts)} 篇貼文")
    for i, post in enumerate(posts[:10], 1):
        print(f"{i}. {post['title']} | 留言: {post['comments']} | 按讚: {post['likes']} | 時間: {post['time']} | 連結: {post['link']}") 