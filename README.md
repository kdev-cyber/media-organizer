# Media Organizer

A Python media organization tool that sorts files from a safe inbox folder into categorized media folders with clean numbered filenames.

Built as part of a practical automation portfolio.

---

## Features

- Sorts media files into organized folders
- Supports videos, images, audio, documents, archives, and subtitles
- Uses a safe dry-run preview mode before moving files
- Creates destination folders automatically
- Renames files with clean numbered names like `IMG_0001.jpg`
- Avoids messy download names like `Download (1).mp4`
- Sends unsupported files to `99_Review`
- Saves previous input settings using `settings.json`

---

## Folder Structure

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

---

## Example Renaming

```text
1000024969.jpg
→ IMG_0001.jpg

Download.mp4
→ VID_0001.mp4

POWERELLA V01 PDF DELUXE.zip
→ ARC_0001.zip
```

---

## Supported File Types

### Videos

`.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`, `.wmv`

### Images

`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.tif`, `.tiff`

### Audio

`.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`

### Documents

`.txt`, `.pdf`, `.docx`, `.rtf`

### Archives

`.zip`, `.rar`, `.7z`

### Subtitles

`.srt`, `.ass`, `.ssa`, `.vtt`

---

## How To Use

1. Create a main `Media` folder.

2. Inside it, create:

```text
00_Inbox
```

3. Drop files into `00_Inbox`.

4. Run the script:

```bash
python media_organizer.py
```

5. Choose dry run mode first:

```text
y
```

6. If the preview looks correct, run again and choose live mode:

```text
n
```

---

## Safety Features

- Dry run mode previews changes before moving files
- Files are sorted from `00_Inbox` only
- Unsupported files go to `99_Review`
- Numbered filenames avoid overwrite confusion
- Existing files are not reused or reshuffled

---

## Current Naming System

The organizer uses category prefixes:

```text
IMG_0001.jpg
VID_0001.mp4
AUD_0001.mp3
DOC_0001.pdf
ARC_0001.zip
SUB_0001.srt
REV_0001.unknown
```

Numbers continue upward instead of reusing deleted numbers.

---

## Future Improvements

- Smarter filename cleanup
- ZIP extraction and inspection
- Metadata-based sorting
- Downloads folder watcher
- Duplicate detection by file hash
- GUI/Desktop app version
- Thumbnail previews
- Silent hover preview for videos
- Open media in default player or VLC
- AI-assisted media search
- Image similarity detection
- Audio fingerprinting
- Video recognition

---

## Technologies Used

- Python
- os
- shutil
- re
- JSON settings storage

---

## Author

Created by KDEV-CYBER