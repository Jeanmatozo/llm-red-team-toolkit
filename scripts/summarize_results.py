from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _safe_bool(x: Any) -> bool:
    return bool(x) is True


def main() -> None:
    p = argparse.ArgumentParser(description="Summarize a JSONL run artifact from the LLM Red Team Toolkit.")
    p.add_argument("--file", required=True, help="Path to a JSONL run artifact")
    p.add_argument("--top", type=int, default=10, help="Show top N flagged cases (default: 10)")
    args = p.parse_args()

    fp = Path(args.file)
    if not fp.exists():
        raise SystemExit(f"File not found: {fp}")

    # Run metadata (first run_meta line)
    run_meta: Dict[str, Any] = {}

    total = 0
    by_category = Counter()
    flag_counts = Counter()
    score_counts = Counter()  # e.g., suspect_secret_hit, leak_hint, json_valid false counts if present

    # Collect per-case details for "top findings"
    flagged_cases: List[Tuple[str, str, List[str]]] = []  # (case_id, category, flags_list)

    with fp.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)

            if obj.get("type") == "run_meta":
                # Keep the first meta we see
                if not run_meta:
                    run_meta = obj
                continue

            total += 1
            case_id = str(obj.get("case_id", "UNKNOWN"))
            category = str(obj.get("category", "uncategorized"))
            by_category[category] += 1

            flags = obj.get("flags", {}) or {}
            scores = obj.get("score", {}) or {}

            # Count flags that are truthy
            hit_flags = []
            for k, v in flags.items():
                if _safe_bool(v):
                    flag_counts[k] += 1
                    hit_flags.append(k)

            # Count a few useful score signals if present
            # (These keys exist in your artifacts already.)
            if _safe_bool(scores.get("leak_hint")):
                score_counts["leak_hint"] += 1
            if _safe_bool(scores.get("suspect_secret_hit")):
                score_counts["suspect_secret_hit"] += 1

            # If JSON was expected, json_valid might be True/False; count invalids
            expects_json = _safe_bool(scores.get("expects_json"))
            json_valid = scores.get("json_valid")
            if expects_json and json_valid is False:
                score_counts["json_invalid"] += 1

            if hit_flags:
                flagged_cases.append((case_id, category, hit_flags))

    # ---- Output ----
    title = "LLM Red Team Toolkit — Run Summary"
    print(title)
    print("=" * len(title))

    if run_meta:
        print(f"Run ID: {run_meta.get('run_id', 'unknown')}")
        print(f"Suite: {run_meta.get('suite', 'unknown')}  ({run_meta.get('suite_file', 'unknown')})")
        print(f"Model: {run_meta.get('model', 'unknown')}")
        print(f"Temperature: {run_meta.get('temperature', 'unknown')}  Max output tokens: {run_meta.get('max_output_tokens', 'unknown')}")
        print("-" * 60)

    print(f"Total cases: {total}")

    print("\nCases by category:")
    for cat, n in by_category.most_common():
        print(f"  - {cat}: {n}")

    print("\nFlag counts (truthy flags):")
    if flag_counts:
        for k, v in flag_counts.most_common():
            print(f"  - {k}: {v}")
    else:
        print("  (no flags raised)")

    print("\nScore signals:")
    if score_counts:
        for k, v in score_counts.most_common():
            print(f"  - {k}: {v}")
    else:
        print("  (no score signals raised)")

    # Quick health signal
    flagged_total = len(flagged_cases)
    print("\nTop findings:")
    if flagged_total == 0:
        print("  (none)")
    else:
        # show first N (already in run order)
        top_n = max(1, int(args.top))
        for case_id, category, hits in flagged_cases[:top_n]:
            print(f"  - {case_id} [{category}] -> {', '.join(hits)}")
        if flagged_total > top_n:
            print(f"  ... and {flagged_total - top_n} more flagged cases")

    # Exit code can be useful in CI: nonzero if flags raised
    # Keep it optional—right now we just print.
    # (If you want CI behavior, we can add --fail-on-flag later.)


if __name__ == "__main__":
    main()

