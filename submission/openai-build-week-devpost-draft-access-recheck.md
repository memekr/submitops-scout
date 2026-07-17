# OpenAI Build Week Devpost Draft Access Recheck

Captured: 2026-07-18 03:16 KST.

## Event URL and Source Snapshot

Sources checked through the existing signed-in Chrome session:

- https://openai.devpost.com/
- https://devpost.com/submit-to/30223-openai-build-week/manage/submissions
- https://devpost.com/submit-to/30223-openai-build-week/manage/submissions/1088316/edit

Observed public source state:

- Chrome remained signed in to Devpost as `spdish12`.
- OpenAI Build Week still showed the deadline as 2026-07-22 9:00 AM GMT+9 / July 21, 2026, 5:00 PM PT.
- Public Devpost surfaces showed 33,739 participants during this recheck.
- The event overview still exposed `Start project`, `My projects`, and `Import from portfolio`.
- The `Start project` and `Create project` controls were Devpost `g-recaptcha` submit buttons using a public site key.
- The manage-submissions page showed active reCAPTCHA iframes, including challenge frames titled `recaptcha challenge expires in two minutes`.
- A transient `Edit project` link for `/manage/submissions/1088316/edit` appeared during one extraction pass, but direct navigation to that URL returned `You are not authorized to access this page`, and the link did not reappear after reloading the manage page. Treat draft edit access as not stable.

## Deadline and Timezone

- Public deadline: July 21, 2026, 5:00 PM PT.
- KST planning conversion: July 22, 2026, 9:00 AM KST.
- Current local planning time during this recheck: July 18, 2026, 3:16 AM KST.

## Eligibility and Account Requirements

- Devpost registration remains complete under `spdish12`.
- No new eligibility, identity, tax, banking, payment, employment, travel, or IP-transfer facts were transmitted.
- No CAPTCHA bypass was attempted. The next external action requires the entrant to complete Devpost reCAPTCHA interactively.

## Required Materials Impact

Already ready and still usable:

- Public repository: https://github.com/memekr/submitops-scout
- Public static demo: https://memekr.github.io/submitops-scout/
- Public demo video: https://youtu.be/6PCzqJu1dRU
- README, license, setup instructions, sample packet, Qwen fixture, public URL verification gate, and Devpost field map.

Still blocked before final submit:

- Stable Devpost project draft creation/edit access.
- Official `/feedback` Codex Session ID.
- Live GPT-5.6 evidence under a verified no-billing/free/prepaid boundary.
- Final Devpost preview and submit.

## Rubric Mapping

- Technological implementation: unchanged; CLI, scanner, public URL verification, and static demo are public.
- Design: unchanged; judge has no-login static demo and fresh-clone CLI path.
- Potential impact: strengthened by showing the tool's live ability to distinguish account-flow evidence from unsupported final-submit readiness.
- Quality of idea: strengthened by preserving the human CAPTCHA boundary instead of claiming a completed draft.

## Submission Status

Status: not submitted.

Current Devpost state: registered, but project draft creation/access remains blocked by Devpost reCAPTCHA. Direct edit access is not stable and must not be treated as draft proof.

Next allowed action: have the entrant complete the visible Devpost reCAPTCHA in Chrome, then reopen `My projects`, create or edit the draft, paste the verified public repository/video/static-demo fields, and stop again before final submit if `/feedback`, live GPT-5.6 evidence, payment, identity, tax, banking, travel, employment/IP-transfer, or another CAPTCHA gate appears.
