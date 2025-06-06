import json
import os
# import openai  # 実運用ではこちらを有効化して API 呼び出しを行ってください

def generate_scenario(game_type):
    if game_type == "都市裁判":
        # --- ダミーデータの例 ---
        scenario = {
            "episode": 1,
            "case_name": "消えたケーキ事件",
            "case_overview": "人気カフェ「スイートドリーム」で、お客様が注文したケーキが忽然と姿を消した。店長の田中さんは事件の一部始終を目撃したと主張しているが、その証言には矛盾があるようで...",
            "witness_name": "カフェ店長 田中太郎",
            "witness_description": "地元で20年続く老舗カフェの店長。真面目な性格で、お客さんからの信頼も厚い。しかし、時々うっかりミスをすることがある。",
            "witness_icon": "🍰"
        }
        # 証言リスト
        testimonies = [
            {
                "text": "「事件が起きたのは、確か午後2時頃でした。」",
                "contradiction": None,
                "false_reaction": "その時間ではケーキはまだ準備中でしたが...",
                "full_reveal": "",
                "verdict": ""
            },
            {
                "text": "「私はその時、店の奥でケーキを作っていました。」",
                "contradiction": None,
                "false_reaction": "そんな時間には厨房には誰もいませんでしたが...",
                "full_reveal": "",
                "verdict": ""
            },
            {
                "text": "「お客さんの悲鳴を聞いて、急いで店頭に向かったんです。」",
                "contradiction": None,
                "false_reaction": "店頭には誰もいませんでしたが...",
                "full_reveal": "",
                "verdict": ""
            },
            {
                "text": "「時計を見ると、ちょうど3時でした。つまり事件は3時に起きたということです。」",
                "contradiction": "clock",
                "false_reaction": "時計が壊れていたのを忘れていましたが...",
                "full_reveal": "う、うう…バレてしまいましたね。実は…時計を見間違えていたんです。本当は3時15分でした。ケーキ泥棒の件、すみませんでした…",
                "verdict": "有罪 - 店長が時間を誤魔化していたことが判明しました。"
            },
            {
                "text": "「犯人の姿は見ていませんが、きっと常連客の仕業だと思います。」",
                "contradiction": None,
                "false_reaction": "それは根拠のない推測ですね…",
                "full_reveal": "",
                "verdict": ""
            }
        ]
        # 証拠品リスト
        evidence_items = [
            {
                "key": "clock",
                "name": "時計の写真",
                "description": "事件現場で撮影された時計の写真。針は3時15分を指している。",
                "icon": "🕒"
            },
            {
                "key": "receipt",
                "name": "購入レシート",
                "description": "被害者が持っていたケーキ購入のレシート。時刻は15:30と記載されている。",
                "icon": "🧾"
            },
            {
                "key": "witness",
                "name": "目撃証言",
                "description": "近所の住民による目撃証言。「3時頃に怪しい人影を見た」とのこと。",
                "icon": "👁️"
            }
        ]
        correct_index = 3  # 0始まりで、4番目の証言で正解

        return scenario, testimonies, evidence_items, correct_index

    elif game_type == "ささやきノベル":
        # 既存のダミー実装を流用
        scenario = {
            "protagonist_desc": "女の子",
            "present_list": ["花束", "チョコレート", "アクセサリー"],
            "affection_line": "彼女はあなたのチョコレートに微笑んだ。"
        }
        return scenario, None, None, None

    elif game_type == "観測者Z":
        scenario = {
            "room_description": "薄暗い倉庫の中、錆びた扉がわずかに開いている。",
            "escape_steps": "ドライバーで通気口を外し、鍵を使って扉を開ける。"
        }
        return scenario, None, None, None

    return {}, None, None, None

def main():
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    games = data.get("games", {})
    for game_name in games.keys():
        scenario, testimonies, evidence_items, correct_index = generate_scenario(game_name)
        data["games"][game_name]["scenario_variables"] = scenario

        if game_name == "都市裁判":
            data["games"][game_name]["testimonies"] = testimonies
            data["games"][game_name]["evidence_items"] = evidence_items
            data["games"][game_name]["correct_index"] = correct_index

    with open("templates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
