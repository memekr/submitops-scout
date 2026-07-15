#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT/output/playwright/openai-demo-video}"
WORK_DIR="$OUT_DIR/work"
SLIDE_DIR="$WORK_DIR/slides"
FRAME_DIR="$WORK_DIR/frames"
VOICEOVER="$OUT_DIR/voiceover.txt"
AUDIO="$WORK_DIR/voiceover.aiff"
BASE_VIDEO="$WORK_DIR/slides-only.mp4"
VIDEO="$OUT_DIR/submitops-scout-openai-demo-preupload.mp4"
PROBE="$OUT_DIR/ffprobe.json"
SHA="$OUT_DIR/sha256.txt"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required for Playwright screenshots." >&2
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  echo "ffmpeg and ffprobe are required to render and validate the video." >&2
  exit 1
fi
if ! command -v node >/dev/null 2>&1 || ! command -v uv >/dev/null 2>&1; then
  echo "node and uv are required to generate slide content from the local packet." >&2
  exit 1
fi

cd "$ROOT"
rm -rf "$WORK_DIR"
mkdir -p "$SLIDE_DIR" "$FRAME_DIR" "$OUT_DIR"

uv run submitops-scout ../submission-packets/openai-build-week.md . \
  --out reports/openai-build-week-submitops-scout.md \
  --json reports/openai-build-week-submitops-scout.json \
  --devpost-map submission/openai-build-week-devpost-field-map.md \
  --gpt56-payload reports/openai-build-week-gpt56-payload.json \
  --gpt56-status

node - "$ROOT" "$SLIDE_DIR" "$OUT_DIR" <<'NODE'
const fs = require("fs");
const path = require("path");

const [root, slideDir, outDir] = process.argv.slice(2);
const packet = JSON.parse(
  fs.readFileSync(path.join(root, "reports/openai-build-week-submitops-scout.json"), "utf8"),
);
const fieldMap = fs.readFileSync(
  path.join(root, "submission/openai-build-week-devpost-field-map.md"),
  "utf8",
);
const gptPayload = JSON.parse(
  fs.readFileSync(path.join(root, "reports/openai-build-week-gpt56-payload.json"), "utf8"),
);
const qwenFixture = fs.readFileSync(path.join(root, "fixtures/qwen-cloud-packet.md"), "utf8");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function bullets(values) {
  return values.map((value) => `<li>${escapeHtml(value)}</li>`).join("");
}

function codeBlock(value) {
  return `<pre>${escapeHtml(value)}</pre>`;
}

function slideHtml({ eyebrow, title, summary, points = [], code = "", footer = "" }) {
  const pointMarkup = points.length ? `<ul>${bullets(points)}</ul>` : "";
  const codeMarkup = code ? codeBlock(code) : "";
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(title)}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      width: 1280px;
      height: 720px;
      overflow: hidden;
      background: #f5f7fb;
      color: #18212f;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }
    .stage {
      width: 1280px;
      height: 720px;
      display: grid;
      align-items: center;
      padding: 52px 64px;
      background:
        linear-gradient(90deg, rgba(20, 120, 105, 0.12), transparent 48%),
        linear-gradient(180deg, #ffffff, #edf2f7);
    }
    .frame {
      border: 1px solid #d6deea;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.96);
      box-shadow: 0 18px 48px rgba(24, 33, 47, 0.14);
      min-height: 562px;
      display: grid;
      grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.08fr);
      gap: 42px;
      align-items: center;
      padding: 42px 46px;
    }
    .eyebrow {
      color: #0f766e;
      font-size: 21px;
      font-weight: 800;
      text-transform: uppercase;
      margin-bottom: 16px;
    }
    h1 {
      margin: 0;
      font-size: 52px;
      line-height: 1.04;
      letter-spacing: 0;
    }
    .summary {
      margin: 24px 0 0;
      color: #4a5565;
      font-size: 25px;
      line-height: 1.32;
    }
    ul {
      margin: 0;
      padding-left: 28px;
      display: grid;
      gap: 15px;
      font-size: 25px;
      line-height: 1.25;
    }
    li::marker { color: #2563eb; }
    pre {
      margin: 0;
      width: 100%;
      max-height: 456px;
      overflow: hidden;
      white-space: pre-wrap;
      border: 1px solid #cad4e4;
      border-radius: 8px;
      background: #111827;
      color: #f8fafc;
      padding: 22px;
      font-size: 21px;
      line-height: 1.28;
    }
    .footer {
      margin: 24px 0 0;
      color: #667085;
      font-size: 20px;
      line-height: 1.3;
    }
  </style>
</head>
<body>
  <main class="stage">
    <section class="frame">
      <div>
        <div class="eyebrow">${escapeHtml(eyebrow)}</div>
        <h1>${escapeHtml(title)}</h1>
        <p class="summary">${escapeHtml(summary)}</p>
        ${footer ? `<p class="footer">${escapeHtml(footer)}</p>` : ""}
      </div>
      <div>${codeMarkup || pointMarkup}</div>
    </section>
  </main>
</body>
</html>`;
}

function pickLines(text, patterns, maxLines = 10) {
  const lowerPatterns = patterns.map((pattern) => pattern.toLowerCase());
  return text
    .split(/\r?\n/)
    .filter((line) => lowerPatterns.some((pattern) => line.toLowerCase().includes(pattern)))
    .slice(0, maxLines)
    .join("\n");
}

const readinessExcerpt = [
  `Decision: ${packet.decision.toUpperCase()}`,
  `Deadline: ${packet.event.deadline}`,
  `Repository: ${packet.evidence.public_urls.find((url) => url.includes("github.com/memekr/submitops-scout"))}`,
  "",
  "Still blocked:",
  ...packet.blockers.map((blocker) => `- ${blocker}`),
  "",
  `Pass count: ${packet.checks.filter((check) => check.status === "pass").length}/${packet.checks.length}`,
  "Strong evidence:",
  "- README, license, public repository",
  "- tests, sample data, secret scan clear",
].join("\n");

const devpostExcerpt = pickLines(
  fieldMap,
  ["Project title", "Category", "Repository URL", "Demo video URL", "/feedback", "Status:"],
);

const fixtureExcerpt = pickLines(
  qwenFixture,
  ["Deadline:", "public repository", "public demo video", "Remaining blockers", "Current readiness"],
);

const payloadExcerpt = JSON.stringify({
  model: gptPayload.model,
  purpose: "review final packet for unsupported claims",
  network_call: "not made by this demo",
  input_count: Array.isArray(gptPayload.input) ? gptPayload.input.length : 0,
}, null, 2);

const slides = [
  ["01-title.html", {
    eyebrow: "OpenAI Build Week - Developer Tools",
    title: "SubmitOps Scout",
    summary: "A Codex-built command center for turning hackathon rules and repository evidence into a truthful submission packet.",
    points: [
      "Parses event packets for deadlines, requirements, and account gates.",
      "Scans repo evidence for README, license, tests, sample data, URLs, and secrets.",
      "Outputs Devpost copy plus go, downgrade, or stop decisions.",
    ],
    footer: "Render source for the published YouTube demo.",
  }],
  ["02-readiness.html", {
    eyebrow: "Readiness gate",
    title: "The tool refuses missing proof",
    summary: "The current Build Week packet is downgraded until the /feedback Session ID is present.",
    code: readinessExcerpt,
    footer: "Unsupported claims become blockers, not optimistic copy.",
  }],
  ["03-devpost-map.html", {
    eyebrow: "Devpost field map",
    title: "Paste-safe answers stay guarded",
    summary: "SubmitOps Scout drafts the exact fields judges need while preserving blocked placeholders for missing external evidence.",
    code: devpostExcerpt,
    footer: "The final Submit button stays out of scope until public proof is complete.",
  }],
  ["04-gpt-payload.html", {
    eyebrow: "GPT-5.6 boundary",
    title: "Live review is prepared, not faked",
    summary: "The repo includes a Responses API payload builder for GPT-5.6 review after a verified no-billing path exists.",
    code: payloadExcerpt,
    footer: "No API key is read and no paid network call is made by the local demo.",
  }],
  ["05-fixture.html", {
    eyebrow: "Real last-mile fixture",
    title: "The Qwen packet proves the use case",
    summary: "The fixture shows why builders need source freshness, public proof ledgers, and exact blocker tracking near a deadline.",
    code: fixtureExcerpt,
    footer: "Fixture content is public submission metadata, not credentials.",
  }],
  ["06-close.html", {
    eyebrow: "Judge path",
    title: "Reproducible in one command",
    summary: "Judges can run the CLI locally, inspect Markdown and JSON reports, and verify why the decision is go, downgrade, or stop.",
    points: [
      "uv run submitops-scout ../submission-packets/openai-build-week.md .",
      "uv run pytest",
      "uv run ruff check .",
      "uv run ty check src tests",
    ],
    footer: "Next step: insert /feedback evidence before final Devpost submit.",
  }],
];

for (const [filename, config] of slides) {
  fs.writeFileSync(path.join(slideDir, filename), slideHtml(config), "utf8");
}

const voiceover = `SubmitOps Scout is a Codex-built developer tool for OpenAI Build Week.

The problem is the final mile of a hackathon submission. Teams have working code, but the rules drift, proof links are missing, demo videos run long, and people are tempted to paste unsupported claims under deadline pressure.

SubmitOps Scout reads a competition packet and a local repository. It extracts deadlines, tracks, required materials, account gates, and judging notes. Then it scans the repository for README files, license, tests, sample data, public links, Codex mentions, GPT-5.6 evidence, feedback Session ID evidence, video URLs, and secret-risk patterns.

The output is a readiness packet with a clear decision. In this live Build Week state the decision is downgrade because the slash feedback Session ID is still missing. The public YouTube demo URL is now recorded as proof. That is intentional: the tool refuses to turn placeholders into final submission claims.

It also writes a Devpost field map. The project title, category, short description, repository URL, YouTube demo URL, judge instructions, and rubric fit are ready, while missing slash feedback evidence remains visibly blocked.

For GPT-5.6, the repository prepares a Responses API review payload without reading secrets or making a network call. A live review should only run after the entrant verifies free or prepaid credits and no auto top-up.

The Qwen Cloud fixture demonstrates the real use case: a mature submission with public assets, source snapshots, and exact external blockers. SubmitOps Scout gives builders the same disciplined final checklist for every competition.

Judges can clone the public repository, run the CLI, run tests, lint, and type checks, and inspect the generated Markdown and JSON artifacts. The tool helps teams ship truthful, judge-ready submissions without losing the human approval boundary.`;

fs.writeFileSync(path.join(outDir, "voiceover.txt"), voiceover, "utf8");
fs.writeFileSync(path.join(outDir, "metadata.json"), JSON.stringify({
  generatedAt: new Date().toISOString(),
  slideCount: slides.length,
  decision: packet.decision,
  blockers: packet.blockers,
  videoStatus: "published-youtube-proof-recorded",
}, null, 2), "utf8");
NODE

capture() {
  local url="$1"
  local png="$2"
  npx --yes playwright screenshot -b chromium --viewport-size "1280,720" --timeout 30000 "$url" "$png" >/dev/null
}

capture "file://$SLIDE_DIR/01-title.html" "$FRAME_DIR/01-title.png"
capture "file://$SLIDE_DIR/02-readiness.html" "$FRAME_DIR/02-readiness.png"
capture "file://$SLIDE_DIR/03-devpost-map.html" "$FRAME_DIR/03-devpost-map.png"
capture "file://$SLIDE_DIR/04-gpt-payload.html" "$FRAME_DIR/04-gpt-payload.png"
capture "file://$SLIDE_DIR/05-fixture.html" "$FRAME_DIR/05-fixture.png"
capture "file://$SLIDE_DIR/06-close.html" "$FRAME_DIR/06-close.png"

CONCAT="$WORK_DIR/frames.txt"
: > "$CONCAT"
for frame in "$FRAME_DIR"/*.png; do
  printf "file '%s'\n" "$frame" >> "$CONCAT"
  printf "duration 18\n" >> "$CONCAT"
done
printf "file '%s'\n" "$(ls "$FRAME_DIR"/*.png | sort | tail -n 1)" >> "$CONCAT"

ffmpeg -y -loglevel error -f concat -safe 0 -i "$CONCAT" \
  -vf "fps=30,format=yuv420p" \
  -c:v libx264 -movflags +faststart "$BASE_VIDEO"

if command -v say >/dev/null 2>&1; then
  say -r 180 -o "$AUDIO" -f "$VOICEOVER"
  ffmpeg -y -loglevel error -i "$BASE_VIDEO" -i "$AUDIO" \
    -c:v copy -c:a aac -b:a 128k -shortest -movflags +faststart "$VIDEO"
else
  cp "$BASE_VIDEO" "$VIDEO"
fi

ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height \
  -of json "$VIDEO" > "$PROBE"

DURATION="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO")"
if ! awk "BEGIN { exit !($DURATION < 179) }"; then
  echo "Rendered video is too long: ${DURATION}s" >&2
  exit 1
fi

shasum -a 256 "$VIDEO" > "$SHA"

echo "OpenAI Build Week demo video preupload asset: $VIDEO"
echo "Duration seconds: $DURATION"
echo "ffprobe: $PROBE"
echo "sha256: $SHA"
