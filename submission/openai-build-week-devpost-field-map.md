# OpenAI Build Week Devpost Field Map

Generated: 2026-07-15T12:27:44+00:00
Status: DRAFT - DO NOT FINAL SUBMIT

## Source Snapshot

- Event: OpenAI Build Week Packet
- Event URL: https://openai.devpost.com/
- Deadline: July 21, 2026, 5:00 PM PT, per Devpost overview copy.
- Captured at: 2026-07-15T12:27:44+00:00

## Core Fields

- Project title: SubmitOps Scout: Codex-Powered Submission Command Center
- Category: Developer Tools
- Short description: SubmitOps Scout helps builders turn a project repository and hackathon rules into a ready-to-submit packet: eligibility gates, proof links, Devpost drafts, demo scripts, validation commands, and blockers.
- Repository URL: https://github.com/memekr/submitops-scout
- Demo video URL: https://youtu.be/6PCzqJu1dRU
- /feedback Codex Session ID: BLOCKED: paste /feedback Codex Session ID from primary build thread

## Project Description

It reads public competition pages, scans local repo evidence, maps judging criteria to proof, drafts submission copy, and refuses unsupported claims until a human supplies missing account, eligibility, legal, payment, or publication facts.

## Codex and GPT-5.6 Usage

Codex was used to build the Python/uv CLI, source packet parser, repository
evidence scanner, readiness gate, tests, and generated submission artifacts.
The project includes a GPT-5.6 Responses API review payload generator so a
verified no-billing live review can check the final packet for unsupported
claims before Devpost submission.

## Judge Testing Instructions

```bash
uv sync --all-groups
uv run submitops-scout ../submission-packets/openai-build-week.md . \
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

- /feedback Session ID present
