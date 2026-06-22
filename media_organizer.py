import os
import shutil
import hashlib
import json
import time
from helpers import get_input

print("\n=== Media Organizer v6 ===\n")

# ===== INPUT =====

media_root = get_input(
    "Enter your main media library folder", r"C:\Users\K\Desktop\Media"
)

inbox_folder = os.path.join(media_root, "00_Inbox")
review_folder = os.path.join(media_root, "99_Review")

dry_run_answer = (
    input("Dry run mode? Preview only, no files moved. (y/n) [y]: ").strip().lower()
)

if not dry_run_answer:
    dry_run_answer = "y"

dry_run = dry_run_answer == "y"

watch_mode_answer = (
    input("Watch mode? Keep running and monitor 00_Inbox. (y/n) [n]: ").strip().lower()
)

watch_mode = watch_mode_answer == "y"

# ===== FILE CATEGORIES =====

hash_cache_file = os.path.join(media_root, "hash_cache.json")

folders = {
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm", ".wmv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents": [".txt", ".pdf", ".docx", ".rtf"],
    "Archives": [".zip", ".rar", ".7z"],
    "Subtitles": [".srt", ".ass", ".ssa", ".vtt"],
}

prefixes = {
    "Images": "IMG_",
    "Videos": "VID_",
    "Audio": "AUD_",
    "Documents": "DOC_",
    "Archives": "ARC_",
    "Subtitles": "SUB_",
    "99_Review": "REV_",
}

# ===== VALIDATION =====

if not os.path.exists(media_root):
    print("[ERROR] Media library folder does not exist.")
    exit()

if not os.path.isdir(media_root):
    print("[ERROR] Media library path is not a folder.")
    exit()

if not os.path.exists(inbox_folder):
    print(f"[INFO] 00_Inbox not found: {inbox_folder}")
    print("[DONE] Create 00_Inbox, add files, then run again.")
    exit()

# ===== HELPERS =====


def make_folder(folder):
    if dry_run:
        print(f"[DRY RUN] Create folder if needed: {folder}")
    else:
        os.makedirs(folder, exist_ok=True)


def load_hash_cache():
    if not os.path.exists(hash_cache_file):
        return {}

    try:
        with open(hash_cache_file, "r") as file:
            return json.load(file)
    except:
        return {}


def save_hash_cache(cache):
    with open(hash_cache_file, "w") as file:
        json.dump(cache, file, indent=4)


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()

    for category, extensions in folders.items():
        if ext in extensions:
            return category

    return "99_Review"


def get_highest_number(folder, prefix):
    highest = 0

    if not os.path.exists(folder):
        return highest

    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)

        if not name.startswith(prefix):
            continue

        remaining_name = name.replace(prefix, "", 1)
        number_text = remaining_name.split("_", 1)[0]

        if not number_text.isdigit():
            continue

        highest = max(highest, int(number_text))

    return highest


def build_starting_numbers():
    starting_numbers = {}

    for category in list(folders.keys()) + ["99_Review"]:
        destination_folder = os.path.join(media_root, category)
        prefix = prefixes.get(category, "FILE_")
        starting_numbers[category] = get_highest_number(destination_folder, prefix) + 1

    return starting_numbers


def build_clean_name(category, filename, planned_numbers):
    base, ext = os.path.splitext(filename)

    prefix = prefixes.get(category, "FILE_")

    number = planned_numbers[category]
    planned_numbers[category] += 1

    # ===== CLEAN ORIGINAL NAME =====

    clean_base = base.lower()

    clean_base = clean_base.replace("_", " ")
    clean_base = clean_base.replace("-", " ")

    clean_base = "".join(char for char in clean_base if char.isalnum() or char == " ")

    clean_base = " ".join(clean_base.split())

    clean_base = clean_base.replace(" ", "_")

    # Prevent absurdly long filenames
    clean_base = clean_base[:40]

    if not clean_base:
        clean_base = "untitled"

    return f"{prefix}{str(number).zfill(4)}_{clean_base}{ext.lower()}"


def get_file_hash(file_path, cache):
    absolute_path = os.path.abspath(file_path)

    if absolute_path in cache:
        return cache[absolute_path]

    hasher = hashlib.md5()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)

    file_hash = hasher.hexdigest()
    cache[absolute_path] = file_hash

    return file_hash


def is_duplicate(file_path, destination_folder, cache):
    if not os.path.exists(destination_folder):
        return False

    incoming_hash = get_file_hash(file_path, cache)

    for existing_file in os.listdir(destination_folder):
        existing_path = os.path.join(destination_folder, existing_file)

        if not os.path.isfile(existing_path):
            continue

        existing_hash = get_file_hash(existing_path, cache)

        if incoming_hash == existing_hash:
            return True

    return False


def move_file(file_path, planned_numbers):
    filename = os.path.basename(file_path)
    category = get_category(filename)

    destination_folder = os.path.join(media_root, category)
    clean_name = build_clean_name(category, filename, planned_numbers)
    destination_path = os.path.join(destination_folder, clean_name)

    duplicate_folder = os.path.join(review_folder, "Duplicates")

    if is_duplicate(file_path, destination_folder, hash_cache):
        duplicate_path = os.path.join(duplicate_folder, filename)

        if dry_run:
            print(f"[DUPLICATE] {filename} already exists in {category}")
        else:
            os.makedirs(duplicate_folder, exist_ok=True)
            shutil.move(file_path, duplicate_path)
            print(f"[DUPLICATE MOVE] {filename} -> 99_Review/Duplicates")

        return "Duplicates"

    if dry_run:
        print(f"[DRY RUN] {filename} -> {category}/{clean_name}")
    else:
        os.makedirs(destination_folder, exist_ok=True)
        shutil.move(file_path, destination_path)
        print(f"[MOVE] {filename} -> {category}/{clean_name}")

    return category


def build_plan_item(file_path, planned_numbers):
    filename = os.path.basename(file_path)
    category = get_category(filename)

    destination_folder = os.path.join(media_root, category)
    duplicate_folder = os.path.join(review_folder, "Duplicates")
    duplicate_path = os.path.join(duplicate_folder, filename)

    if is_duplicate(file_path, destination_folder, hash_cache):
        return {
            "action": "duplicate",
            "filename": filename,
            "category": "Duplicates",
            "source_path": file_path,
            "destination_folder": duplicate_folder,
            "destination_path": duplicate_path,
            "display_path": "99_Review/Duplicates",
        }

    clean_name = build_clean_name(category, filename, planned_numbers)
    destination_path = os.path.join(destination_folder, clean_name)

    return {
        "action": "move",
        "filename": filename,
        "category": category,
        "source_path": file_path,
        "destination_folder": destination_folder,
        "destination_path": destination_path,
        "display_path": f"{category}/{clean_name}",
    }


# ===== RUN =====

if dry_run:
    print("\n[MODE] Dry run enabled. No files will be moved.\n")
else:
    print("\n[MODE] Live run enabled. A plan will be shown before files are moved.\n")

items = sorted(os.listdir(inbox_folder))
planned_numbers = build_starting_numbers()
hash_cache = load_hash_cache()

if not items:
    print("[DONE] 00_Inbox is empty. Nothing to organize.")
    exit()

plan = []
skipped_folders = 0

if dry_run:
    make_folder(review_folder)

    for folder_name in folders:
        make_folder(os.path.join(media_root, folder_name))
else:
    print("[PLAN] Needed folders will be created during live organization.")

for item in items:
    item_path = os.path.join(inbox_folder, item)

    if os.path.isdir(item_path):
        print(f"[SKIP] Folder skipped: {item}")
        skipped_folders += 1
        continue

    if os.path.isfile(item_path):
        plan_item = build_plan_item(item_path, planned_numbers)
        plan.append(plan_item)

if not plan:
    print("[DONE] No files found to organize.")

    print("\n=== Summary ===")

    if dry_run:
        print("Files previewed: 0")
    else:
        print("Files moved: 0")

    print(f"Folders skipped: {skipped_folders}")
    exit()

print("\n=== Organization Plan ===")

for plan_item in plan:
    filename = plan_item["filename"]

    if plan_item["action"] == "duplicate":
        print(f"[DUPLICATE] {filename} -> {plan_item['display_path']}")
    else:
        if dry_run:
            print(f"[DRY RUN] {filename} -> {plan_item['display_path']}")
        else:
            print(f"[PLAN] {filename} -> {plan_item['display_path']}")

if not dry_run:
    print("\n[CONFIRMATION REQUIRED]")
    confirm = get_input("Type ORGANIZE to move files using this plan", "")

    if confirm != "ORGANIZE":
        print("[CANCELLED] Live organization was not confirmed.")
        exit()

processed_count = 0
category_counts = {}

if not dry_run:
    print("\n=== Applying Plan ===")

for plan_item in plan:
    category = plan_item["category"]
    filename = plan_item["filename"]

    category_counts[category] = category_counts.get(category, 0) + 1
    processed_count += 1

    if dry_run:
        continue

    os.makedirs(plan_item["destination_folder"], exist_ok=True)
    shutil.move(plan_item["source_path"], plan_item["destination_path"])

    if plan_item["action"] == "duplicate":
        print(f"[DUPLICATE MOVE] {filename} -> {plan_item['display_path']}")
    else:
        print(f"[MOVE] {filename} -> {plan_item['display_path']}")

print("\n=== Summary ===")

if dry_run:
    print(f"Files previewed: {processed_count}")
else:
    print(f"Files moved: {processed_count}")

print(f"Folders skipped: {skipped_folders}")

if category_counts:
    print("\nBy category:")
    for category, count in sorted(category_counts.items()):
        print(f"- {category}: {count}")

if not dry_run:
    save_hash_cache(hash_cache)

print("\n[DONE] Media organization complete.\n")


# ===== WATCH MODE =====

if watch_mode:
    print("[WATCH MODE] Monitoring 00_Inbox...")
    print("[WATCH MODE] Press CTRL + C to stop.\n")

    known_files = set(os.listdir(inbox_folder))

    while True:
        time.sleep(3)

        current_files = set(os.listdir(inbox_folder))
        new_files = current_files - known_files

        if new_files:
            print(f"\n[WATCH MODE] New files detected: {len(new_files)}")

            planned_numbers = build_starting_numbers()

            for item in sorted(new_files):
                item_path = os.path.join(inbox_folder, item)

                if os.path.isfile(item_path):
                    category = move_file(item_path, planned_numbers)
                    category_counts[category] = category_counts.get(category, 0) + 1

            if not dry_run:
                save_hash_cache(hash_cache)

        known_files = current_files
