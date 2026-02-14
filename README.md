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

```
---
## Safety
This repository is for defensive research and authorized testing only.
Do not use it against systems you do not own or have explicit permission to test.

---

## 7) What you will put in your profile

Once this repo exists, your profile item becomes real:

**🔴 LLM Red Team Toolkit (Research / Active Development)**  
- Prompt suites: injection, structured output coercion, convergence, transformation  
- Runner: reproducible execution + JSONL artifacts  
- Scoring: leak hints, secret-like patterns, JSON validity

---

## 8) Next step: I need one decision from you (but I will not block you)

Which interface do you want the toolkit to target first?

1) **OpenAI Responses API** only (simple, already in code above)  
2) Add an **adapter layer** so you can test:
   - OpenAI
   - local models
   - “bring your own HTTP endpoint”

If you do nothing, option (1) is perfect for v0.1.

If you want, paste your preferred repo name and I will tailor the README + suite taxonomy to match your exact profile language.


