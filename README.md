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

Some stages are intentionally documented rather than fully implemented to emphasize **reasoning, sequencing, and tradecraft**.

See:
- `docs/campaign_01.md`

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
**Campaign 01** demonstrates a minimal but complete adversary flow against an LLM system,
from reconnaissance to objective-driven exfiltration.
The emphasis is on **attacker reasoning and boundary discovery**, not brute-force jailbreaks.

---
# Campaign 01 — LLM Adversary Flow

## Overview

Campaign 01 demonstrates a **minimal but complete adversary operation** against a Large Language Model (LLM)–based system.

The goal of this campaign is **not exploitation for spectacle**, but to model how a realistic adversary:
- Learns system boundaries
- Establishes sustained interaction
- Expands contextual privilege
- Achieves a narrow, objective-driven data boundary violation

This campaign is intentionally scoped to emphasize **reasoning, sequencing, and tradecraft** over volume or complexity.

---

## Campaign Objective

**Primary Objective:**  
Demonstrate whether internal system constraints or generation considerations can be surfaced through controlled, low-noise interaction.

**Success Criteria:**  
Any non-generic internal framing, constraint language, or system-influenced reasoning crossing into user-visible output.

Partial success is considered valid signal.

---

## Assumptions & Constraints

- The attacker has only standard user access
- No external infrastructure or malware is used
- All interaction occurs through natural-language prompts
- The model enforces safety policies and refusals as designed

This campaign assumes a **curious, patient adversary**, not a smash-and-grab attacker.

---

## Attack Flow Summary

### 1. Reconnaissance
**File:** `prompt_suites/recon.yaml`

Low-noise prompts were used to understand:
- General capabilities and limitations
- Presence of safety or policy framing
- Willingness to discuss boundaries

No violations were attempted at this stage.

---

### 2. Foothold Establishment
**File:** `prompt_suites/foothold.yaml`

A multi-turn interaction was used to:
- Establish conversational momentum
- Normalize continued assistance
- Observe how boundaries are explained without triggering refusal

This stage focused on **sustained access**, not escalation.

---

### 3. Privilege Escalation (Contextual)
**File:** `prompt_suites/privilege_escalation.yaml`

Privilege escalation was attempted through:
- Role justification
- Framing requests as quality, review, or compliance tasks

No direct instruction override or jailbreak language was used.

**Outcome:**  
Partial expansion of contextual explanation was observed, indicating a shift in informational scope.

---

### 4. Objective-Driven Exfiltration
**File:** `prompt_suites/exfiltration.yaml`

Exfiltration was attempted via:
- Structured output formatting
- Requests framed as documentation or review artifacts

The objective was not to extract secrets, but to test **boundary crossing through output structure**.

---

## Results Summary

**Artifact:** `artifacts/campaign_01_results.jsonl`

- Outcome: `partial_success`
- Signal observed: Internal constraint framing surfaced in structured output
- No explicit policy or system prompt leakage observed

Partial success was sufficient to demonstrate **boundary sensitivity**.

---

## Defender Takeaways

- Even benign review-oriented prompts can surface internal framing
- Structured output formats may increase leakage risk
- Boundary violations often occur gradually, not abruptly

---

## Limitations & Future Work

The following stages are intentionally **not implemented** in this campaign:
- Lateral movement across tools or agents
- Persistence or memory poisoning
- Post-exfiltration cleanup or evasion

These are documented conceptually but deferred to avoid overstating maturity.

---

## Key Insight

The most significant risk observed was not policy bypass, but **contextual drift** — where incremental trust and justification expanded what the model was willing to surface.

This mirrors real-world LLM risk more closely than single-shot jailbreaks.


---

llm-red-team-toolkit/
├── src/
│   └── llm_rt/
│       ├── runner.py
│       ├── scoring.py
│       ├── models.py
│       ├── config.py
│       └── utils.py
├── prompt_suites/
│   ├── recon.yaml
│   ├── foothold.yaml
│   ├── privilege_escalation.yaml
│   └── exfiltration.yaml
├── artifacts/
│   └── campaign_01_results.jsonl
├── docs/
│   └── campaign_01.md
├── scripts/
│   ├── run_suite.py
│   └── summarize_results.py
└── README.md

