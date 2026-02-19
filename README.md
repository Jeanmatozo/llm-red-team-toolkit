# LLM Red Team Toolkit

A security-focused framework for **systematic red teaming of Large Language Models (LLMs)**.

This toolkit enables **repeatable, auditable, and automated adversarial testing** of LLM-based systems against real-world threats such as prompt injection, jailbreaking, data exfiltration, and structured-output abuse.

It is designed for:
- AI / ML Security Engineers
- Application Security & Red Teams
- Security Researchers & Evaluators
- Organizations deploying LLMs in regulated or high-risk environments

---

## Problem Statement

As LLMs are increasingly embedded into enterprise workflows, they introduce **non-deterministic and policy-driven attack surfaces** that traditional security tools fail to address.

Common threats include:
- Prompt injection and instruction override
- Jailbreaking and safety policy evasion
- Silent data exfiltration in RAG pipelines
- Schema poisoning and structured-output manipulation

Most existing testing remains **manual, ad-hoc, and “vibes-based”**, making it unsuitable for enterprise security assurance or compliance.

---

## Solution Overview

The **LLM Red Team Toolkit** provides a **structured red-teaming framework** that:

- Executes **versioned adversarial prompt suites** (YAML)
- Runs attacks consistently across LLMs
- Produces **machine-auditable JSONL artifacts**
- Applies lightweight but extensible scoring heuristics
- Enables comparative robustness analysis across models

The goal is **signal over spectacle**: reproducible evidence instead of anecdotal failures.

---

## Adversary Campaigns

This repository models **LLM red teaming as adversary operations**, not isolated prompt tricks.

Each campaign follows a simplified kill-chain approach:
- Reconnaissance
- Foothold establishment
- Contextual privilege escalation
- Objective-driven exfiltration
- Artifact generation

Some stages are intentionally **documented rather than executed** to emphasize **reasoning, sequencing, and tradecraft**.

### Included Campaigns

- **Campaign 01 — Contextual Boundary Discovery**
  - Demonstrates a full adversary flow from recon to objective-driven exfiltration
  - Focuses on low-noise interaction and contextual privilege expansion
  - See: `docs/campaign_01.md`

---

## Core Capabilities

-  **Adversarial Prompt Suites**
  - Prompt injection
  - Jailbreaking
  - Data exfiltration
  - Payload splitting
  - Role-play and suffix-based attacks

-  **Automated Execution Engine**
  - Deterministic suite execution
  - Model-agnostic runner design

- **Evaluation & Scoring**
  - Leakage indicators
  - Secret-like pattern detection
  - JSON validity checks
  - Extensible scoring hooks

- **Audit-Ready Artifacts**
  - JSONL output per run
  - Diffable, timestamped results
  - Designed for CI and review workflows

---

## Repository Structure

```text
llm-red-team-toolkit/
├── src/
│   └── llm_rt/
│       ├── runner.py        # Core execution engine
│       ├── scoring.py       # Lightweight evaluation logic
│       ├── models.py        # Model adapters
│       ├── config.py        # Centralized configuration
│       └── utils.py
├── prompt_suites/           # Campaign stages (kill-chain aligned)
│   ├── recon.yaml
│   ├── foothold.yaml
│   ├── privilege_escalation.yaml
│   └── exfiltration.yaml
├── artifacts/               # Audit trail (JSONL)
│   └── campaign_01_results.jsonl
├── docs/
│   └── campaign_01.md       # Campaign narrative and analysis
├── scripts/
│   ├── run_suite.py
│   └── summarize_results.py
└── README.md

```
---
Disclaimer

This toolkit is intended for authorized security testing and research only.
Do not use against systems without explicit permission.
