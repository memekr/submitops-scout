from __future__ import annotations

from html import escape
from pathlib import Path
from urllib import parse

from submitops_scout.core import PublicUrlCheck, ReadinessCheck, SubmissionPacket


def _html(value: object) -> str:
    return escape(str(value), quote=True)


def _first_public_url(packet: SubmissionPacket, fragment: str) -> str:
    return next(
        (url for url in packet.evidence.public_urls if fragment in url.lower()),
        "",
    )


def _repo_url(packet: SubmissionPacket) -> str:
    return (
        _first_public_url(packet, "github.com/")
        or _first_public_url(packet, "gitlab.com/")
        or _first_public_url(packet, "bitbucket.org/")
    )


def _video_url(packet: SubmissionPacket) -> str:
    return next(
        (url for url in packet.evidence.video_urls if "oembed" not in url.lower()),
        packet.evidence.video_urls[0] if packet.evidence.video_urls else "",
    )


def _youtube_id(url: str) -> str:
    parsed = parse.urlparse(url)
    host = parsed.netloc.lower()
    if host.endswith("youtu.be"):
        return parsed.path.strip("/").split("/", maxsplit=1)[0]
    if "youtube.com" in host:
        values = parse.parse_qs(parsed.query).get("v", [])
        return values[0] if values else ""
    return ""


def _video_thumbnail(url: str) -> str:
    video_id = _youtube_id(url)
    if not video_id:
        return ""
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"


def _status_label(status: str) -> str:
    if status == "pass":
        return "PASS"
    if status == "stop":
        return "STOP"
    return "MISSING"


def _status_span(status: str) -> str:
    return (
        f'<span class="status status-{_html(status)}">'
        f"{_html(_status_label(status))}</span>"
    )


def _check_rows(checks: tuple[ReadinessCheck, ...]) -> str:
    return "\n".join(
        f"""
        <article class="check" data-status="{_html(check.status)}">
          {_status_span(check.status)}
          <h3>{_html(check.name)}</h3>
          <p>{_html(check.detail or "No supporting evidence recorded.")}</p>
        </article>
        """.strip()
        for check in checks
    )


def _url_rows(checks: tuple[PublicUrlCheck, ...]) -> str:
    if not checks:
        return """
        <tr>
          <td colspan="4">Run with --verify-public-urls to populate public URL checks.</td>
        </tr>
        """.strip()
    return "\n".join(
        f"""
        <tr>
          <td>{_status_span(check.status)}</td>
          <td>{_html(check.expectation)}</td>
          <td><a href="{_html(check.url)}">{_html(check.url)}</a></td>
          <td>{_html(check.detail)}</td>
        </tr>
        """.strip()
        for check in checks
    )


def _blocker_items(packet: SubmissionPacket) -> str:
    if not packet.blockers:
        return "<li>No blockers recorded.</li>"
    return "\n".join(f"<li>{_html(blocker)}</li>" for blocker in packet.blockers)


def _source_links(packet: SubmissionPacket) -> str:
    return "\n".join(
        f'<a href="{_html(url)}">{_html(url)}</a>' for url in packet.event.sources[:6]
    )


def _sample_paths(packet: SubmissionPacket) -> str:
    paths = packet.evidence.sample_data[:8]
    if not paths:
        return "<li>No sample data found.</li>"
    return "\n".join(f"<li>{_html(path)}</li>" for path in paths)


def _metric(label: str, value: object) -> str:
    return f"""
    <div class="metric">
      <span>{_html(label)}</span>
      <strong>{_html(value)}</strong>
    </div>
    """.strip()


def _judge_command() -> str:
    return """git clone https://github.com/memekr/submitops-scout.git
cd submitops-scout
uv sync --all-groups
uv run submitops-scout fixtures/openai-build-week-packet.md . \\
  --out reports/openai-build-week-submitops-scout.md \\
  --json reports/openai-build-week-submitops-scout.json \\
  --devpost-map submission/openai-build-week-devpost-field-map.md \\
  --gpt56-payload reports/openai-build-week-gpt56-payload.json \\
  --gpt56-status
uv run pytest"""


def render_static_demo(packet: SubmissionPacket) -> str:
    answers = packet.event.draft_answers
    title = answers.title or packet.event.name.removesuffix(" Packet")
    description = answers.short_description or "Hackathon submission readiness scanner."
    repo_url = _repo_url(packet)
    video_url = _video_url(packet)
    thumbnail = _video_thumbnail(video_url)
    pass_count = sum(1 for check in packet.checks if check.status == "pass")
    missing_count = sum(1 for check in packet.checks if check.status != "pass")
    public_pass = sum(1 for check in packet.public_url_checks if check.status == "pass")
    thumbnail_html = (
        f'<img src="{_html(thumbnail)}" alt="Public demo video thumbnail">'
        if thumbnail
        else '<div class="video-placeholder">No public thumbnail recorded</div>'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>{_html(title)} | SubmitOps Scout</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172033;
      --muted: #5b6578;
      --line: #d8dee9;
      --paper: #f7f9fc;
      --panel: #ffffff;
      --green: #0f766e;
      --amber: #b45309;
      --red: #b42318;
      --blue: #2357c5;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font: 16px/1.5 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
    }}
    a {{ color: var(--blue); overflow-wrap: anywhere; }}
    header {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: end;
      padding: 32px max(24px, calc((100vw - 1120px) / 2));
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      margin: 0 0 6px;
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0;
      text-transform: uppercase;
    }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ margin-bottom: 10px; font-size: clamp(2rem, 4vw, 3.8rem); line-height: 1; }}
    h2 {{ font-size: 1.25rem; }}
    .lede {{ max-width: 760px; margin-bottom: 0; color: var(--muted); }}
    .decision {{
      min-width: 180px;
      padding: 16px;
      border: 1px solid var(--line);
      background: #fef7ed;
      text-align: right;
    }}
    .decision strong {{ display: block; font-size: 1.35rem; color: var(--amber); }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 24px;
    }}
    section {{ margin: 0 0 24px; }}
    .overview {{
      display: grid;
      grid-template-columns: minmax(280px, 0.9fr) minmax(320px, 1.1fr);
      gap: 20px;
      align-items: stretch;
    }}
    .video {{
      display: block;
      min-height: 260px;
      border: 1px solid var(--line);
      background: #111827;
      overflow: hidden;
    }}
    .video img {{
      width: 100%;
      height: 100%;
      min-height: 260px;
      display: block;
      object-fit: cover;
    }}
    .video-placeholder {{
      min-height: 260px;
      display: grid;
      place-items: center;
      color: #ffffff;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .metric {{
      padding: 16px;
      border: 1px solid var(--line);
      background: var(--panel);
    }}
    .metric span {{ display: block; color: var(--muted); font-size: 0.85rem; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 1.5rem; }}
    .panel {{
      padding: 20px;
      border: 1px solid var(--line);
      background: var(--panel);
    }}
    .split {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 20px;
    }}
    .toolbar {{
      display: flex;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }}
    select {{
      min-height: 36px;
      border: 1px solid var(--line);
      background: #ffffff;
      color: var(--ink);
    }}
    .checks {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
    }}
    .check {{
      min-height: 132px;
      padding: 14px;
      border: 1px solid var(--line);
      background: #ffffff;
    }}
    .check h3 {{ margin: 10px 0 6px; font-size: 1rem; }}
    .check p {{ margin: 0; color: var(--muted); overflow-wrap: anywhere; }}
    .status {{
      display: inline-block;
      padding: 3px 7px;
      border: 1px solid currentColor;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0;
    }}
    .status-pass {{ color: var(--green); }}
    .status-missing {{ color: var(--amber); }}
    .status-stop {{ color: var(--red); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
    }}
    th, td {{
      padding: 10px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }}
    th {{ color: var(--muted); font-size: 0.84rem; }}
    pre {{
      margin: 0;
      padding: 16px;
      overflow: auto;
      background: #101828;
      color: #e6edf6;
    }}
    ul {{ margin-bottom: 0; padding-left: 20px; }}
    .sources {{
      display: grid;
      gap: 8px;
    }}
    @media (max-width: 780px) {{
      header, .overview, .split {{ grid-template-columns: 1fr; }}
      header {{ align-items: start; }}
      .decision {{ text-align: left; }}
      .metrics {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <p class="eyebrow">{_html(packet.event.name)}</p>
      <h1>{_html(title)}</h1>
      <p class="lede">{_html(description)}</p>
    </div>
    <div class="decision">
      <span>Decision</span>
      <strong>{_html(packet.decision.upper())}</strong>
      <span>{_html(packet.generated_at)}</span>
    </div>
  </header>
  <main>
    <section class="overview">
      <a class="video" href="{_html(video_url)}">{thumbnail_html}</a>
      <div class="metrics">
        {_metric("Deadline", packet.event.deadline or "Unknown")}
        {_metric("Readiness checks passed", f"{pass_count}/{len(packet.checks)}")}
        {_metric("Open blockers", missing_count)}
        {_metric("Public URLs verified", public_pass)}
        {_metric("Repository", repo_url or "Missing")}
        {_metric("Scanned text files", packet.evidence.scanned_files)}
      </div>
    </section>
    <section class="split">
      <div class="panel">
        <h2>Current Blockers</h2>
        <ul>{_blocker_items(packet)}</ul>
      </div>
      <div class="panel">
        <h2>Judge Assets</h2>
        <ul>
          <li>Repository: <a href="{_html(repo_url)}">{_html(repo_url or "Missing")}</a></li>
          <li>Demo video: <a href="{_html(video_url)}">{_html(video_url or "Missing")}</a></li>
          <li>Samples: {len(packet.evidence.sample_data)}</li>
          <li>Tests: {len(packet.evidence.test_files)}</li>
        </ul>
      </div>
    </section>
    <section class="panel">
      <div class="toolbar">
        <h2>Readiness Checks</h2>
        <label>Filter
          <select id="check-filter">
            <option value="all">All</option>
            <option value="pass">Pass</option>
            <option value="missing">Missing</option>
            <option value="stop">Stop</option>
          </select>
        </label>
      </div>
      <div class="checks" id="checks">{_check_rows(packet.checks)}</div>
    </section>
    <section class="panel">
      <h2>Public URL Verification</h2>
      <table>
        <thead>
          <tr><th>Status</th><th>Expectation</th><th>URL</th><th>Detail</th></tr>
        </thead>
        <tbody>{_url_rows(packet.public_url_checks)}</tbody>
      </table>
    </section>
    <section class="split">
      <div class="panel">
        <h2>Judge Command</h2>
        <pre>{_html(_judge_command())}</pre>
      </div>
      <div class="panel">
        <h2>Samples and Sources</h2>
        <ul>{_sample_paths(packet)}</ul>
        <div class="sources">{_source_links(packet)}</div>
      </div>
    </section>
  </main>
  <script>
    const filter = document.querySelector("#check-filter");
    const checks = Array.from(document.querySelectorAll(".check"));
    filter.addEventListener("change", () => {{
      for (const check of checks) {{
        const show = filter.value === "all" || check.dataset.status === filter.value;
        check.style.display = show ? "" : "none";
      }}
    }});
  </script>
</body>
</html>
"""


def write_static_demo(packet: SubmissionPacket, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_static_demo(packet), encoding="utf-8")
