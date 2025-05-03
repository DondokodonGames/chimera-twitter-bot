import os
import time
import json
import urllib.parse
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot_debug.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0, 2, 4]:
        return 'A', '都市裁判くん'
    if wd in [1, 3, 5]:
        return 'B', 'ささやきノベル'
    return 'C', '観察者Z'

def load_template(bot_key):
    data = json.load(open("templates.json", "r", encoding="utf-8"))
    tpl = data.get(bot_key)
    if not tpl:
        raise Exception(f"No template for {bot_key}")
    return tpl["template"].format(**tpl["variables"])

def post_to_twitter(username, password, content, key):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        logging.info(f"Bot {key}: Logging in as {username}")
        driver.get("https://twitter.com/login")
        time.sleep(5)

        driver.find_element(By.NAME, "text").send_keys(username, Keys.RETURN)
        time.sleep(3)
        pwd_el = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        pwd_el.send_keys(password, Keys.RETURN)
        time.sleep(5)

        logging.info(f"Bot {key}: Navigating to intent/tweet")
        intent = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(content)
        driver.get(intent)
        time.sleep(5)

        logging.info(f"Bot {key}: Clicking tweet button")
        tweet_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
        tweet_button.click()
        time.sleep(5)

        logging.info(f"Bot {key}: Tweet posted successfully")

    except Exception as e:
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        screenshot = f"debug_{key}_{timestamp}.png"
        html_dump = f"debug_{key}_{timestamp}.html"
        driver.save_screenshot(screenshot)
        with open(html_dump, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logging.exception(f"Bot {key}: Error occurred, saved {screenshot} and {html_dump}")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    key, bot = get_bot_identity()
    try:
        content = load_template(bot)
        user = os.getenv(f"TWITTER_USERNAME_{key}")
        pwd  = os.getenv(f"TWITTER_PASSWORD_{key}")
        if not user or not pwd:
            raise RuntimeError(f"Credentials for {key} missing")
        post_to_twitter(user, pwd, content, key)
    except Exception as e:
        logging.error(f"Fatal error for bot {key}: {e}")
        raise
