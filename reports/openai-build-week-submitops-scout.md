# SubmitOps Scout Packet

Generated: 2026-07-16T00:16:16+00:00
Decision: DOWNGRADE

## Event Snapshot

- Event: OpenAI Build Week Packet
- URL: https://openai.devpost.com/
- Deadline: July 21, 2026, 5:00 PM PT, per Devpost overview copy.
- Captured at: 2026-07-16T00:16:16+00:00

## Tracks

- Apps for Your Life
- Work and Productivity
- Developer Tools
- Education

## Required Materials

- Demo video published: 2026-07-15 21:19 KST
- Devpost says builders should create a working project using Codex with GPT-5.6 and can enter one of four tracks: Apps for Your Life, Work and Productivity, Developer Tools, or Education
- Required submission materials now include a chosen category, project description, public YouTube demo video under three minutes with voiceover covering how Codex and GPT-5.6 were used, repository URL with README/setup/sample data, and a `/feedback` Codex Session ID from the primary build thread
- The theme fits this workspace and the user's Codex-heavy workflow
- OpenAI still needs a `/feedback` Session ID and live GPT-5.6 proof before Devpost final submit; the public repository, public YouTube demo URL, Devpost event registration, and proof-boundary gate are now verified locally
- OpenAI/Codex access
- OpenAI/Codex credits are available only through the event resource flow and must remain prepaid/no-auto-top-up before any live GPT-5.6 evidence run
- Working project built with Codex and GPT-5.6
- Chosen track/category
- Project description
- Public YouTube demo video under three minutes with voiceover that covers what was built, how Codex was used, and how GPT-5.6 was used
- Code repository, public with relevant license or private and shared with `testing@devpost.com` and `build-week-event@openai.com`

## Repository Evidence

- Root: .
- Scanned text files: 14
- README: README.md
- License: LICENSE
- Tests: 2
- Sample data: fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- Video URLs: https://youtu.be/6PCzqJu1dRU, https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json
- Video assets: missing
- Devpost flow evidence: submission/openai-build-week-devpost-registration-gate.md
- Live GPT-5.6 evidence: missing
- Public URLs found: 11

## Readiness Checks

- PASS: official rules captured - Packet records Official Rules source state.
- PASS: README present - README.md
- PASS: license present - LICENSE
- PASS: public repository URL present - https://github.com/memekr/submitops-scout
- PASS: setup path present - README.md, scripts/render-openai-demo-video.sh, src/submitops_scout/core.py, src/submitops_scout/gpt56_adapter.py, submission/openai-build-week-demo-video-publication.md
- PASS: tests present - 2 test files
- PASS: sample data present - fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- PASS: Codex evidence present - README.md, pyproject.toml, scripts/render-openai-demo-video.sh, src/submitops_scout/core.py, submission/openai-build-week-demo-video-publication.md
- PASS: GPT-5.6 evidence present - README.md, scripts/render-openai-demo-video.sh, src/submitops_scout/cli.py, src/submitops_scout/core.py, src/submitops_scout/gpt56_adapter.py
- MISSING: live GPT-5.6 review evidence present - no detail
- MISSING: /feedback Session ID present - no detail
- PASS: public demo video present - https://youtu.be/6PCzqJu1dRU, https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json
- PASS: secret scan clear - 0 findings

## Blockers

- live GPT-5.6 review evidence present
- /feedback Session ID present

## Secret Findings

- None
