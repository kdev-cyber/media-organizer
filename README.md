# Media Organizer

A safe Python command-line tool that organizes files from a `00_Inbox` folder into media categories such as Videos, Images, Audio, Documents, Archives, and Subtitles.

This project focuses on safe automation: previewing actions before moving files, avoiding filename collisions, detecting duplicates, and keeping a log of each run.

## Features

* Sorts files from `00_Inbox` into organized folders
* Supports Videos, Images, Audio, Documents, Archives, and Subtitles
* Sends unknown file types to `99_Review`
* Dry run mode previews changes without moving files
* Builds a full organization plan before applying changes
* Requires `ORGANIZE` confirmation before live moves
* Uses numbered, cleaned filenames
* Continues numbering from existing files
* Detects duplicate files using file hashes
* Prevents destination filename collisions
* Saves an organizer log after each run

## Folder Structure

The tool expects a media folder like this:

```text
Media/
├── 00_Inbox/
├── Videos/
├── Images/
├── Audio/
├── Documents/
├── Archives/
├── Subtitles/
└── 99_Review/
```

Files should be placed inside `00_Inbox` before running the organizer.

## Example Output

```text
=== Media Organizer v6 ===

[MODE] Dry run enabled. No files will be moved.

=== Organization Plan ===
[DRY RUN] clip.mp4 -> Videos/VID_0001_clip.mp4
[DRY RUN] photo.jpg -> Images/IMG_0001_photo.jpg

=== Summary ===
Files previewed: 2
Folders skipped: 0

By category:
- Images: 1
- Videos: 1

[LOG] Saved organizer log: C:\Users\K\Desktop\Media\organizer_log.txt
[DONE] Media organization complete.
```

## Safety Features

The organizer is designed to avoid accidental damage.

Dry run mode is enabled by default, so files are previewed before anything is moved.

Live mode requires typing:

```text
ORGANIZE
```

before any files are moved.

The tool also checks for duplicate files and avoids overwriting existing destination filenames.

## How to Run

Run the script from the project folder:

```bash
python media_organizer.py
```

Then follow the prompts:

```text
Enter your main media library folder [C:\Users\K\Desktop\Media]:
Dry run mode? Preview only, no files moved. (y/n) [y]:
```

Press Enter to use the default media folder and dry run mode.

## Logging

Each run saves a log file in the media folder:

```text
organizer_log.txt
```

The log records the mode used, planned file moves, skipped folders, and final summary.

## Project Goals

This project demonstrates practical Python automation skills:

* File and folder handling
* Safe command-line workflows
* User input validation
* Duplicate detection with hashing
* Collision-safe file naming
* Dry run previews
* Logging
* Git/GitHub project workflow

## Tech Used

* Python
* Standard library modules:

  * `os`
  * `shutil`
  * `hashlib`
  * `json`
  * `datetime`

## Status

Portfolio-ready command-line automation project.
