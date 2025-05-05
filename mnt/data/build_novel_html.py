# build_novel_html.py: CHIMERAノベルをHTML5にビルドするスクリプト

import os
import json
from jinja2 import Environment, FileSystemLoader

def main():
    # テンプレートJSONをロード
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Jinja2環境設定
    os.makedirs("novel_templates", exist_ok=True)
    env = Environment(loader=FileSystemLoader("novel_templates"))
    
    # シンプルHTMLテンプレートをnovel_templates/novel.html.j2として作成する想定
    # 例:
    # <!DOCTYPE html>
    # <html><head><meta charset="utf-8"><title>{{ title }}</title></head>
    # <body><h1>{{ title }}</h1><p>{{ body }}</p></body></html>

    # ビルド先ディレクトリ
    publish_dir = "public"
    os.makedirs(publish_dir, exist_ok=True)

    for bot_key, tpl in data.items():
        title = tpl["variables"].get("title", bot_key)
        # 本文など自由にテンプレート側で扱えるよう変数渡し
        context = {
            "title": title,
            "variables": tpl["variables"]
        }
        html = env.get_template("novel.html.j2").render(context)
        out_dir = os.path.join(publish_dir, bot_key)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Built novel for {bot_key} → {out_dir}/index.html")

if __name__ == "__main__":
    main()

# .github/workflows/novel_build.yml: HTML5ノベルのビルド＆GitHub Pagesデプロイ

novel_build_workflow = """
name: Build and Deploy CHIMERA Novels

on:
  push:
    paths:
      - 'templates.json'
      - 'novel_templates/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install jinja2

      - name: Build novel HTML
        run: python build_novel_html.py

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
"""

# 保存
os.makedirs("/mnt/data/.github/workflows", exist_ok=True)
with open("/mnt/data/build_novel_html.py", "w", encoding="utf-8") as f:
    f.write(open(__file__, encoding="utf-8").read().split('# build_novel_html.py:')[1].split('# .github')[0])
with open("/mnt/data/.github/workflows/novel_build.yml", "w", encoding="utf-8") as f:
    f.write(novel_build_workflow)

[("/mnt/data/build_novel_html.py", "build_novel_html.py"), ("/mnt/data/.github/workflows/novel_build.yml", "novel_build.yml")]
