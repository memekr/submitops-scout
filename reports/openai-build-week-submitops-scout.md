# SubmitOps Scout Packet

Generated: 2026-07-15T06:12:34+00:00
Decision: DOWNGRADE

## Event Snapshot

- Event: OpenAI Build Week Packet
- URL: https://openai.devpost.com/
- Deadline: July 21, 2026, 5:00 PM PT, per Devpost overview copy.
- Captured at: 2026-07-15T06:12:34+00:00

## Tracks

- Apps for Your Life
- Work and Productivity
- Developer Tools
- Education

## Required Materials

- Devpost says builders should create a working project using Codex with GPT-5.6 and can enter one of four tracks: Apps for Your Life, Work and Productivity, Developer Tools, or Education
- Required submission materials now include a chosen category, project description, public YouTube demo video under three minutes with voiceover covering how Codex and GPT-5.6 were used, repository URL with README/setup/sample data, and a `/feedback` Codex Session ID from the primary build thread
- The theme fits this workspace and the user's Codex-heavy workflow
- OpenAI still needs a public repo, public video, `/feedback` Session ID, and live GPT-5.6 proof before Devpost final submit
- OpenAI/Codex access
- OpenAI/Codex credits are available only through the event resource flow and must remain prepaid/no-auto-top-up before any live GPT-5.6 evidence run
- Working project built with Codex and GPT-5.6
- Chosen track/category
- Project description
- Public YouTube demo video under three minutes with voiceover that covers what was built, how Codex was used, and how GPT-5.6 was used
- Code repository, public with relevant license or private and shared with `testing@devpost.com` and `build-week-event@openai.com`
- README with setup instructions, sample data if needed, and clear testing guidance

## Repository Evidence

- Root: .
- Scanned text files: 10
- README: README.md
- License: LICENSE
- Tests: 2
- Sample data: fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- Video URLs: missing
- Video assets: missing
- Public URLs found: 7

## Readiness Checks

- PASS: official rules captured - Packet records Official Rules source state.
- PASS: README present - README.md
- PASS: license present - LICENSE
- MISSING: public repository URL present - BLOCKED: public repository URL not verified yet
- PASS: setup path present - README.md, src/submitops_scout/core.py, src/submitops_scout/gpt56_adapter.py, submission/openai-build-week-devpost-field-map.md, submission/openai-build-week-draft.md
- PASS: tests present - 2 test files
- PASS: sample data present - fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- PASS: Codex evidence present - README.md, pyproject.toml, src/submitops_scout/core.py, submission/openai-build-week-devpost-field-map.md, submission/openai-build-week-draft.md
- PASS: GPT-5.6 evidence present - README.md, src/submitops_scout/cli.py, src/submitops_scout/core.py, src/submitops_scout/gpt56_adapter.py, submission/openai-build-week-devpost-field-map.md
- MISSING: /feedback Session ID present - no detail
- MISSING: public demo video present - no detail
- PASS: secret scan clear - 0 findings

## Blockers

- public repository URL present
- /feedback Session ID present
- public demo video present

## Secret Findings

- None
