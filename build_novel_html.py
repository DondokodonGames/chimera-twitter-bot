import os
import json
from jinja2 import Environment, FileSystemLoader

# Load templates.json
with open("templates.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

# Existing Bot HTML generation logic (not shown) can remain here.

# Novel game HTML generation
format_conf = templates.get("format_config", {})
all_games = templates.get("games", {})

env = Environment(loader=FileSystemLoader("novel_templates"))
template = env.get_template("novel.html.j2")

for game_name, game_info in all_games.items():
    out_dir = os.path.join("public", "novel", game_name)
    os.makedirs(out_dir, exist_ok=True)
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
