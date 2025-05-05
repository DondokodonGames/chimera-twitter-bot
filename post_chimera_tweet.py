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
     template_data = data.get(bot_name)
     if not template_data:
         raise RuntimeError(f"No template for '{bot_name}'")
     return template_data["template"].format(**template_data["variables"])

 def post_tweet_v2(bot_key, content):
     """Tweepy v2でツイートを投稿"""
     api_key       = os.environ[f"TW_API_KEY_{bot_key}"]
     api_secret    = os.environ[f"TW_API_SECRET_{bot_key}"]
     access_token  = os.environ[f"TW_ACCESS_TOKEN_{bot_key}"]
     access_secret = os.environ[f"TW_ACCESS_SECRET_{bot_key}"]

     client = tweepy.Client(
         consumer_key=api_key,
         consumer_secret=api_secret,
         access_token=access_token,
         access_token_secret=access_secret
     )
     response = client.create_tweet(text=content)
     if hasattr(response, "errors") and response.errors:
         raise RuntimeError(f"Tweet failed: {response.errors}")
     tweet_id = response.data.get("id")
     print(f"[Bot {bot_key}] Tweet posted. ID={tweet_id}")

def post_tweet_with_media(bot_key, content):
    """画像付きツイートをv1.1 APIで投稿"""
    # OAuth1.0a 認証
    auth_v1 = tweepy.OAuth1UserHandler(
        os.environ[f"TW_API_KEY_{bot_key}"],
        os.environ[f"TW_API_SECRET_{bot_key}"],
        os.environ[f"TW_ACCESS_TOKEN_{bot_key}"],
        os.environ[f"TW_ACCESS_SECRET_{bot_key}"]
    )
    api_v1 = tweepy.API(auth_v1)

    # images/{bot_key}/latest.png を最新画像として取得
    imgs = sorted(glob.glob(f"images/{bot_key}/*.png"))
    if not imgs:
        raise RuntimeError(f"No image found for bot {bot_key}")
    media = api_v1.media_upload(imgs[-1])

    # 画像付きで投稿
    api_v1.update_status(status=content, media_ids=[media.media_id_string])
    print(f"[Bot {bot_key}] Tweet with image posted.")

 if __name__ == "__main__":
     bot_key, bot_name = get_bot_identity()
     text = load_template(bot_name)
    # 画像付き投稿を優先する場合はこちらを呼び出し
    post_tweet_with_media(bot_key, text)
    # もし画像が不要なときは下記を使ってください
    # post_tweet_v2(bot_key, text)
