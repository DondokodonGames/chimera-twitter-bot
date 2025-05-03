
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

# 曜日によってBot人格を切り替える
def get_bot_identity():
    weekday = datetime.utcnow().weekday()
    if weekday in [0, 2, 4]:  # 月水金
        return 'A', '都市裁判くん'
    elif weekday in [1, 3, 5]:  # 火木土
        return 'B', 'ささやきノベル'
    else:  # 日
        return 'C', '観察者Z'

# テンプレート読み込みと本文生成
def load_template(bot_key):
    with open("templates.json", "r", encoding="utf-8") as f:
        templates = json.load(f)
    template_data = templates.get(bot_key)
    if not template_data:
        raise Exception("Bot template not found.")
    return template_data["template"].format(**template_data["variables"])

# SeleniumによるTwitter投稿
def post_to_twitter(username, password, content):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get("https://twitter.com/login")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    time.sleep(3)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    tweet_box = driver.find_element(By.CSS_SELECTOR, "div[aria-label='ツイート内容を入力']")
    tweet_box.send_keys(content)
    time.sleep(2)

    tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
    tweet_button.click()
    time.sleep(5)

    driver.quit()

if __name__ == "__main__":
    bot_key_map = {"A": "都市裁判くん", "B": "ささやきノベル", "C": "観察者Z"}
    key, bot_key = get_bot_identity()
    content = load_template(bot_key)

    username = os.environ[f"TWITTER_USERNAME_{key}"]
    password = os.environ[f"TWITTER_PASSWORD_{key}"]

    post_to_twitter(username, password, content)
