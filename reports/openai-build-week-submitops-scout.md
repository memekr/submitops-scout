# SubmitOps Scout Packet

Generated: 2026-07-17T18:20:03+00:00
Decision: DOWNGRADE

## Event Snapshot

- Event: OpenAI Build Week Packet
- URL: https://openai.devpost.com/
- Deadline: July 21, 2026, 5:00 PM PT, per Devpost rules.
- Captured at: 2026-07-17T18:20:02+00:00

## Tracks

- Apps for Your Life
- Work and Productivity
- Developer Tools
- Education

## Required Materials

- Devpost says builders should create a working project using Codex and GPT-5.6
- Required submission materials include a chosen category, project description, public YouTube demo video under three minutes with audio, repository URL with README/setup/sample data, and a `/feedback` Codex Session ID from the primary build thread
- The FAQ says Codex usage must be demonstrated in the text description, demo video, and README; GPT-5.6 must be clearly referenced in the demo video and repository
- Developer tool submissions should include installation instructions, supported platforms, and a way for judges to test without rebuilding from scratch

## Account Requirements

- Devpost Resources say registered participants can request `$100 Codex credits` before Friday, July 17, 2026 at 12:00 PM PT; the resources copy says these are not API credits
- The official Codex credits request form was submitted before the cutoff and the confirmation page displayed `Your response has been recorded`. Credit approval and delivery are still pending
- Devpost account is required
- OpenAI/Codex access is required
- OpenAI/Codex credits must stay within verified free, prepaid, or no-auto-top-up boundaries before any live GPT-5.6 evidence run
- The submitted Codex credits request is not proof of API credits; do not run any billable API or paid resource path from this request alone
- Codex credits request is submitted but not yet approved or delivered

## Repository Evidence

- Root: .
- Scanned text files: 21
- README: README.md
- License: LICENSE
- Tests: 2
- Sample data: fixtures/openai-build-week-packet.md, fixtures/qwen-cloud-packet.md, reports/openai-build-week-gpt56-payload.json, reports/openai-build-week-submitops-scout.json, reports/openai-build-week-submitops-scout.md
- Video URLs: https://youtu.be/6PCzqJu1dRU, https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json
- Video assets: missing
- Devpost flow evidence: submission/openai-build-week-devpost-draft-access-recheck.md, submission/openai-build-week-devpost-registration-gate.md
- Live GPT-5.6 evidence: missing
- Public URLs found: 24

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
- PASS: public URL reachable: https://memekr.github.io/submitops-scout/ - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/README.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-devpost-field-map.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-proof-boundary-gate.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/fixtures/openai-build-week-packet.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-judge-quickstart-gate.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-static-demo-sandbox.md - HTTP 200
- PASS: public URL reachable: https://raw.githubusercontent.com/memekr/submitops-scout/main/submission/openai-build-week-source-freshness-parse-gate.md - HTTP 200
- PASS: public URL absent: https://raw.githubusercontent.com/memekr/submitops-scout/main/.env - HTTP 404

## Blockers

- live GPT-5.6 review evidence present
- /feedback Session ID present

## Secret Findings

- None
