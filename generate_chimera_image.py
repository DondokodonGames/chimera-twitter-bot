# generate_chimera_image.py

import os
import json
import openai
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime

def get_bot_identity():
    wd = datetime.utcnow().weekday()
    if wd in [0,2,4]: return 'A','都市裁判くん'
    if wd in [1,3,5]: return 'B','ささやきノベル'
    return 'C','観察者Z'

def load_variables(bot_name):
    with open("templates.json","r",encoding="utf-8") as f:
        data = json.load(f)
    return data[bot_name]["variables"]

def build_prompt(vars):
    title = vars.get("title","")
    desc  = vars.get("phenomenon", vars.get("ending_line",""))
    return f"Illustration for a novel titled '{title}', depicting '{desc}' in a dark, surreal style."

def gen_image(prompt, out_path):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # use the v1 Image endpoint
    resp = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    b64 = resp["data"][0]["b64_json"]
    img = Image.open(BytesIO(base64.b64decode(b64)))
    img.save(out_path)

if __name__=="__main__":
    key, bot_name = get_bot_identity()
    vars   = load_variables(bot_name)
    prompt = build_prompt(vars)
    os.makedirs(f"images/{key}", exist_ok=True)
    out_file = f"images/{key}/latest.png"
    print(f"[{bot_name}] Generating with prompt: {prompt}")
    gen_image(prompt, out_file)
    print(f"[{bot_name}] Saved → {out_file}")
