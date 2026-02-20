"""Shared OCR + dictation helpers for Android and iOS variants."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytesseract
from PIL import Image


@dataclass
class DictationLine:
    index: int
    text: str
    language: str


def run_ocr(image_path: str | Path, lang: str = "eng+chi_sim") -> str:
    """Extract raw text from an image using Tesseract OCR."""
    image = Image.open(str(image_path))
    return pytesseract.image_to_string(image, lang=lang)


def _normalize_text(raw_text: str) -> str:
    cleaned = raw_text.replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    return cleaned.strip()


def split_into_dictation_lines(raw_text: str) -> List[DictationLine]:
    """
    Create short bilingual dictation units from OCR text.

    Rules:
    - Split by punctuation/newlines.
    - Keep chunks with at least 2 characters.
    - Label chunk language as 'zh', 'en', or 'mixed'.
    """
    normalized = _normalize_text(raw_text)
    chunks = re.split(r"[\n。！？.!?；;]+", normalized)

    lines: List[DictationLine] = []
    for chunk in chunks:
        text = chunk.strip()
        if len(text) < 2:
            continue

        has_zh = bool(re.search(r"[\u4e00-\u9fff]", text))
        has_en = bool(re.search(r"[A-Za-z]", text))

        if has_zh and has_en:
            language = "mixed"
        elif has_zh:
            language = "zh"
        else:
            language = "en"

        lines.append(DictationLine(index=len(lines) + 1, text=text, language=language))

    return lines
