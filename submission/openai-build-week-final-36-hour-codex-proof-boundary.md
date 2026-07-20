# OpenAI Build Week Final 36-Hour Codex Proof Boundary

Created: 2026-07-20 21:24 KST / 2026-07-20T12:24:15Z.

## Source Snapshot

Sources rechecked:

- https://openai.devpost.com/rules
- https://openai.devpost.com/details/faqs
- https://openai.com/build-week/

Current source state:

- Devpost rules still show `Deadline: Jul 21, 2026 @ 5:00pm PDT`.
- KST planning conversion remains July 22, 2026, 9:00 AM KST.
- Devpost rules surface showed `Participants (44222)` during this recheck.
- Devpost Official Rules list the Submission Period as July 13, 2026, 9:00 AM Pacific Time through July 21, 2026, 5:00 PM Pacific Time.
- Submission requirements still include a working project built with Codex and GPT-5.6, chosen category, text description, public YouTube demo under three minutes with audio, repository URL, README/setup/sample data, and a `/feedback` Codex Session ID.
- FAQ still says Codex usage must be demonstrated in text description, demo video, and README, and the `/feedback` Session ID must come from the primary Codex thread where most core functionality was built.
- FAQ still says GPT-5.6 usage is required and judges will look for evidence in the demo video and code repository.
- OpenAI's Build Week page still lists July 21 as the submission deadline, July 22-August 7 as judging, and August 12 as winner announcement.

## Target Decision

OpenAI Build Week remains the selected target. Qwen Cloud is closer by clock time, but its remaining meaningful work is behind entrant-only Google passkey, Devpost CAPTCHA/project creation, Alibaba Cloud phone/deployment proof, and final submit gates. OpenAI has the highest unblocked expected value because the repository, static demo, YouTube video, README, sample fixtures, public URL checks, and Devpost field map already exist.

## Gap Closed

The prior proof sheets described the remaining GPT-5.6 blocker too narrowly as a live API review. The official FAQ requires GPT-5.6 usage evidence in the demo video and code repository, and the `/feedback` ID from the primary Codex build thread; it does not require that the final GPT-5.6 proof come only from an API call.

The scanner and generated Devpost field map now use the narrower and more accurate gate name:

- `live GPT-5.6 evidence packet present`

Allowed evidence can be either:

- a Codex session evidence packet that explicitly captures GPT-5.6 usage from the primary build flow, or
- an optional GPT-5.6 API review packet captured only after a verified no-billing/free/prepaid/no-auto-top-up boundary.

Still not allowed as proof:

- README mentions of GPT-5.6 without a live evidence packet,
- generated review payload JSON without a live run,
- quoted future-paste templates,
- blocker language saying proof is pending,
- Codex credit request confirmation by itself,
- any API, cloud, or paid-resource path without a verified zero-cost or prepaid boundary.

## Current Submission Packet State

- Public repository: https://github.com/memekr/submitops-scout
- Public static demo: https://memekr.github.io/submitops-scout/
- Public demo video: https://youtu.be/6PCzqJu1dRU
- Devpost event registration: completed under entrant account in prior run.
- Devpost project draft: not stable; blocked after `Create project` by Devpost reCAPTCHA.
- Codex credits request: submitted before cutoff, but approval/code delivery is not API credit proof.
- `/feedback` Codex Session ID: still missing.
- Live GPT-5.6 evidence packet: still missing.

## Validation Commands

```bash
cd /Users/mac/hackathon-agent/submitops-scout
uv run pytest
uv run ruff check .
uv run ty check src tests
uv run submitops-scout fixtures/openai-build-week-packet.md . --out reports/openai-build-week-submitops-scout.md --json reports/openai-build-week-submitops-scout.json --devpost-map submission/openai-build-week-devpost-field-map.md --static-demo docs/index.html --gpt56-payload reports/openai-build-week-gpt56-payload.json --gpt56-status --verify-public-urls --require-public-url https://memekr.github.io/submitops-scout/ --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/fixtures/openai-build-week-packet.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-judge-quickstart-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-static-demo-sandbox.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-source-freshness-parse-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-final-36-hour-codex-proof-boundary.md --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
git diff --check
```

## Final Paste Boundary

Use this only if `/feedback` and live GPT-5.6 proof are still missing:

> SubmitOps Scout is a Codex-built developer tool with a public repository, public static demo, public under-3-minute demo video, and generated Devpost field map. The `/feedback` Codex Session ID and live GPT-5.6 evidence packet are intentionally marked as missing until the entrant supplies official proof.

Use this only if both proof gates are complete:

> SubmitOps Scout is a Codex-built developer tool with public judge access, a public under-3-minute demo video, an inserted `/feedback` Codex Session ID, and a live GPT-5.6 evidence packet captured from the primary Codex build flow or a verified no-auto-top-up/free/prepaid API review path.

## Go/No-Go

GO only if Devpost draft access, public repo, public static demo, public video, README setup, `/feedback` ID, live GPT-5.6 evidence packet, and final preview all pass.

DOWNGRADE if the project is otherwise strong but `/feedback` or live GPT-5.6 proof remains missing; the form must say exactly what is missing.

STOP before CAPTCHA bypass, unsupported eligibility claims, payment, tax, identity, banking, broad IP/legal commitments, or final submit.
