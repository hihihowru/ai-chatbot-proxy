from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://www.cmoney.tw/forum/stock/2330"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL)

# 等待 JS 載入
print("等待 JS 載入...")
time.sleep(5)

# 嘗試抓取討論串
posts = driver.find_elements(By.CSS_SELECTOR, '.post-list .post-item')
print(f"共抓到 {len(posts)} 篇貼文")

for i, post in enumerate(posts[:10], 1):
    title = post.find_element(By.CSS_SELECTOR, '.post-title').text if post.find_elements(By.CSS_SELECTOR, '.post-title') else ''
    comments = post.find_element(By.CSS_SELECTOR, '.comment-count').text if post.find_elements(By.CSS_SELECTOR, '.comment-count') else '0'
    likes = post.find_element(By.CSS_SELECTOR, '.like-count').text if post.find_elements(By.CSS_SELECTOR, '.like-count') else '0'
    time_str = post.find_element(By.CSS_SELECTOR, '.post-time').text if post.find_elements(By.CSS_SELECTOR, '.post-time') else ''
    print(f"{i}. {title} | 留言: {comments} | 按讚: {likes} | 時間: {time_str}")

driver.quit() 