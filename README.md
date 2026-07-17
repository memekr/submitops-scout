# SubmitOps Scout

SubmitOps Scout turns hackathon rules plus a local project repository into a
submission packet: source facts, evidence links, readiness checks, downgrade
notes, and exact external blockers.

Public repository: https://github.com/memekr/submitops-scout
Public demo video: https://youtu.be/6PCzqJu1dRU
Public static demo: https://memekr.github.io/submitops-scout/
Devpost registration evidence: submission/openai-build-week-devpost-registration-gate.md
Codex credits request evidence: submission/openai-build-week-codex-credits-request.md
Proof boundary gate: submission/openai-build-week-proof-boundary-gate.md
Public URL verification gate: submission/openai-build-week-public-url-verification-gate.md

This initial Build Week version is scoped to the OpenAI Build Week requirements:

- working project built with Codex and GPT-5.6
- selected category
- project description
- public YouTube demo under 3 minutes with voiceover
- repository URL with README, setup instructions, and sample data when needed
- `/feedback` Codex Session ID from the primary build thread
- installation and judge-testing path for developer tools

The tool never claims a public video, live GPT-5.6 call, final Devpost submit, or
eligibility fact unless it finds supporting evidence. Missing proof becomes a
`downgrade` or `stop` status in the packet.

## Usage

```bash
uv run submitops-scout fixtures/openai-build-week-packet.md . \
  --out reports/openai-build-week-submitops-scout.md \
  --json reports/openai-build-week-submitops-scout.json \
  --devpost-map submission/openai-build-week-devpost-field-map.md \
  --static-demo docs/index.html \
  --gpt56-payload reports/openai-build-week-gpt56-payload.json \
  --gpt56-status \
  --verify-public-urls \
  --require-public-url https://memekr.github.io/submitops-scout/ \
  --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md \
  --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md \
  --require-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md \
  --forbid-public-url https://raw.githubusercontent.com/memekr/submitops-scout/main/.env
```

## Judge Quickstart

Supported platforms: macOS, Linux, or Windows with Python 3.12 and `uv`.

```bash
git clone https://github.com/memekr/submitops-scout.git
cd submitops-scout
uv sync --all-groups
uv run submitops-scout fixtures/openai-build-week-packet.md . \
  --out reports/openai-build-week-submitops-scout.md \
  --json reports/openai-build-week-submitops-scout.json \
  --devpost-map submission/openai-build-week-devpost-field-map.md \
  --static-demo docs/index.html \
  --gpt56-payload reports/openai-build-week-gpt56-payload.json \
  --gpt56-status
uv run pytest
```

The command uses the in-repository `fixtures/openai-build-week-packet.md`, so a
judge can test the core workflow from a fresh clone without access to this local
workspace. The GPT-5.6 step writes a review payload and prints connector status;
it does not read secrets or call the network unless the operator chooses to run a
separate live review.

The Devpost field map is intentionally guarded. If public video, repository, or
`/feedback` evidence is missing, the map labels those fields as blocked rather
than inventing paste-ready values.

## Static Demo Sandbox

The generated static dashboard in `docs/index.html` gives judges a no-login,
no-build view of the same packet: decision state, blockers, public URL checks,
sample paths, the public video thumbnail, and the fresh-clone command. It is
published through GitHub Pages at https://memekr.github.io/submitops-scout/.

## Public URL Verification

`--verify-public-urls` checks the discovered repository and hosted demo video.
`--require-public-url` adds judge-critical raw files that must return HTTP 2xx
or 3xx, and `--forbid-public-url` records sensitive paths such as `.env` that
must return HTTP 404 or 410. URL templates in source code are ignored so
placeholder strings do not become false blockers.

## Demo Video

The public Build Week demo video is published at https://youtu.be/6PCzqJu1dRU.
The source render can be regenerated locally:

```bash
bash scripts/render-openai-demo-video.sh
```

The generated MP4 is intentionally written under `output/`, which is ignored by
git. The publication evidence and SHA-256 are recorded in
`submission/openai-build-week-demo-video-publication.md`.

## Devpost Registration Boundary

The OpenAI Build Week Devpost registration is complete under `spdish12`.
Project draft creation is blocked at Devpost image reCAPTCHA after `Create
project`; the visible challenge was `Select all squares with traffic lights`.
No CAPTCHA bypass, project draft, final submit, payment, identity, tax, or
banking action was performed.

## Codex Credits Boundary

The official Build Week Resources form for `$100 Codex credits` was submitted
before the July 17, 2026, 12:00 PM PT cutoff. The confirmation page showed
`Your response has been recorded`. These are Codex credits, not API credits, and
approval is still pending until a code or balance appears in the entrant-owned
OpenAI account.

## Demo Fixture

`fixtures/qwen-cloud-packet.md` is a compact real-world fixture from the Qwen
Cloud submission sprint. It gives judges a mature packet with strong public
assets and explicit external blockers, which demonstrates why SubmitOps Scout is
useful beyond a toy repository scan.

## GPT-5.6 Boundary

`submitops_scout.gpt56_adapter` prepares a Responses API payload for `gpt-5.6`
submission review. It does not make network calls or read secrets. The readiness
gate now separates general GPT-5.6 mentions from live review evidence. A later
run can promote this only after `OPENAI_API_KEY`, free credits, and no-auto-top-up
boundaries are verified.

Primary source references:

- OpenAI Build Week: https://openai.com/build-week/
- OpenAI Build Week Devpost: https://openai.devpost.com/
- OpenAI Build Week FAQ: https://openai.devpost.com/details/faqs
- OpenAI API Responses docs: https://developers.openai.com/api/docs/guides/text
