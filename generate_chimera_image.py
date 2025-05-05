# generate_chimera_image.py

import os, json, base64
from datetime import datetime
from openai import OpenAI
from PIL import Image
from io import BytesIO

# ① Bot人格を曜日で選択
def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0,2,4]: return 'A','都市裁判くん'
    if wd in [1,3,5]: return 'B','ささやきノベル'
    return 'C','観察者Z'

# ② テンプレートからタイトル等を読み込む
def load_variables(bot_name):
    with open("templates.json","r",encoding="utf-8") as f:
        data = json.load(f)
    return data[bot_name]["variables"]

# ③ プロンプト生成例
def build_prompt(vars):
    title = vars.get("title","")
    desc = vars.get("phenomenon",vars.get("ending_line",""))
    return f"Illustration for a novel titled “{title}”, depicting “{desc}” in a dark, surreal style."

# ④ 画像を生成して保存
def gen_image(prompt, out_path):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.images.generate(prompt=prompt, size="512x512", n=1)
    img_data = base64.b64decode(resp.data[0].b64_json)
    img = Image.open(BytesIO(img_data))
    img.save(out_path)

if __name__=="__main__":
    key, bot_name = get_bot_identity()
    vars = load_variables(bot_name)
    prompt = build_prompt(vars)
    os.makedirs(f"images/{key}", exist_ok=True)
    out_file = f"images/{key}/latest.png"
    gen_image(prompt, out_file)
    print(f"[{bot_name}] Generated image → {out_file}")
