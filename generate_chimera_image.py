import os
import json
import openai
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image

# デバッグフラグ
DEBUG_MODE = os.getenv("DEBUG_MODE") == "1"

openai.api_key = os.getenv("OPENAI_API_KEY")

# ① Bot人格を曜日で選択
def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0,2,4]: return 'A','都市裁判くん'
    if wd in [1,3,5]: return 'B','ささやきノベル'
    return 'C','観察者Z'

# ② テンプレートからノベル変数を読み込む
def load_variables(bot_name):
    with open("templates.json","r",encoding="utf-8") as f:
        data = json.load(f)
    return data[bot_name]["variables"]

# ③ 画像生成用プロンプトを作成
def build_prompt(vars):
    title = vars.get("title","")
    desc  = vars.get("phenomenon", vars.get("ending_line",""))
    return f"Illustration for a novel titled “{title}”, depicting “{desc}” in a dark surreal style."

# ④ OpenAI Images API(v1.0+)を使って画像を生成
def gen_image(prompt, out_path):
        # プレースホルダ画像を生成
        if DEBUG_MODE:
        img = Image.new("RGB", (512, 512), color=(200,200,200))
        draw = ImageDraw.Draw(img)
        text = "DEBUG"
        tw, th = draw.textsize(text)
        draw.text(((512-tw)/2, (512-th)/2), text, fill=(50,50,50))
        img.save(out_path)
        print(f"[DEBUG] Placeholder image saved → {out_path}")
        return

    # 本番用：OpenAI Images API
    resp = openai.images.generate(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="b64_json"
    )
    b64 = resp["data"][0]["b64_json"]
    img = Image.open(BytesIO(base64.b64decode(b64)))
    img.save(out_path)
    print(f"[{bot_name}] Generated image → {out_path}")

if __name__=="__main__":
    key, bot_name = get_bot_identity()
    vars   = load_variables(bot_name)
    prompt = build_prompt(vars)
    os.makedirs(f"images/{key}", exist_ok=True)
    out_file = f"images/{key}/latest.png"
    print(f"[{bot_name}] Generating with prompt:\n  {prompt}")
    gen_image(prompt, out_file)
    print(f"[{bot_name}] Saved → {out_file}")
