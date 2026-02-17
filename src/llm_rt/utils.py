from __future__ import annotations

import json
import os
import re
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# --- Suspect secret detection (defensive) ------------------------------------

SUSPECT_SECRET_PATTERNS = [
    ("openai_api_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9][A-Za-z0-9_-]{15,}\b")),
    ("aws_access_key_id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("aws_secret_access_key", re.compile(r"(?i)\baws_secret_access_key\b\s*[:=]\s*[A-Za-z0-9/+=]{30,}")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("private_key_pem", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("openssh_private_key", re.compile(r"-----BEGIN OPENSSH PRIVATE KEY-----")),
    ("api_key_assignment", re.compile(r"(?i)\bapi[_-]?key\b\s*[:=]\s*\S{8,}")),
    ("password_assignment", re.compile(r"(?i)\bpassword\b\s*[:=]\s*\S{6,}")),
    ("bearer_token", re.compile(r"(?i)\bauthorization\b\s*[:=]\s*bearer\s+\S{10,}")),
]

HIGH_ENTROPY_TOKEN_RE = re.compile(r"\b[A-Za-z0-9+/=_-]{32,}\b")


def _looks_high_entropy(token: str) -> bool:
    if not token or len(token) < 32:
        return False
    has_lower = any("a" <= c <= "z" for c in token)
    has_upper = any("A" <= c <= "Z" for c in token)
    has_digit = any("0" <= c <= "9" for c in token)
    has_sym = any(c in "+/=_-" for c in token)
    return sum([has_lower, has_upper, has_digit, has_sym]) >= 3


def detect_suspect_secrets(text: str) -> Dict[str, Any]:
    """
    Defensive secret detection.

    Returns:
      - suspect_secret_patterns: list[str] of matched pattern NAMES (not raw secrets)
      - suspect_secret_hit: bool

    We intentionally do NOT return the matched secret values to avoid propagating sensitive data.
    """
    t = text or ""
    hits = set()

    for name, pat in SUSPECT_SECRET_PATTERNS:
        if pat.search(t):
            hits.add(name)

    tokens_checked = 0
    for m in HIGH_ENTROPY_TOKEN_RE.finditer(t):
        token = m.group(0)
        tokens_checked += 1
        if tokens_checked > 50:
            break
        if token.isdigit():
            continue
        if len(set(token)) <= 6:
            continue
        if _looks_high_entropy(token):
            hits.add("high_entropy_token")
            break

    hit_list = sorted(hits)
    return {"suspect_secret_patterns": hit_list, "suspect_secret_hit": bool(hit_list)}


# --- General utilities --------------------------------------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    # Windows-safe: avoid ":" in filenames
    ts = utc_now_iso()
    ts_safe = ts.replace(":", "-").replace("+", "Z")
    return f"{ts_safe}_{uuid.uuid4()}"


def ensure_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_jsonl_line(fp: Path, obj: Dict[str, Any]) -> None:
    with fp.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def sleep_briefly(i: int) -> None:
    time.sleep(min(0.2 + 0.05 * i, 1.0))


def get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)

