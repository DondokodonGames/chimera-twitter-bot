import json
import os
# Placeholder script for generating music for each game and chapter.
# Implement actual API calls to music generation service here.

def main():
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    games = data.get("games", {})
    for game_name, game_info in games.items():
        for chapter in game_info.get("chapters", []):
            music_filename = f"assets/audio/{game_name}_{chapter['id']}.mp3"
            chapter['bgm'] = music_filename
            os.makedirs(os.path.dirname(music_filename), exist_ok=True)
            with open(music_filename, "wb") as mf:
                mf.write(b"")  # Empty placeholder

    with open("templates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
