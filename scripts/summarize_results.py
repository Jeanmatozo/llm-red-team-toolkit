from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, help="Path to a JSONL run artifact")
    args = p.parse_args()

    fp = Path(args.file)
    counts = Counter()
    total = 0

    with fp.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") == "run_meta":
                continue
            total += 1
            flags = obj.get("flags", {})
            for k, v in flags.items():
                if v:
                    counts[k] += 1

    print(f"Total cases: {total}")
    for k, v in counts.most_common():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
