# Android build guide (Buildozer)

1. Install Buildozer dependencies (Linux host).
2. Initialize: `buildozer init`
3. Set in `buildozer.spec`:
   - `title = DictatingAppAndroid`
   - `source.dir = .`
   - `source.include_exts = py,png,jpg,kv,md`
   - `requirements = python3,kivy,plyer,pytesseract,pillow`
   - `android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE`
   - `package.name = dictatingapp`
4. Ensure app entry is `android_version/main.py`.
5. Build APK: `buildozer android debug`.

## OCR note
For offline OCR, bundle Tesseract binaries + language data (`eng`, `chi_sim`) and configure `pytesseract.pytesseract.tesseract_cmd` at runtime.
