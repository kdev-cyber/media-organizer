import json
import os

SETTINGS_FILE = "settings.json"


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {}


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def get_input(prompt, default=""):
    settings = load_settings()

    saved_value = settings.get(prompt, default)

    user_input = input(f"{prompt} [{saved_value}]: ").strip()

    if not user_input:
        user_input = saved_value

    settings[prompt] = user_input
    save_settings(settings)

    return user_input