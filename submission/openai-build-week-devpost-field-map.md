# OpenAI Build Week Devpost Field Map

Generated: 2026-07-20T06:26:40+00:00
Status: DRAFT - DO NOT FINAL SUBMIT

## Source Snapshot

- Event: OpenAI Build Week Packet
- Event URL: https://openai.devpost.com/
- Deadline: July 21, 2026, 5:00 PM PT, per Devpost rules.
- Captured at: 2026-07-20T06:26:36+00:00

## Core Fields

- Project title: SubmitOps Scout: Codex-Powered Submission Command Center
- Category: Developer Tools
- Short description: SubmitOps Scout helps builders turn hackathon rules and a project repository into a ready-to-submit packet: evidence scan, eligibility gates, proof links, Devpost copy, validation commands, and exact blockers.
- Repository URL: https://github.com/memekr/submitops-scout
- Demo video URL: https://youtu.be/6PCzqJu1dRU
- /feedback Codex Session ID: BLOCKED: paste /feedback Codex Session ID from primary build thread
- Live GPT-5.6 review evidence: BLOCKED: run live GPT-5.6 review only after verified no-billing/free-credit boundary

## Live Devpost State

- Event registration and draft-access evidence found in submission/openai-build-week-devpost-draft-access-recheck.md, submission/openai-build-week-devpost-registration-gate.md.
- Project draft creation/access: BLOCKED by Devpost reCAPTCHA after `Create
  project`; direct edit access is not stable until the entrant completes the
  visible CAPTCHA and the draft preview is checked.


## Codex Credits State

- Request status: Submitted; approval/code delivery pending.
- Boundary: Do not treat this as OpenAI API credit proof.


## Public URL Verification

- PASS: reachable https://github.com/memekr/submitops-scout - HTTP 200
- PASS: reachable https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json - HTTP 200
- PASS: reachable https://memekr.github.io/submitops-scout/ - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/fixtures/openai-build-week-packet.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-judge-quickstart-gate.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-static-demo-sandbox.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-source-freshness-parse-gate.md - HTTP 200
- PASS: absent https://raw.githubusercontent.com/memekr/submitops-scout/main/.env - HTTP 404


## Project Description

The tool parses competition source facts, scans a local project for submission evidence, maps requirements to proof, generates a readiness packet, and refuses unsupported claims. Missing public video, missing `/feedback` Session ID, secret findings, or unreviewed rules become explicit `downgrade` or `stop` statuses instead of optimistic submission copy.

## Codex and GPT-5.6 Usage

Codex was used to build the Python/uv CLI, source packet parser, repository
evidence scanner, readiness gate, tests, and generated submission artifacts.
The project includes a GPT-5.6 Responses API review payload generator so a
verified no-billing live review can check the final packet for unsupported
claims before Devpost submission. Current live evidence gate: BLOCKED: run live GPT-5.6 review only after verified no-billing/free-credit boundary.

## Judge Testing Instructions

```bash
uv sync --all-groups
uv run submitops-scout fixtures/openai-build-week-packet.md . \
  --out reports/openai-build-week-submitops-scout.md \
  --json reports/openai-build-week-submitops-scout.json \
  --devpost-map submission/openai-build-week-devpost-field-map.md \
  --gpt56-payload reports/openai-build-week-gpt56-payload.json \
  --gpt56-status
uv run pytest
uv run ruff check .
uv run ty check src tests
```

## Rubric Fit

- Technological implementation: non-trivial CLI, structured packets, tests,
  secret scan, and explicit go/downgrade/stop decisioning.
- Design: runnable developer-tool workflow with generated Markdown/JSON outputs.
- Potential impact: helps hackathon builders avoid missing proof, stale rules,
  and unsupported final-submission claims.
- Quality of idea: applies Codex to the real last-mile submission workflow that
  this hackathon itself requires.

## Why It Can Win

It is a practical Codex-native developer tool with a live deadline use case. Instead of only generating code, it helps teams ship truthful, judge-ready submissions under pressure.

## Current Blockers

- live GPT-5.6 review evidence present
- /feedback Session ID present
