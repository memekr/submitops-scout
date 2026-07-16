# OpenAI Build Week Judge Quickstart Gate

Generated KST: 2026-07-16 21:14:08 KST

## Selected Target

OpenAI Build Week remains the active target for this run. Qwen Cloud is still
closer by deadline, but its remaining steps require human-only Devpost image
reCAPTCHA and Alibaba Cloud phone verification. OpenAI had an unblocked
judge-readiness gap: the public repository needed a self-contained quickstart
that works from a fresh clone.

## Public Source Recheck

- Devpost rules rechecked: https://openai.devpost.com/rules
- OpenAI Build Week page rechecked: https://openai.com/build-week/
- Deadline still shown by Devpost rules: July 21, 2026, 5:00 PM PDT.
- KST planning conversion: July 22, 2026, 9:00 AM KST.
- Public participant count observed: 25,146.
- Requirements still include a working project built with Codex and GPT-5.6, a
  public under-three-minute YouTube demo with audio, a repository URL with
  README/setup/sample data, and a `/feedback` Codex Session ID from the primary
  build thread.
- Developer tools must include installation instructions, supported platforms,
  and a way for judges to test without rebuilding from scratch.

## Gap Closed

The public README and generated Devpost field map previously used
`../submission-packets/openai-build-week.md` in judge commands. That file lives
outside the public GitHub repository, so a judge cloning only
`memekr/submitops-scout` could not reproduce the workflow as written.

This gate adds `fixtures/openai-build-week-packet.md` as the in-repository event
packet and changes README plus generated field-map commands to use it. The
README now includes a Judge Quickstart with supported platforms, `uv sync`, a
fresh-clone command, and the test command.

## Scanner Hardening

While regenerating the packet from the new fixture, the scanner initially
misread a negative sentence about GPT-5.6 evidence as successful live evidence.
The blocked-evidence filter now rejects phrases such as `has not`, `not been`,
`not captured`, and `not complete`, with test coverage for the exact regression.

## Verification Result

Command run from `/Users/mac/hackathon-agent/submitops-scout`:

```bash
uv run submitops-scout fixtures/openai-build-week-packet.md . --out reports/openai-build-week-submitops-scout.md --json reports/openai-build-week-submitops-scout.json --devpost-map submission/openai-build-week-devpost-field-map.md --gpt56-payload reports/openai-build-week-gpt56-payload.json --gpt56-status --verify-public-urls --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
```

Observed output:

- GPT-5.6 connector status: `not configured; set OPENAI_API_KEY to run live gpt-5.6 review`.
- SubmitOps decision: `DOWNGRADE`.
- Blocker count: 2.

Validation commands:

- `uv run pytest`
- `uv run ruff check .`
- `uv run ty check src tests`

## Current Decision

Safe to continue local submission preparation. Do not final-submit.

Exact remaining blockers:

- Devpost image reCAPTCHA before project draft creation.
- Official `/feedback` Codex Session ID.
- Live GPT-5.6 review evidence after verified no-billing/free-credit boundary.
- Final Devpost project preview and submit.
