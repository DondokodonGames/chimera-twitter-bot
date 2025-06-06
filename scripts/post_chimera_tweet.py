import argparse
import json
import os
# Placeholder for Twitter posting logic
# Implement actual Twitter API calls here.

def post_tweet(game_type, link, image_path):
    # Implement posting logic with Twitter API
    print(f"Posting {game_type} tweet with link {link} and image {image_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, help='Game type to post')
    args = parser.parse_args()

    game_type = args.type
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Adjust key for "都市裁判" to match "都市裁判くん"
    key = "都市裁判くん" if game_type == "都市裁判" else game_type
    tweet_template = data.get(key, {})
    link = f"https://<your_github_pages_url>/novel/{game_type}/"
    image_path = tweet_template.get("variables", {}).get("image", "")

    post_tweet(game_type, link, image_path)

if __name__ == "__main__":
    main()
