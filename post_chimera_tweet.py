import os
import json
from datetime import datetime
import tweepy
import glob

def get_bot_identity():
    """曜日ごとにBotを切り替え：A/B/Cと名称"""
    wd = datetime.utcnow().weekday()
    if wd in [0, 2, 4]:
        return 'A', '都市裁判くん'
    if wd in [1, 3, 5]:
        return 'B', 'ささやきノベル'
    return 'C', '観察者Z'

def load_template(bot_name):
    """templates.jsonからBot名に対応したテンプレートを読み込む"""
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    tpl = data.get(bot_name)
    if not tpl:
        raise RuntimeError(f"No template for '{bot_name}'")
    return tpl["template"].format(**tpl["variables"])

def post_tweet_with_media(bot_key, content):
    """画像アップロードは v1.1 API、ツイート投稿は v2 API で行う"""
    # 1) v1.1 でメディアをアップロード
    auth_v1 = tweepy.OAuth1UserHandler(
        os.getenv(f"TW_API_KEY_{bot_key}"),
        os.getenv(f"TW_API_SECRET_{bot_key}"),
        os.getenv(f"TW_ACCESS_TOKEN_{bot_key}"),
        os.getenv(f"TW_ACCESS_SECRET_{bot_key}")
    )
    api_v1 = tweepy.API(auth_v1)
    imgs = sorted(glob.glob(f"images/{bot_key}/*.png"))
    if not imgs:
        raise RuntimeError(f"No image found for bot {bot_key}")
    media = api_v1.media_upload(imgs[-1])
    media_id = media.media_id_string

    # 2) v2 でツイートを投稿
    client = tweepy.Client(
        consumer_key=os.getenv(f"TW_API_KEY_{bot_key}"),
        consumer_secret=os.getenv(f"TW_API_SECRET_{bot_key}"),
        access_token=os.getenv(f"TW_ACCESS_TOKEN_{bot_key}"),
        access_token_secret=os.getenv(f"TW_ACCESS_SECRET_{bot_key}")
    )
    response = client.create_tweet(text=content, media_ids=[media_id])
    if hasattr(response, "errors") and response.errors:
        raise RuntimeError(f"Tweet failed: {response.errors}")
    tweet_id = response.data.get("id")
    print(f"[Bot {bot_key}] Tweet with image posted. ID={tweet_id}")

if __name__ == "__main__":
    bot_key, bot_name = get_bot_identity()
    text = load_template(bot_name)
    post_tweet_with_media(bot_key, text)
