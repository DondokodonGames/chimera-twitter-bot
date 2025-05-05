import os
import json
from jinja2 import Environment, FileSystemLoader

def main():
    # テンプレートJSONをロード
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Jinja2環境設定
    env = Environment(loader=FileSystemLoader("novel_templates"))
    # novel_templates/novel.html.j2 にテンプレートを配置してください

    publish_dir = "public"
    os.makedirs(publish_dir, exist_ok=True)

    for bot_key, tpl in data.items():
        title = tpl["variables"].get("title", bot_key)
        context = {"title": title, "variables": tpl["variables"]}
        html = env.get_template("novel.html.j2").render(context)
        out_dir = os.path.join(publish_dir, bot_key)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Built novel for {bot_key} -> {out_dir}/index.html")

if __name__ == "__main__":
    main()
