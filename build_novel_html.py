import os
import json
from jinja2 import Environment, FileSystemLoader

# Load templates.json
with open("templates.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

# 共通のフォーマット設定
format_conf = templates.get("format_config", {})
all_games = templates.get("games", {})

env = Environment(loader=FileSystemLoader("novel_templates"))

for game_name, game_info in all_games.items():
    out_dir = os.path.join("public", "novel", game_name)
    os.makedirs(out_dir, exist_ok=True)

    # 都市裁判だけ trial.html.j2 を使い、それ以外は従来どおり novel.html.j2
    if game_name == "都市裁判":
        template = env.get_template("trial.html.j2")
        case_data = game_info.get("scenario_variables", {})
        testimonies = game_info.get("testimonies", [])
        evidence_items = game_info.get("evidence_items", [])
        correct_index = game_info.get("correct_index", 0)
        rendered = template.render(
            case=case_data,
            testimonies=testimonies,
            evidence_items=evidence_items,
            correct_index=correct_index
        )
    else:
        template = env.get_template("novel.html.j2")
        rendered = template.render(
            story_title=f"CHIMERA {game_name}",
            logo_image=format_conf.get("logo_image"),
            initial_bgm_state=format_conf.get("initial_bgm_state", True),
            initial_font_class=format_conf.get("initial_font_class", ""),
            font_options=format_conf.get("font_options", []),
            chapters=game_info.get("chapters", [])
        )

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(rendered)
