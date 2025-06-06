import json
import os
# Placeholder script for generating music for each game and chapter.
# Implement actual API calls to music generation service here.

def main():
    # Load templates.json
    with open("templates.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    games = data.get("games", {})
    for game_name, game_info in games.items():
        for chapter in game_info.get("chapters", []):
            # Placeholder: Assign a default or pre-generated BGM path.
            # Replace with calls to actual music generation API.
            music_filename = f"assets/audio/{game_name}_{chapter['id']}.mp3"
            chapter['bgm'] = music_filename
            # Create dummy file if not exists
            os.makedirs(os.path.dirname(music_filename), exist_ok=True)
            with open(music_filename, "wb") as mf:
                mf.write(b"")  # Empty file as placeholder

    # Save updated templates.json
    with open("templates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
