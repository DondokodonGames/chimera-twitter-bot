# -*- coding: utf-8 -*-
import os
import json
import openai
from datetime import datetime
from PIL import Image, ImageDraw
from io import BytesIO
import base64

# デバッグモードフラグ: DEBUG_MODE=1 または OPENAI_API_KEY が設定されていなければデバッグ
DEBUG_MODE = os.getenv("DEBUG_MODE") == "1" or not bool(os.getenv("OPENAI_API_KEY"))

# OpenAI APIキー設定（DEBUG_MODE時は不要）
openai.api_key = os.getenv("OPENAI_API_KEY") if not DEBUG_MODE else None

def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0, 2, 4]:
        return 'A', '都市裁判くん'
    if wd in [1, 3, 5]:
        return 'B', 'ささやきノベル'
    return 'C', '観察者Z'

def load_variables(bot_name):
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[bot_name]["variables"]

def build_prompt(vars):
    title = vars.get("title", "")
    desc = vars.get("phenomenon", vars.get("ending_line", ""))
    return f"Illustration for a novel titled “{title}”, depicting “{desc}” in a dark, surreal style."

def gen_image(prompt, out_path):
        # デバッグモード: プレースホルダ画像を生成
    if DEBUG_MODE:
        img = Image.new("RGB", (512, 512), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        text = "DEBUG"
        # textbbox で文字サイズを取得
        bbox = draw.textbbox((0, 0), text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # 文字を中央に描画
        draw.text(((512 - tw) / 2, (512 - th) / 2), text, fill=(50, 50, 50))
        img.save(out_path)
        print(f"[DEBUG] Placeholder image saved → {out_path}")
        return

    # 本番モード: OpenAI Images API 呼び出し
    response = openai.images.generate(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="b64_json"
    )
    b64 = response["data"][0]["b64_json"]
    img = Image.open(BytesIO(base64.b64decode(b64)))
    img.save(out_path)
    print(f"[{bot_name}] Generated image → {out_path}")

if __name__ == "__main__":
    key, bot_name = get_bot_identity()
    vars = load_variables(bot_name)
    prompt = build_prompt(vars)
    os.makedirs(f"images/{key}", exist_ok=True)
    out_file = f"images/{key}/latest.png"
    print(f"[{bot_name}] Generating with prompt:")
    print(f"  {prompt}")
    gen_image(prompt, out_file)
