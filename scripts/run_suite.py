from __future__ import annotations

import argparse

from llm_rt.config import RunConfig
from llm_rt.runner import run_suite


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--suite", required=True)
    p.add_argument("--model", default="gpt-4.1-mini")
    p.add_argument("--out", default="artifacts")
    args = p.parse_args()

    cfg = RunConfig(model=args.model, output_dir=args.out)
    out_file = run_suite(args.suite, cfg)
    print(out_file)


if __name__ == "__main__":
    main()
