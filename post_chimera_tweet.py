import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse

def get_bot_identity():
    weekday = datetime.utcnow().weekday()
    if weekday in [0, 2, 4]:
        return 'A', '都市裁判くん'
    elif weekday in [1, 3, 5]:
        return 'B', 'ささやきノベル'
    else:
        return 'C', '観察者Z'

def load_template(bot_key):
    with open("templates.json", "r", encoding="utf-8") as f:
        templates = json.load(f)
    data = templates.get(bot_key)
    if not data:
        raise Exception("Bot template not found.")
    return data["template"].format(**data["variables"])

def post_to_twitter(username, password, content):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # ログイン
    driver.get("https://twitter.com/login")
    time.sleep(5)
    driver.find_element(By.NAME, "text").send_keys(username, Keys.RETURN)
    time.sleep(3)
    # パスワード欄を input[type="password"] で取得
    pwd = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    pwd.send_keys(password, Keys.RETURN)
    time.sleep(5)

    # Web Intent で投稿ページへ
    intent_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(content)
    driver.get(intent_url)
    time.sleep(5)

    # 投稿ボタンをクリック
    btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
    btn.click()
    time.sleep(5)

    driver.quit()

if __name__ == "__main__":
    key, bot_key = get_bot_identity()
    content = load_template(bot_key)
    username = os.environ[f"TWITTER_USERNAME_{key}"]
    password = os.environ[f"TWITTER_PASSWORD_{key}"]
    post_to_twitter(username, password, content)
