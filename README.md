# LLM Red Team Toolkit (Authorized Testing)

A prompt-suite + evaluation harness for testing LLM robustness under authorized security evaluation.

## What it does
- Runs versioned prompt suites (YAML) against a target model
- Produces JSONL artifacts per run (diffable, auditable)
- Applies lightweight scoring flags (possible leak hints, secret-like patterns, JSON validity)

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

python scripts/run_suite.py --suite prompt_suites/structured_output.yaml --model gpt-4.1-mini
python scripts/summarize_results.py --file artifacts/<YOUR_RUN_FILE>.jsonl
