import os
import json
from datetime import datetime
import tweepy

# Bot を曜日で選択
def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0,2,4]:
        return 'A','都市裁判くん'
    if wd in [1,3,5]:
        return 'B','ささやきノベル'
    return 'C','観察者Z'

# テンプレ読み込み
def load_template(key):
    data = json.load(open("templates.json","r",encoding="utf-8"))
    tpl = data.get(key)
    if not tpl:
        raise RuntimeError(f"No template for {key}")
    return tpl["template"].format(**tpl["variables"])

# Tweepy で投稿
def post_tweet(bot_key, content):
    prefix = f"TW_API_KEY_{bot_key}"
    auth = tweepy.OAuth1UserHandler(
        os.environ[f"{prefix}"],
        os.environ[f"TW_API_SECRET_{bot_key}"],
        os.environ[f"TW_ACCESS_TOKEN_{bot_key}"],
        os.environ[f"TW_ACCESS_SECRET_{bot_key}"]
    )
    api = tweepy.API(auth)
    api.update_status(content)

if __name__ == "__main__":
    key, bot = get_bot_identity()
    text = load_template(bot)
    post_tweet(key, text)
