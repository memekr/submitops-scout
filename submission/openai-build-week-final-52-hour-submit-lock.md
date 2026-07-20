# OpenAI Build Week Final 52-Hour Submit Lock

Created: 2026-07-20 05:33 KST.

## Source Snapshot

Sources:

- https://openai.devpost.com/
- https://openai.devpost.com/rules
- https://openai.devpost.com/details/faqs
- https://openai.com/build-week/

Current source state:

- Devpost rules list registration through July 21, 2026, 5:00 PM Pacific Time.
- Devpost rules list submissions from July 13, 2026, 9:00 AM Pacific Time through July 21, 2026, 5:00 PM Pacific Time.
- KST planning conversion: July 22, 2026, 9:00 AM KST.
- Public Devpost counter was around 43,170 participants during the July 20 KST scout.
- Prize pool remains $100,000 cash.

## Priority Decision

Status: best target to finish first.

Qwen Cloud is still active until July 21, 2026, 6:00 AM KST, but the remaining steps are entrant-only: Google passkey, Devpost CAPTCHA/project creation, Alibaba Cloud phone/deployment proof, and final submit. OpenAI Build Week has the strongest unblocked local packet and the highest sponsor fit.

## Current Submission Packet State

- Public repository: https://github.com/memekr/submitops-scout
- Public static demo: https://memekr.github.io/submitops-scout/
- Public demo video: https://youtu.be/6PCzqJu1dRU
- Devpost registration: completed under entrant account in prior run.
- Devpost project draft: not stable; blocked after `Create project` by Devpost reCAPTCHA.
- Codex credits request: submitted before cutoff, but approval/code delivery is still not API credit proof.
- `/feedback` Codex Session ID: still missing.
- Live GPT-5.6 review evidence: still blocked until a verified free/prepaid/no-auto-top-up API boundary exists.

## Exact Next Local Step

Do not change core behavior unless a final proof gate fails.

Next local edit if user supplies `/feedback` ID or GPT-5.6 proof:

- Update `submission/openai-build-week-devpost-field-map.md`.
- Update `submission/openai-build-week-draft.md`.
- Re-run the generator command with public URL verification.
- Keep any still-missing proof as `BLOCKED`, not as paste-ready copy.

Prototype modules to inspect only if proof automation needs code:

- `src/submitops_scout/gpt56_adapter.py`
- `src/submitops_scout/core.py`

## Validation Commands

```bash
cd /Users/mac/hackathon-agent/submitops-scout
uv run pytest
uv run ruff check .
uv run ty check src tests
uv run submitops-scout fixtures/openai-build-week-packet.md . --out reports/openai-build-week-submitops-scout.md --json reports/openai-build-week-submitops-scout.json --devpost-map submission/openai-build-week-devpost-field-map.md --static-demo docs/index.html --gpt56-payload reports/openai-build-week-gpt56-payload.json --gpt56-status --verify-public-urls --require-public-url https://memekr.github.io/submitops-scout/ --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/fixtures/openai-build-week-packet.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-judge-quickstart-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-static-demo-sandbox.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-source-freshness-parse-gate.md --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
git diff --check
```

## External Actions Waiting on Entrant

1. Complete Devpost reCAPTCHA after `Create project`.
2. Create or reopen the Devpost project draft.
3. Paste the official `/feedback` Codex Session ID from the primary build thread.
4. Verify whether Codex credits/code arrived; do not treat Codex credits as OpenAI API credit proof.
5. Capture live GPT-5.6 review evidence only after a verified free/prepaid/no-auto-top-up boundary.
6. Preview the final Devpost submission.
7. Click final `Submit project` only after the entrant confirms rules, eligibility, and field accuracy.

## Final Paste Boundary

Use this only if `/feedback` and live GPT-5.6 proof are still missing:

> SubmitOps Scout is a Codex-built developer tool with a public repository, public static demo, public under-3-minute demo video, and generated Devpost field map. The `/feedback` Codex Session ID and live GPT-5.6 review evidence are intentionally marked as missing until the entrant supplies official proof.

Use this only if both proof gates are complete:

> SubmitOps Scout is a Codex-built developer tool with public judge access, a public under-3-minute demo video, an inserted `/feedback` Codex Session ID, and a live GPT-5.6 review evidence packet captured under a verified no-auto-top-up/free or prepaid boundary.

## Go/No-Go

GO only if Devpost draft access, public repo, public static demo, public video, README setup, `/feedback` ID, live GPT-5.6 proof boundary, and final preview all pass.

DOWNGRADE if the project is otherwise strong but `/feedback` or live GPT-5.6 proof remains missing; the form must say exactly what is missing.

STOP before CAPTCHA bypass, unsupported eligibility claims, payment, tax, identity, banking, broad IP/legal commitments, or final submit.
