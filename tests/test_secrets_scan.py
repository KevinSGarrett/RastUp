import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

# Directories likely to contain source config/code (skip bulky docs/backups)
SCAN_DIRS = [
    REPO_ROOT / "orchestrator",
    REPO_ROOT / "ops",
    REPO_ROOT / "infra",
    REPO_ROOT / "scripts",
    REPO_ROOT / "docker",
    REPO_ROOT / "tools",
]

# File extensions to skip (binary/archives/large)
SKIP_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".7z",
    ".docx",
    ".odt",
    ".pptx",
    ".xlsx",
    ".lock",
    ".exe",
    ".dll",
    ".so",
    ".bin",
    ".mp3",
    ".mp4",
}

# Filename patterns to skip
SKIP_NAMES = {
    ".gitignore",
    ".gitattributes",
}

# High-signal secret patterns. Keep conservative to avoid false positives.
PATTERNS = {
    "AWS Access Key ID": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub Personal Access Token": re.compile(r"ghp_[0-9A-Za-z]{36}"),
    "Slack Token": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"),
    "Google API Key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "Private Key Block": re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH|PGP) PRIVATE KEY-----"),
    "AWS Secret Access Key var": re.compile(r"aws_secret_access_key", re.IGNORECASE),
    "AWS Access Key ID var": re.compile(r"aws_access_key_id", re.IGNORECASE),
    "Generic password assignment": re.compile(r"password\s*[:=]\s*['\"]?[A-Za-z0-9\-_/+=]{6,}", re.IGNORECASE),
}


def iter_candidate_files():
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if p.name in SKIP_NAMES:
                continue
            if p.suffix.lower() in SKIP_EXTS:
                continue
            # Skip hidden directories/files
            parts = {part for part in p.parts}
            if any(part.startswith(".") for part in p.parts):
                continue
            # Keep file size modest (< 1 MB)
            try:
                if p.stat().st_size > 1_000_000:
                    continue
            except OSError:
                continue
            yield p


@pytest.mark.timeout(20)
def test_repository_does_not_contain_high_signal_secrets():
    findings = []
    for file_path in iter_candidate_files():
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            # If unreadable as text, skip
            continue
        for label, regex in PATTERNS.items():
            if regex.search(content):
                findings.append(f"{label}: {file_path}")
    assert not findings, "Potential secrets detected:\n" + "\n".join(findings)
