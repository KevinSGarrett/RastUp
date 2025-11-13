# -*- coding: utf-8 -*-
import json
import tempfile
from pathlib import Path


def test_utf8_literals_and_roundtrip_file_io():
    # Curly quotes, em dash, non-breaking hyphen, check mark
    text = "UTF‑8 smoke — quotes “ok” — em‑dash — symbols ✓"

    # Validate key code points are present
    assert "“" in text and "”" in text, "Curly quotes missing"
    assert "—" in text, "Em dash missing"
    assert "‑" in text, "Non-breaking hyphen missing"
    assert "✓" in text, "Check mark missing"

    # Check representative code points directly
    codepoints = [ord(ch) for ch in ["“", "”", "—", "‑", "✓"]]
    assert codepoints == [0x201C, 0x201D, 0x2014, 0x2011, 0x2713]

    # File write/read roundtrip using explicit UTF-8
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "utf8.txt"
        p.write_text(text, encoding="utf-8")
        read_back = p.read_text(encoding="utf-8")
        assert read_back == text


def test_utf8_json_roundtrip_preserves_characters():
    payload = {"text": "UTF‑8 smoke — quotes “ok” — em‑dash — symbols ✓"}

    dumped = json.dumps(payload, ensure_ascii=False)
    loaded = json.loads(dumped)

    assert loaded["text"] == payload["text"]
    # Ensure characters are not ASCII-escaped in the JSON string
    assert "\\u" not in dumped.lower()
