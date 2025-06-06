import json
import os
# Placeholder for image generation logic
# Implement actual calls to DALL·E or other image generation services here.

def main():
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    games = data.get("games", {})
    for game_name, game_info in games.items():
        for chapter in game_info.get("chapters", []):
            image_filename = f"assets/img/{game_name}_{chapter['id']}.png"
            chapter['bg_image'] = image_filename
            os.makedirs(os.path.dirname(image_filename), exist_ok=True)
            with open(image_filename, "wb") as img_f:
                img_f.write(b"")  # Empty placeholder

    with open("templates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
