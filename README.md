# DictatingApp (Python, Android + iPhone)

This repository contains two Python app variants for helping middle school students practice English/Chinese textbook dictation by taking photos of textbook pages.

- `android_version/` – Kivy app + Android packaging notes.
- `ios_version/` – Kivy app + iOS packaging notes.
- `shared/` – Shared OCR and text preparation logic.

## Core workflow
1. Take a photo of a textbook page.
2. OCR extracts Chinese and English text.
3. App splits text into short dictation sentences.
4. Built-in speech synthesis reads sentence-by-sentence.
5. Student writes what they hear and can replay each sentence.

## Quick start (desktop simulation)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python android_version/main.py
```

> You can also run `python ios_version/main.py`; both use the same shared Python logic.

## Packaging summary

### Android
- Recommended: Buildozer + python-for-android.
- Main entrypoint: `android_version/main.py`.
- Add `tesseract` binary/data in your Android build if you want fully on-device OCR.

### iOS
- Recommended: `kivy-ios` toolchain.
- Main entrypoint: `ios_version/main.py`.
- Use native iOS OCR bridges (Vision framework) for production-level OCR performance.

## Notes
- The included OCR pipeline uses `pytesseract` for a pure-Python workflow.
- For production mobile apps, consider replacing OCR with cloud OCR or native APIs for better speed and accuracy.
