# OpenAI Build Week Source Freshness and Parse Gate

Generated KST: 2026-07-17 15:14:11 KST

## Selected Target

OpenAI Build Week remains the active target for this run. Qwen Cloud is nearer
by deadline, but its remaining actions still require human-only Devpost image
reCAPTCHA and Alibaba Cloud phone verification. OpenAI can still advance
locally by keeping the submission packet aligned with the live public sources
and making the generated judge packet cleaner.

## Public Source Recheck

- Devpost overview rechecked: https://openai.devpost.com/
- Devpost rules rechecked: https://openai.devpost.com/rules
- Devpost FAQ rechecked: https://openai.devpost.com/details/faqs
- OpenAI Build Week page rechecked: https://openai.com/build-week/
- Deadline still shown by Devpost: July 21, 2026, 5:00 PM PDT.
- KST planning conversion: July 22, 2026, 9:00 AM KST.
- Public participant count observed across Devpost public surfaces: about 31,500.
- Requirements still include a working project built with Codex and GPT-5.6, a
  public under-three-minute YouTube demo with audio, repository URL with
  README/setup/sample data, `/feedback` Codex Session ID, and for developer
  tools a way for judges to test without rebuilding from scratch.
- FAQ source text reinforces that Codex usage must be demonstrated in the text
  description, demo video, and README, and that GPT-5.6 must be clearly
  referenced in the video and repository.

## Tooling Change

The event packet parser now keeps the generated `Required Materials` section
focused on actual requirement bullets. It skips source-only URL bullets, title
lines, and draft-answer blockquotes, and it preserves wrapped Markdown bullets
as one item. Account and credit facts are separated into an `Account
Requirements` section in the generated readiness report.

## Current Decision

Safe to continue local submission preparation. Do not final-submit.

Exact remaining blockers:

- Devpost image reCAPTCHA before project draft creation.
- Official `/feedback` Codex Session ID.
- Codex credit approval/code delivery.
- Live GPT-5.6 review evidence after verified no-billing/free-credit boundary.
- Final Devpost project preview and submit.
