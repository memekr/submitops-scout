# OpenAI Build Week Final 42-Hour Proof Lock

Created: 2026-07-20 15:23 KST.

## Source Snapshot

Sources:

- https://openai.devpost.com/
- https://openai.devpost.com/rules
- https://openai.devpost.com/details/faqs
- https://openai.com/build-week/

Current source state:

- Devpost overview still shows `Deadline: Jul 21, 2026 @ 5:00pm PDT`.
- KST planning conversion remains July 22, 2026, 9:00 AM KST.
- Public Devpost counter was 43,706 participants during this recheck.
- Devpost public overview still lists `$100,000 in cash`.
- Devpost requirements still include a working project built with Codex and GPT-5.6, a public under-3-minute YouTube demo with audio, repository URL with README/setup/sample data, and `/feedback` Codex Session ID.
- Devpost still says developer-tool submissions should include installation instructions, supported platforms, and a way for judges to test without rebuilding from scratch.
- FAQ still says the video must be public YouTube, 3 minutes or under, include a working demo, include voiceover, and cover what was built plus Codex and GPT-5.6 usage.
- OpenAI's Build Week page still lists July 13 as challenge open, July 21 as submission deadline, July 22 to August 7 as judging, and August 12 as winner announcement.

## Priority Decision

Status: best local target to finish first.

Qwen Cloud has the nearer deadline, July 21, 2026, 6:00 AM KST, but it is still blocked by entrant-only Google passkey, Devpost CAPTCHA/project creation, Alibaba Cloud phone/deployment proof, and final submit. OpenAI Build Week has the highest sponsor signal and the strongest unblocked local packet, so this run tightens final proof handling instead of idling on Qwen's external gates.

## Gap Closed

The final 52-hour sheet contains quoted future paste templates for the state where live GPT-5.6 proof is later complete. Those quotes are useful for the operator, but a text scanner should not treat quoted future-template language as actual live proof.

The readiness scanner now ignores Markdown blockquote lines when detecting live GPT-5.6 evidence. This keeps the Devpost field map in `DRAFT - DO NOT FINAL SUBMIT` mode until a real live evidence packet appears outside quoted template text.

## Current Submission Packet State

- Public repository: https://github.com/memekr/submitops-scout
- Public static demo: https://memekr.github.io/submitops-scout/
- Public demo video: https://youtu.be/6PCzqJu1dRU
- Devpost registration: completed under entrant account in prior run.
- Devpost project draft: not stable; blocked after `Create project` by Devpost reCAPTCHA.
- Codex credits request: submitted before cutoff, but approval/code delivery is still not API credit proof.
- `/feedback` Codex Session ID: still missing.
- Live GPT-5.6 review evidence: still blocked until a verified free/prepaid/no-auto-top-up API boundary exists.

## Validation Commands

```bash
cd /Users/mac/hackathon-agent/submitops-scout
uv run pytest
uv run ruff check .
uv run ty check src tests
uv run submitops-scout fixtures/openai-build-week-packet.md . --out reports/openai-build-week-submitops-scout.md --json reports/openai-build-week-submitops-scout.json --devpost-map submission/openai-build-week-devpost-field-map.md --static-demo docs/index.html --gpt56-payload reports/openai-build-week-gpt56-payload.json --gpt56-status --verify-public-urls --require-public-url https://memekr.github.io/submitops-scout/ --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/fixtures/openai-build-week-packet.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-judge-quickstart-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-static-demo-sandbox.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-source-freshness-parse-gate.md --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
git diff --check
```

## Final Paste Boundary

Use this only if `/feedback` and live GPT-5.6 proof are still missing:

> SubmitOps Scout is a Codex-built developer tool with a public repository, public static demo, public under-3-minute demo video, and generated Devpost field map. The `/feedback` Codex Session ID and live GPT-5.6 review evidence are intentionally marked as missing until the entrant supplies official proof.

Use this only if both proof gates are complete:

> SubmitOps Scout is a Codex-built developer tool with public judge access, a public under-3-minute demo video, an inserted `/feedback` Codex Session ID, and a live GPT-5.6 review evidence packet captured under a verified no-auto-top-up/free or prepaid boundary.

## Go/No-Go

GO only if Devpost draft access, public repo, public static demo, public video, README setup, `/feedback` ID, live GPT-5.6 proof boundary, and final preview all pass.

DOWNGRADE if the project is otherwise strong but `/feedback` or live GPT-5.6 proof remains missing; the form must say exactly what is missing.

STOP before CAPTCHA bypass, unsupported eligibility claims, payment, tax, identity, banking, broad IP/legal commitments, or final submit.
