# SubmitOps Scout

SubmitOps Scout turns hackathon rules plus a local project repository into a
submission packet: source facts, evidence links, readiness checks, downgrade
notes, and exact external blockers.

Public repository: https://github.com/memekr/submitops-scout

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
uv run submitops-scout ../submission-packets/openai-build-week.md . \
  --out reports/openai-build-week-submitops-scout.md \
  --json reports/openai-build-week-submitops-scout.json \
  --devpost-map submission/openai-build-week-devpost-field-map.md \
  --gpt56-payload reports/openai-build-week-gpt56-payload.json
```

The Devpost field map is intentionally guarded. If public video, repository, or
`/feedback` evidence is missing, the map labels those fields as blocked rather
than inventing paste-ready values.

## Demo Fixture

`fixtures/qwen-cloud-packet.md` is a compact real-world fixture from the Qwen
Cloud submission sprint. It gives judges a mature packet with strong public
assets and explicit external blockers, which demonstrates why SubmitOps Scout is
useful beyond a toy repository scan.

## GPT-5.6 Boundary

`submitops_scout.gpt56_adapter` prepares a Responses API payload for `gpt-5.6`
submission review. It does not make network calls or read secrets. A later run
can promote this to live evidence only after `OPENAI_API_KEY`, free credits, and
no-auto-top-up boundaries are verified.

Primary source references:

- OpenAI Build Week: https://openai.com/build-week/
- OpenAI Build Week Devpost: https://openai.devpost.com/
- OpenAI Build Week FAQ: https://openai.devpost.com/details/faqs
- OpenAI API Responses docs: https://developers.openai.com/api/docs/guides/text
