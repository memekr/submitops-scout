# SubmitOps Scout Packet

Generated: 2026-07-16T12:15:09+00:00
Decision: DOWNGRADE

## Event Snapshot

- Event: OpenAI Build Week Packet
- URL: https://openai.devpost.com/
- Deadline: July 21, 2026, 5:00 PM PT, per Devpost rules.
- Captured at: 2026-07-16T12:15:07+00:00

## Tracks

- Apps for Your Life
- Work and Productivity
- Developer Tools
- Education

## Required Materials

- Devpost says builders should create a working project using Codex and GPT-5.6
- Required submission materials include a chosen category, project description, public YouTube demo video under three minutes with audio, repository URL with README/setup/sample data, and a `/feedback` Codex Session ID from the primary build thread
- OpenAI/Codex access is required
- OpenAI/Codex credits must stay within verified free, prepaid, or no-auto-top-up boundaries before any live GPT-5.6 evidence run
- Title: `SubmitOps Scout: Codex-Powered Submission Command Center`
- > The tool parses competition source facts, scans a local project for submission evidence, maps requirements to proof, generates a readiness packet, and refuses unsupported claims. Missing public video, missing `/feedback` Session ID, secret findings, or unreviewed rules become explicit `downgrade` or `stop` statuses instead of optimistic submission copy
- > It is a practical Codex-native developer tool with a live deadline use case. Instead of only generating code, it helps teams ship truthful, judge-ready submissions under pressure
- Official `/feedback` Codex Session ID is not inserted
- Live GPT-5.6 review evidence has not been captured under a verified no-billing/free-credit boundary

## Repository Evidence

- Root: .
- Scanned text files: 16
- README: README.md
- License: LICENSE
- Tests: 2
- Sample data: fixtures/openai-build-week-packet.md, fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- Video URLs: https://youtu.be/6PCzqJu1dRU, https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json
- Video assets: missing
- Devpost flow evidence: submission/openai-build-week-devpost-registration-gate.md
- Live GPT-5.6 evidence: missing
- Public URLs found: 17

## Public URL Verification

- PASS: reachable https://github.com/memekr/submitops-scout - HTTP 200
- PASS: reachable https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md - HTTP 200
- PASS: reachable https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md - HTTP 200
- PASS: absent https://raw.githubusercontent.com/memekr/submitops-scout/main/.env - HTTP 404


## Readiness Checks

- PASS: official rules captured - Packet records Official Rules source state.
- PASS: README present - README.md
- PASS: license present - LICENSE
- PASS: public repository URL present - https://github.com/memekr/submitops-scout
- PASS: setup path present - README.md, fixtures/openai-build-week-packet.md, scripts/render-openai-demo-video.sh, src/submitops_scout/core.py, src/submitops_scout/gpt56_adapter.py
- PASS: tests present - 2 test files
- PASS: sample data present - fixtures/openai-build-week-packet.md, fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- PASS: Codex evidence present - README.md, fixtures/openai-build-week-packet.md, pyproject.toml, scripts/render-openai-demo-video.sh, src/submitops_scout/core.py
- PASS: GPT-5.6 evidence present - README.md, fixtures/openai-build-week-packet.md, scripts/render-openai-demo-video.sh, src/submitops_scout/cli.py, src/submitops_scout/core.py
- MISSING: live GPT-5.6 review evidence present - no detail
- MISSING: /feedback Session ID present - no detail
- PASS: public demo video present - https://youtu.be/6PCzqJu1dRU, https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json
- PASS: secret scan clear - 0 findings
- PASS: public URL reachable: https://github.com/memekr/submitops-scout - HTTP 200
- PASS: public URL reachable: https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md - HTTP 200
- PASS: public URL absent: https://raw.githubusercontent.com/memekr/submitops-scout/main/.env - HTTP 404

## Blockers

- live GPT-5.6 review evidence present
- /feedback Session ID present

## Secret Findings

- None
