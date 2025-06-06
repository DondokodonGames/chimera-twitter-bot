import json
import os
import openai

# Placeholder OpenAI API key setup
# openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_scenario(game_type):
    # Draft prompts based on game_type
    if game_type == "都市裁判":
        prompt = """あなたは“逆転裁判”風の短編ノベルライターです。
以下の要素を満たす物語構造を作成してください。
• 事件名
• 証言文
• 証拠品
• 矛盾点
• 判決
JSON形式で返してください:
{
  "case_name": "イベント名テキスト",
  "testimony_text": "目撃者の証言文",
  "evidence_item": "証拠品名",
  "contradiction_point": "矛盾点を示す一文",
  "verdict": "判決文"
}
"""
    elif game_type == "ささやきノベル":
        prompt = """あなたは“ささやきノベル”のシナリオライターです。
主人公が異性にプレゼントを贈って好感度を上げる短編ストーリーを作成してください。
JSON形式で返してください:
{
  "protagonist_desc": "男の子または女の子のテキスト",
  "present_list": ["花束", "チョコレート", "アクセサリー"],
  "affection_line": "好感度上昇メッセージ"
}
"""
    elif game_type == "観測者Z":
        prompt = """あなたは“観測者Z”というワンシーン脱出ゲームのライターです。
短時間でプレイヤーが脱出できるよう、次の要素をJSON形式で返してください:
{
  "room_description": "部屋の説明文",
  "escape_steps": "脱出手順"
}
"""
    else:
        return {}

    # Placeholder for actual API call
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # result_json = response.choices[0].message.content

    # For now, return dummy data
    if game_type == "都市裁判":
        return {
            "case_name": "夜行バス失踪事件",
            "testimony_text": "被害者が夜行バスに乗ったと証言した。",
            "evidence_item": "バスチケットの半券",
            "contradiction_point": "半券の日付が証言と食い違っている。",
            "verdict": "有罪"
        }
    elif game_type == "ささやきノベル":
        return {
            "protagonist_desc": "女の子",
            "present_list": ["花束", "チョコレート", "アクセサリー"],
            "affection_line": "彼女はあなたのチョコレートに微笑んだ。"
        }
    elif game_type == "観測者Z":
        return {
            "room_description": "薄暗い倉庫の中、錆びた扉がわずかに開いている。",
            "escape_steps": "ドライバーで通気口を外し、鍵を使って扉を開ける。"
        }
    return {}

def main():
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    games = data.get("games", {})
    for game_name in games.keys():
        scenario = generate_scenario(game_name)
        data["games"][game_name]["scenario_variables"] = scenario

        # Embed variables into chapters
        chapters = data["games"][game_name].get("chapters", [])
        for chap in chapters:
            for k, v in scenario.items():
                chap["texts"] = [line.replace(f"{{{{ {k} }}}}", v) for line in chap["texts"]]
                if chap.get("choices"):
                    for choice in chap["choices"]:
                        choice["text"] = choice["text"].replace(f"{{{{ {k} }}}}", v)

    with open("templates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
