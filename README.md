# Media Organizer

A Python media organization tool that sorts files from a safe inbox folder into categorized media folders with clean hybrid filenames.

Built as part of a practical automation portfolio.

---

## Features

- Sorts media files into organized folders
- Supports videos, images, audio, documents, archives, and subtitles
- Safe dry-run preview mode by default
- Automatic folder creation
- Clean hybrid filenames like `IMG_0001_screenshot.png`
- Sequential numbering that does not reuse deleted numbers
- Duplicate detection using file hashes
- Duplicate quarantine folder
- Persistent hash cache using `hash_cache.json`
- Watch mode for monitoring `00_Inbox`
- Unsupported files go to `99_Review`
- Saves media folder path using `settings.json`

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
├── 99_Review/
└── hash_cache.json
```


## Example Renaming
Screenshot 2026-05-28 005501.png
→ IMG_0003_screenshot_2026_05_28_005501.png

Download.mp4
→ VID_0020_download.mp4

POWERELLA V01 PDF DELUXE.zip
→ ARC_0001_powerella_v01_pdf_deluxe.zip


## Duplicate Detection

Media Organizer checks file contents using hashes, not just filenames.

That means duplicate files can be detected even if they have different names.

Duplicates are not deleted. They are moved to:

`99_Review/Duplicates`


## Watch Mode

Watch mode keeps the script running and monitors 00_Inbox.

When a new file appears, the organizer detects it and processes it automatically.

Watch mode? Keep running and monitor 00_Inbox. (y/n) [n]:

Press CTRL + C to stop watch mode.


## How To Use

1. Create a main Media folder.
2. Create a `00_Inbox` folder.
3. Drop files into `00_Inbox`.
4. Run:

```bash
python media_organizer.py
```

5. Choose dry run first:

```text
y
```

6. If the preview looks correct, run again and choose live mode:

```text
n
```


## Supported File Types

Videos: .mp4, .mkv, .mov, .avi, .webm, .wmv

Images: .jpg, .jpeg, .png, .gif, .webp, .bmp, .tif, .tiff

Audio: .mp3, .wav, .flac, .aac, .ogg, .m4a

Documents: .txt, .pdf, .docx, .rtf

Archives: .zip, .rar, .7z

Subtitles: .srt, .ass, .ssa, .vtt


## Future Improvements

- Downloads folder intake watcher
- Smarter filename cleanup
- Metadata-based sorting
- Thumbnail previews
- GUI/Desktop app version
- Silent hover preview for videos
- Open media in default player or VLC
- AI-assisted media search
- Image similarity detection
- Audio fingerprinting
- Video recognition

## Technologies Used

- Python
- os
- shutil
- hashlib
- json
- time

## Author

Created by KDEV-CYBER