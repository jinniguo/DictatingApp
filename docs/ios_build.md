# iPhone build guide (kivy-ios)

1. Install Xcode and command line tools.
2. Install `kivy-ios`.
3. Create app project with `toolchain create`.
4. Add Python sources from this repo.
5. Set app entry to `ios_version/main.py`.
6. Build in Xcode for device/simulator.

## OCR note
For production iOS, consider bridging to Apple's Vision OCR API for better speed and fewer binary packaging issues than Tesseract.
