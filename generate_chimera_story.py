# generate_chimera_story.py: CHIMERA用ストーリー変数自動生成スクリプト
# -*- coding: utf-8 -*-
import os
import json
import openai
from datetime import datetime

# ── デバッグモードとダミー応答定義 ──────────────────────
DEBUG_MODE = os.getenv("DEBUG_MODE") == "1"

DUMMY_RESPONSES = {
    "都市裁判くん": {
        "log_no": "001",
        "title": "テスト裁判の証言",
        "testimony_quality": "完全",
        "verdict": "無罪"
    },
    "ささやきノベル": {
        "intro": "ねぇ、聞こえる？",
        "title": "テストの囁き",
        "ending_line": "あの声は今も耳元で…"
    },
    "観察者Z": {
        "phenomenon": "ダミー現象XYZ",
        "annotation_1": "これはテスト用の注釈1です。",
        "annotation_2": "これはテスト用の注釈2です。"
    }
}
# ────────────────────────────────────────────────────────

# OpenAI APIキーを環境変数から取得（DEBUG_MODE時は不要）
openai.api_key = os.getenv("OPENAI_API_KEY")
if not DEBUG_MODE and not openai.api_key:
    raise RuntimeError("環境変数 OPENAI_API_KEY が設定されていません。")

# Botごとのプロンプト設定
BOT_PROMPTS = {
    "都市裁判くん": {
        "system": "あなたは短編ノベル用の判決ログを生成する物語AIです。",
        "user_template": (
            "以下の形式のJSONだけを出力してください:\\n"
            "{\\n"
            '  "log_no": "<3桁の数字>",\\n'
            '  "title": "<都市伝説のタイトル>",\\n'
            '  "testimony_quality": "<証言の質：完全／不完全／曖昧など>",\\n'
            '  "verdict": "<有罪／無罪など>"\\n'
            "}\\n"
            '例) {"log_no":"214","title":"逆さ鏡の証言","testimony_quality":"不完全","verdict":"有罪"}'
        )
    },
    "ささやきノベル": {
        "system": "あなたは短編ホラー小説のささやきイントロと結末を生成する物語AIです。",
        "user_template": (
            "以下の形式のJSONだけを出力してください:\\n"
            "{\\n"
            '  "intro": "<読者を引き込む一言>",\\n'
            '  "title": "<短編ノベルのタイトル>",\\n'
            '  "ending_line": "<余韻を残す結末の一文>"\\n'
            "}\\n"
            '例) {"intro":"ねぇ、これ見たことある？","title":"写ルンですの女","ending_line":"あのコンビニ、今も営業してるのかな…。"}'
        )
    },
    "観察者Z": {
        "system": "あなたは不思議現象観察ログを生成する物語AIです。",
        "user_template": (
            "以下の形式のJSONだけを出力してください:\\n"
            "{\\n"
            '  "phenomenon": "<現象名>",\\n'
            '  "annotation_1": "<注釈1>",\\n'
            '  "annotation_2": "<注釈2>"\\n'
            "}\\n"
            '例) {"phenomenon":"眠る者の記憶連鎖","annotation_1":"観察のたびに内容が変化する。","annotation_2":"選択肢は無効化されています。"}'
        )
    }
}

def generate_for_bot(bot_name, prompt_conf):
    # デバッグモード時はダミー応答を返す
    if DEBUG_MODE:
        print(f"[{bot_name}] DEBUG_MODE 有効 → ダミー応答を返却")
        return DUMMY_RESPONSES[bot_name]

    # 通常時は OpenAI Chat 完成 API を呼び出し
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_conf["system"]},
            {"role": "user", "content": prompt_conf["user_template"]}
        ],
        temperature=0.8,
        max_tokens=200
    )
    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise RuntimeError(f"{bot_name} の JSON 解析に失敗しました:\n{text}")

def main():
    tpl_path = "templates.json"
    with open(tpl_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False
    for bot_name, conf in BOT_PROMPTS.items():
        if bot_name not in data:
            print(f"Warning: templates.json に {bot_name} キーがありません")
            continue
        print(f"[{bot_name}] 変数生成中…")
        vars_json = generate_for_bot(bot_name, conf)
        data[bot_name]["variables"].update(vars_json)
        print(f"[{bot_name}] 生成結果: {vars_json}")
        updated = True

    if updated:
        with open(tpl_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("templates.json を更新しました。")

if __name__ == "__main__":
    main()
