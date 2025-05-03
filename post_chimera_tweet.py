import os
import time
import json
import urllib.parse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Bot人格を曜日で切り替える
def get_bot_identity():
    weekday = datetime.utcnow().weekday()
    if weekday in [0, 2, 4]:
        return 'A', '都市裁判くん'
    elif weekday in [1, 3, 5]:
        return 'B', 'ささやきノベル'
    else:
        return 'C', '観察者Z'

# テンプレート読み込みと本文生成
def load_template(bot_key):
    with open("templates.json", "r", encoding="utf-8") as f:
        templates = json.load(f)
    template_data = templates.get(bot_key)
    if not template_data:
        raise Exception(f"Bot template for '{bot_key}' not found.")
    return template_data["template"].format(**template_data["variables"])

# SeleniumによるTwitter投稿（Web Intent利用）
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

    # ユーザー名入力
    user_input = driver.find_element(By.NAME, "text")
    user_input.send_keys(username)
    user_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # パスワード入力（type=passwordセレクタを使用）
    pwd_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    pwd_input.send_keys(password)
    pwd_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Web Intent URL で投稿ページへ遷移（UI依存を回避）
    intent_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(content)
    driver.get(intent_url)
    time.sleep(5)

    # Intent のツイートボタンをクリック
    tweet_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
    tweet_button.click()
    time.sleep(5)

    driver.quit()

if __name__ == "__main__":
    key, bot_key = get_bot_identity()
    content = load_template(bot_key)

    username = os.environ.get(f"TWITTER_USERNAME_{key}")
    password = os.environ.get(f"TWITTER_PASSWORD_{key}")

    if not username or not password:
        raise RuntimeError(f"Credentials for bot '{key}' are not set in environment variables.")

    post_to_twitter(username, password, content)
