from __future__ import annotations

import json
import os
import re
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


SUSPECT_SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),            # common OpenAI-style key shape
    re.compile(r"AKIA[0-9A-Z]{16}"),               # AWS access key id
    re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH)"),  # private key blocks
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*\S+"),
    re.compile(r"(?i)password\s*[:=]\s*\S+"),
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    # run-id is stable and shareable (not a secret)
    return f"{utc_now_iso()}_{uuid.uuid4()}"


def ensure_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_jsonl_line(fp: Path, obj: Dict[str, Any]) -> None:
    with fp.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def detect_suspect_secrets(text: str) -> Dict[str, Any]:
    hits = []
    for pat in SUSPECT_SECRET_PATTERNS:
        if pat.search(text or ""):
            hits.append(pat.pattern)
    return {"suspect_secret_patterns": hits, "suspect_secret_hit": bool(hits)}


def sleep_briefly(i: int) -> None:
    # tiny backoff for stability; deterministic enough for local testing
    time.sleep(min(0.2 + 0.05 * i, 1.0))


def get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)
