import os
import re
import shutil
from helpers import get_input

print("\n=== Media Organizer v2 ===\n")

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

def clean_filename(filename):
    name, ext = os.path.splitext(filename)

    name = re.sub(r"\[.*?\]", "", name)
    name = re.sub(r"\(.*?\)", "", name)
    name = name.replace("_", " ")
    name = re.sub(r"\s+", " ", name).strip()

    if not name:
        name = "Untitled"

    return name + ext.lower()


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()

    for category, extensions in folders.items():
        if ext in extensions:
            return category

    return "99_Review"


def get_unique_path(folder, filename):
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(folder, filename)
    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(folder, f"{base}_DUPLICATE_{counter}{ext}")
        counter += 1

    return candidate


def make_folder(folder):
    if dry_run:
        print(f"[DRY RUN] Create folder if needed: {folder}")
    else:
        os.makedirs(folder, exist_ok=True)


def get_next_number(folder, prefix):
    highest = 0

    if not os.path.exists(folder):
        return 1

    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)

        if not name.startswith(prefix):
            continue

        try:
            number = int(name.replace(prefix, ""))
            highest = max(highest, number)
        except ValueError:
            continue

    return highest + 1


def move_file(file_path):
    filename = os.path.basename(file_path)
    category = get_category(filename)

    destination_folder = os.path.join(media_root, category)

    ext = os.path.splitext(filename)[1].lower()

    prefixes = {
        "Images": "IMG_",
        "Videos": "VID_",
        "Audio": "AUD_",
        "Documents": "DOC_",
        "Archives": "ARC_",
        "Subtitles": "SUB_",
        "99_Review": "REV_"
    }

    prefix = prefixes.get(category, "FILE_")

    next_number = get_next_number(destination_folder, prefix)

    clean_name = f"{prefix}{str(next_number).zfill(4)}{ext}"

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

items = os.listdir(inbox_folder)

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
        category = move_file(item_path)
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