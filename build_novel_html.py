import os
import json
from jinja2 import Environment, FileSystemLoader

# Bot名から出力ディレクトリキーへのマッピング
BOT_DIR_MAP = {
    "都市裁判くん": "A",
    "ささやきノベル": "B",
    "観察者Z": "C"
}

def main():
    # templates.json をロード
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Jinja2 環境設定
    env = Environment(loader=FileSystemLoader("novel_templates"))

    # 出力先ディレクトリ
    publish_dir = "public"
    os.makedirs(publish_dir, exist_ok=True)

    # 各 Bot ごとに HTML をビルド
    for bot_name, tpl in data.items():
        dir_key = BOT_DIR_MAP.get(bot_name)
        if not dir_key:
            print(f"Warning: No mapping for {bot_name}, using name as directory")
            dir_key = bot_name

        title = tpl["variables"].get("title", bot_name)
        context = {
            "title": title,
            "variables": tpl["variables"]
        }

        html = env.get_template("novel.html.j2").render(context)
        out_dir = os.path.join(publish_dir, dir_key)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Built novel for {bot_name} → {out_dir}/index.html")

if __name__ == "__main__":
    main()
