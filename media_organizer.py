import os
import shutil
from helpers import get_input

print("\n=== Media Organizer v3 ===\n")

# ===== INPUT =====

media_root = get_input(
    "Enter your main media library folder",
    r"C:\Users\K\Desktop\Media"
)

inbox_folder = os.path.join(media_root, "00_Inbox")
review_folder = os.path.join(media_root, "99_Review")

dry_run = get_input(
    "Dry run mode? Preview only, no files moved. (y/n)",
    "y"
).lower() == "y"

# ===== FILE CATEGORIES =====

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
    "99_Review": "REV_"
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

        number_text = name.replace(prefix, "", 1)

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
    ext = os.path.splitext(filename)[1].lower()
    prefix = prefixes.get(category, "FILE_")

    number = planned_numbers[category]
    planned_numbers[category] += 1

    return f"{prefix}{str(number).zfill(4)}{ext}"


def move_file(file_path, planned_numbers):
    filename = os.path.basename(file_path)
    category = get_category(filename)

    destination_folder = os.path.join(media_root, category)
    clean_name = build_clean_name(category, filename, planned_numbers)
    destination_path = os.path.join(destination_folder, clean_name)

    if dry_run:
        print(f"[DRY RUN] {filename} -> {category}/{clean_name}")
    else:
        os.makedirs(destination_folder, exist_ok=True)
        shutil.move(file_path, destination_path)
        print(f"[MOVE] {filename} -> {category}/{clean_name}")

    return category


# ===== RUN =====

if dry_run:
    print("\n[MODE] Dry run enabled. No files will be moved.\n")
else:
    print("\n[MODE] Live run enabled. Files may be moved.\n")

make_folder(review_folder)

for folder_name in folders:
    make_folder(os.path.join(media_root, folder_name))

items = sorted(os.listdir(inbox_folder))
planned_numbers = build_starting_numbers()

if not items:
    print("[DONE] 00_Inbox is empty. Nothing to organize.")
    exit()

processed_count = 0
skipped_folders = 0
category_counts = {}

for item in items:
    item_path = os.path.join(inbox_folder, item)

    if os.path.isdir(item_path):
        print(f"[SKIP] Folder skipped: {item}")
        skipped_folders += 1
        continue

    if os.path.isfile(item_path):
        category = move_file(item_path, planned_numbers)
        category_counts[category] = category_counts.get(category, 0) + 1
        processed_count += 1

print("\n=== Summary ===")
print(f"Files processed: {processed_count}")
print(f"Folders skipped: {skipped_folders}")

if category_counts:
    print("\nBy category:")
    for category, count in sorted(category_counts.items()):
        print(f"- {category}: {count}")

print("\n[DONE] Media organization complete.\n")