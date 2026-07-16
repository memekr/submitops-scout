# SubmitOps Scout OpenAI Build Week Draft

Created: 2026-07-15 09:08 KST.
Devpost registration: completed 2026-07-16 03:11 KST under `spdish12`.

## Target

- Event: OpenAI Build Week
- Track: Developer Tools
- Deadline: July 21, 2026, 5:00 PM PDT; July 22, 2026, 9:00 AM KST.
- Project: SubmitOps Scout: Codex-powered submission command center.
- Public repository: https://github.com/memekr/submitops-scout
- Public demo video: https://youtu.be/6PCzqJu1dRU
- Devpost registration evidence: `/Users/mac/hackathon-agent/submitops-scout/submission/openai-build-week-devpost-registration-gate.md`
- Proof-boundary gate: `/Users/mac/hackathon-agent/submitops-scout/submission/openai-build-week-proof-boundary-gate.md`

## Current State

Implemented local CLI baseline:

- parses an event packet for source facts, deadline, tracks, required materials, and account notes
- scans a repository for README, license, setup, tests, sample data, video URLs, public URLs, Codex mentions, GPT-5.6 mentions, `/feedback` Session ID evidence, and secret-risk patterns
- separates general GPT-5.6 mentions from explicit live GPT-5.6 review evidence
- emits `go`, `downgrade`, or `stop` readiness decisions
- generates a GPT-5.6 Responses API review payload without making a network call or reading secrets
- generates a guarded Devpost field map with blocked placeholders for missing public repo, video, and `/feedback` evidence
- includes a Qwen Cloud fixture that demonstrates last-mile blocker detection on a mature submission packet

## Truth Boundary

Do not claim final Build Week eligibility yet:

- no `/feedback` Session ID has been inserted into final submission materials
- no live GPT-5.6 review call has been run with verified free credits
- Devpost event registration is complete, but project draft creation is blocked by image reCAPTCHA
- no Devpost project draft has been created or submitted

## Current Local Artifacts

- Readiness report: `/Users/mac/hackathon-agent/submitops-scout/reports/openai-build-week-submitops-scout.md`
- JSON report: `/Users/mac/hackathon-agent/submitops-scout/reports/openai-build-week-submitops-scout.json`
- Devpost field map: `/Users/mac/hackathon-agent/submitops-scout/submission/openai-build-week-devpost-field-map.md`
- GPT-5.6 payload: `/Users/mac/hackathon-agent/submitops-scout/reports/openai-build-week-gpt56-payload.json`
- Qwen fixture: `/Users/mac/hackathon-agent/submitops-scout/fixtures/qwen-cloud-packet.md`
- Public demo video publication packet: `/Users/mac/hackathon-agent/submitops-scout/submission/openai-build-week-demo-video-publication.md`
- Devpost registration gate: `/Users/mac/hackathon-agent/submitops-scout/submission/openai-build-week-devpost-registration-gate.md`
- Proof-boundary gate: `/Users/mac/hackathon-agent/submitops-scout/submission/openai-build-week-proof-boundary-gate.md`
- Public repository: `https://github.com/memekr/submitops-scout`

## Draft Devpost Copy

Title: `SubmitOps Scout: Codex-Powered Submission Command Center`

Short description:

> SubmitOps Scout helps builders turn hackathon rules and a project repository into a ready-to-submit packet: evidence scan, eligibility gates, proof links, Devpost copy, validation commands, and exact blockers.

What it does:

> The tool parses competition source facts, scans a local project for submission evidence, maps requirements to proof, generates a readiness packet, and refuses unsupported claims. Missing public video, missing `/feedback` Session ID, secret findings, or unreviewed rules become explicit `downgrade` or `stop` statuses instead of optimistic submission copy.

How Codex and GPT-5.6 are used:

> Codex built the initial Python/uv CLI, tests, packet structure, and Build Week source refresh. The app includes a GPT-5.6 Responses API review payload that will review the generated packet for unsupported claims once a verified no-billing API path is available.

## Next Submission Step

Have the entrant complete the Devpost image reCAPTCHA that appears after `Create project`, insert the official `/feedback` Session ID, capture live GPT-5.6 evidence only after a verified no-billing/free-credit boundary, and run the final Devpost preview. Do not submit until those proof gates are complete or explicitly downgraded in the final form.
