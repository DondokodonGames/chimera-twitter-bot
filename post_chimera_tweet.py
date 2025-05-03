import os, time, json, urllib.parse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0,2,4]: return 'A','都市裁判くん'
    if wd in [1,3,5]: return 'B','ささやきノベル'
    return 'C','観察者Z'

def load_template(key):
    data = json.load(open("templates.json","r",encoding="utf-8"))
    tpl = data.get(key)
    if not tpl: raise Exception(f"No template for {key}")
    return tpl["template"].format(**tpl["variables"])

def post_to_twitter(user, pwd, text):
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    svc = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=svc, options=opts)

    # ログイン
    drv.get("https://twitter.com/login")
    time.sleep(5)
    drv.find_element(By.NAME,"text").send_keys(user, Keys.RETURN)
    time.sleep(3)
    pwd_el = drv.find_element(By.CSS_SELECTOR,'input[type="password"]')
    pwd_el.send_keys(pwd, Keys.RETURN)
    time.sleep(5)

    # Web Intent で投稿
    intent = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(text)
    drv.get(intent)
    time.sleep(5)
    btn = drv.find_element(By.CSS_SELECTOR,"[data-testid='tweetButton']")
    btn.click()
    time.sleep(5)

    drv.quit()

if __name__=="__main__":
    key, bot = get_bot_identity()
    content = load_template(bot)
    user = os.getenv(f"TWITTER_USERNAME_{key}")
    pwd  = os.getenv(f"TWITTER_PASSWORD_{key}")
    if not user or not pwd:
        raise RuntimeError(f"Credentials for {key} missing")
    post_to_twitter(user, pwd, content)
