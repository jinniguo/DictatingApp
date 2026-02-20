"""Reusable Kivy App used by both Android and iOS variants."""

from __future__ import annotations

from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from plyer import camera, filechooser, tts

from shared.ocr_dictation import run_ocr, split_into_dictation_lines


class DictationRoot(BoxLayout):
    def __init__(self, platform_name: str, **kwargs):
        super().__init__(orientation="vertical", spacing=8, padding=8, **kwargs)
        self.platform_name = platform_name
        self.image_path = Path("captured_textbook.jpg")
        self.dictation_lines = []
        self.current_index = 0

        self.status = Label(
            text=f"{platform_name} version: take a textbook photo to begin",
            size_hint_y=None,
            height=50,
        )
        self.add_widget(self.status)

        controls = BoxLayout(size_hint_y=None, height=50, spacing=6)
        btn_camera = Button(text="Take Photo")
        btn_camera.bind(on_release=lambda *_: self.take_photo())
        controls.add_widget(btn_camera)

        btn_file = Button(text="Choose Image")
        btn_file.bind(on_release=lambda *_: self.choose_image())
        controls.add_widget(btn_file)

        btn_ocr = Button(text="Run OCR")
        btn_ocr.bind(on_release=lambda *_: self.process_ocr())
        controls.add_widget(btn_ocr)
        self.add_widget(controls)

        dictation_controls = BoxLayout(size_hint_y=None, height=50, spacing=6)
        btn_play = Button(text="Read Current")
        btn_play.bind(on_release=lambda *_: self.read_current())
        dictation_controls.add_widget(btn_play)

        btn_next = Button(text="Next")
        btn_next.bind(on_release=lambda *_: self.next_line())
        dictation_controls.add_widget(btn_next)

        btn_restart = Button(text="Restart")
        btn_restart.bind(on_release=lambda *_: self.restart())
        dictation_controls.add_widget(btn_restart)
        self.add_widget(dictation_controls)

        self.editor = TextInput(readonly=True, multiline=True)
        scroll = ScrollView()
        scroll.add_widget(self.editor)
        self.add_widget(scroll)

    def take_photo(self):
        self.status.text = "Opening camera..."
        camera.take_picture(filename=str(self.image_path), on_complete=self._photo_complete)

    def _photo_complete(self, path):
        self.status.text = f"Photo saved: {path}"

    def choose_image(self):
        chosen = filechooser.open_file(title="Select textbook image")
        if chosen:
            self.image_path = Path(chosen[0])
            self.status.text = f"Using image: {self.image_path.name}"

    def process_ocr(self):
        if not self.image_path.exists():
            self.status.text = "No image found. Take photo or choose image first."
            return

        try:
            raw_text = run_ocr(self.image_path)
            self.dictation_lines = split_into_dictation_lines(raw_text)
            self.current_index = 0
            self._refresh_textbox()
            self.status.text = f"OCR complete: {len(self.dictation_lines)} lines ready"
        except Exception as exc:  # noqa: BLE001
            self.status.text = f"OCR failed: {exc}"

    def _refresh_textbox(self):
        if not self.dictation_lines:
            self.editor.text = ""
            return

        rows = []
        for line in self.dictation_lines:
            marker = "👉 " if line.index - 1 == self.current_index else "   "
            rows.append(f"{marker}{line.index}. [{line.language}] {line.text}")
        self.editor.text = "\n".join(rows)

    def read_current(self):
        if not self.dictation_lines:
            self.status.text = "No lines to read. Run OCR first."
            return

        line = self.dictation_lines[self.current_index]
        tts.speak(line.text)
        self.status.text = f"Reading line {line.index}/{len(self.dictation_lines)}"

    def next_line(self):
        if not self.dictation_lines:
            self.status.text = "No lines available."
            return

        self.current_index = (self.current_index + 1) % len(self.dictation_lines)
        self._refresh_textbox()
        Clock.schedule_once(lambda *_: self.read_current(), 0.1)

    def restart(self):
        self.current_index = 0
        self._refresh_textbox()
        self.status.text = "Restarted to first line"


class DictationApp(App):
    def __init__(self, platform_name: str, **kwargs):
        super().__init__(**kwargs)
        self.platform_name = platform_name

    def build(self):
        self.title = f"Textbook Dictation ({self.platform_name})"
        return DictationRoot(platform_name=self.platform_name)
