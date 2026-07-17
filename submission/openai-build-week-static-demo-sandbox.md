# OpenAI Build Week Static Demo Sandbox

Generated KST: 2026-07-17 15:10:00 KST

## Selected Target

OpenAI Build Week remains the active target for this run. Qwen Cloud is still
nearer by deadline, but its remaining actions require human-only Devpost image
reCAPTCHA and Alibaba Cloud phone verification. OpenAI had an unblocked
developer-tool gap: a judge should be able to inspect the submission state
without cloning, rebuilding, signing in, or waiting for a live account handoff.

## Public Source Recheck

- Devpost overview rechecked: https://openai.devpost.com/
- Devpost rules rechecked: https://openai.devpost.com/rules
- Devpost FAQ rechecked: https://openai.devpost.com/details/faqs
- OpenAI Build Week page rechecked: https://openai.com/build-week/
- Deadline still shown by Devpost: July 21, 2026, 5:00 PM PDT.
- KST planning conversion: July 22, 2026, 9:00 AM KST.
- Public participant count observed: 29,422.
- Requirements still include a working project built with Codex and GPT-5.6, a
  public under-three-minute YouTube demo with audio, repository URL with
  README/setup/sample data, `/feedback` Codex Session ID, and for developer
  tools a way for judges to test without rebuilding from scratch.

## Gap Closed

Added a generated static dashboard at `docs/index.html` and a `--static-demo`
CLI option. The page renders the same readiness packet used for the Devpost
field map, including:

- decision state and generated timestamp;
- current blockers;
- public repository and demo video links;
- public YouTube thumbnail as the visual demo asset;
- readiness checks with a local filter control;
- public URL verification rows;
- fresh-clone judge command and sample/source paths.

The public target URL is `https://memekr.github.io/submitops-scout/`. This is a
free GitHub Pages path from the existing public repository; no payment method,
paid resource, identity, tax, banking, or credential exposure is involved.

## Verification Result

Local validation commands:

```bash
uv run pytest
uv run ruff check .
uv run ty check src tests
```

The generated static demo must be regenerated with the current packet command:

```bash
uv run submitops-scout fixtures/openai-build-week-packet.md . --out reports/openai-build-week-submitops-scout.md --json reports/openai-build-week-submitops-scout.json --devpost-map submission/openai-build-week-devpost-field-map.md --static-demo docs/index.html --gpt56-payload reports/openai-build-week-gpt56-payload.json --gpt56-status --verify-public-urls --require-public-url https://memekr.github.io/submitops-scout/ --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/fixtures/openai-build-week-packet.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-judge-quickstart-gate.md --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-static-demo-sandbox.md --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
```

## Current Decision

Safe to continue local submission preparation. Do not final-submit.

Exact remaining blockers:

- Devpost image reCAPTCHA before project draft creation.
- Official `/feedback` Codex Session ID.
- Codex credit approval/code delivery.
- Live GPT-5.6 review evidence after verified no-billing/free-credit boundary.
- Final Devpost project preview and submit.
