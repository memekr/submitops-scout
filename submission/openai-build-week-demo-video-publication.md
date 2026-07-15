# OpenAI Build Week Demo Video Publication

Updated: 2026-07-15 21:19 KST.

## Public Video

- YouTube URL: https://youtu.be/6PCzqJu1dRU
- Published title: `SubmitOps Scout OpenAI Build Week Demo`
- YouTube oEmbed author_name matched the signed-in channel display name.
- YouTube Studio publication date shown after publish: `2026. 7. 15.`
- Public oEmbed verification: HTTP 200 on July 15, 2026 KST.

## Current Local Render Evidence

- Render script: `/Users/mac/hackathon-agent/submitops-scout/scripts/render-openai-demo-video.sh`
- Local MP4 path: `/Users/mac/hackathon-agent/submitops-scout/output/playwright/openai-demo-video/submitops-scout-openai-demo-preupload.mp4`
- Duration: `126.000000` seconds.
- Resolution/codecs: 1280x720 H.264 video with AAC audio.
- Size: `2974959` bytes.
- SHA-256: `bea3a4e63d3b089ebdf30fe734c1cc770cd6ae0d258c22e1a14a7c8d6a83afc5`
- Current generated SubmitOps decision: `DOWNGRADE`, with exact blocker `/feedback Session ID present`.

The public URL was created from the same render pipeline before the final video
URL was inserted back into the generated field map. The current local rerender
is the source-of-truth artifact for the latest packet state.

## YouTube Metadata Used

Title:

```text
SubmitOps Scout OpenAI Build Week Demo
```

Description:

```text
OpenAI Build Week Developer Tools demo for SubmitOps Scout.

Public repository: https://github.com/memekr/submitops-scout

SubmitOps Scout is a Codex-built submission command center that reads hackathon rules and scans repository evidence to generate readiness packets, Devpost field maps, validation commands, and exact blockers.

This demo shows the current truthful state: public repo, README, tests, sample fixture, and secret scan are ready; public YouTube proof and /feedback Session ID are still treated as blockers until this upload and final Codex feedback evidence are recorded.

GPT-5.6 boundary: the repo prepares a Responses API review payload but does not make a live paid API call in this video.
```

## Truth Boundary

- Public YouTube demo proof is now available for the Build Week packet.
- This video does not claim a live GPT-5.6 API call.
- This video does not provide the required `/feedback` Codex Session ID.
- Final Devpost submission remains blocked until `/feedback` evidence is inserted and the final form preview is checked.

## Validation

```bash
bash scripts/render-openai-demo-video.sh
uv run pytest
uv run ruff check .
uv run ty check src tests
curl -L -s -o /tmp/submitops-youtube-oembed.json -w 'oembed %{http_code}\n' 'https://www.youtube.com/oembed?url=https://youtu.be/6PCzqJu1dRU&format=json'
```

Observed results:

- Render completed with `Duration seconds: 126.000000`.
- `uv run pytest`: 7 passed.
- `uv run ruff check .`: all checks passed.
- `uv run ty check src tests`: all checks passed.
- YouTube oEmbed returned HTTP 200 and title `SubmitOps Scout OpenAI Build Week Demo`.
