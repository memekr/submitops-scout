# OpenAI Build Week Public URL Verification Gate

Generated KST: 2026-07-16 15:16:21 KST

## Selected Target

OpenAI Build Week remains the active target for this run. Qwen Cloud is still
closer by deadline, but its remaining actions require human-only Devpost image
reCAPTCHA and Alibaba Cloud phone verification. OpenAI still has an unblocked
quality gate: turn public URL smoke testing into first-class readiness evidence.

## Public Source Recheck

- Devpost overview rechecked: https://openai.devpost.com/
- OpenAI Build Week page rechecked: https://openai.com/build-week/
- Deadline still shown by Devpost: July 21, 2026, 5:00 PM PDT.
- KST planning conversion: July 22, 2026, 9:00 AM KST.
- Public participant count observed: 22,514.
- Requirements still include a working project built with Codex and GPT-5.6, a
  public under-three-minute YouTube demo with audio, a repository URL with
  README/setup/sample data, and a `/feedback` Codex Session ID from the primary
  build thread.

## Tooling Change

`submitops-scout` now supports public URL verification as an optional networked
gate:

- `--verify-public-urls` checks the discovered repository URL and hosted demo
  video evidence.
- `--require-public-url` records judge-critical raw URLs that must return HTTP
  2xx or 3xx.
- `--forbid-public-url` records sensitive URLs, such as raw `.env`, that must
  return HTTP 404 or 410.
- URL templates in source code, including strings such as `{encoded_url}` and
  empty oEmbed `url=` placeholders, are ignored so source constants do not
  become false public-link blockers.

## Verification Result

Command run from `/Users/mac/hackathon-agent/submitops-scout`:

```bash
uv run submitops-scout ../submission-packets/openai-build-week.md . --out reports/openai-build-week-submitops-scout.md --json reports/openai-build-week-submitops-scout.json --devpost-map submission/openai-build-week-devpost-field-map.md --gpt56-payload reports/openai-build-week-gpt56-payload.json --gpt56-status --verify-public-urls --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
```

Observed output:

- GPT-5.6 connector status: `not configured; set OPENAI_API_KEY to run live gpt-5.6 review`.
- SubmitOps decision: `DOWNGRADE`.
- Blocker count: 2.

Public URL checks recorded in the generated Markdown and JSON reports:

- GitHub repository: HTTP 200.
- YouTube oEmbed for https://youtu.be/6PCzqJu1dRU: HTTP 200.
- Raw README: HTTP 200.
- Raw Devpost field map: HTTP 200.
- Raw proof-boundary gate: HTTP 200.
- Raw `.env`: HTTP 404.

## Current Decision

The public evidence links are judge-accessible and no raw `.env` file is
public. Safe to continue local submission preparation. Do not final-submit.

Exact remaining blockers:

- Devpost image reCAPTCHA before project draft creation.
- Official `/feedback` Codex Session ID.
- Live GPT-5.6 review evidence after verified no-billing/free-credit boundary.
- Final Devpost project preview and submit.
