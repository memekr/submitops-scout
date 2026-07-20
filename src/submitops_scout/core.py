from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from html import unescape
from pathlib import Path
from typing import Any
from urllib import error, parse, request

SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".playwright-cli",
    ".ruff_cache",
    ".ty",
    ".venv",
    "__pycache__",
    "node_modules",
    "output",
}
TEXT_SUFFIXES = {
    ".cfg",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {"LICENSE", "NOTICE", "Dockerfile", "Makefile"}
MAX_TEXT_BYTES = 1_000_000
SUBMISSION_EVIDENCE_TEXT_SKIP_PREFIXES = ("docs/", "reports/", "tests/")
SUBMISSION_EVIDENCE_TEXT_SKIP_FRAGMENTS = ("devpost-field-map",)
VIDEO_SUFFIXES = {".mp4", ".mov", ".webm"}
DECK_SUFFIXES = {".ppt", ".pptx", ".pdf"}
SAMPLE_SUFFIXES = {".csv", ".json", ".jsonl", ".md", ".tsv"}
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    (
        "inline credential assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{18,}"
        ),
    ),
)
URL_PATTERN = re.compile(r"https?://[^\s)<>\"'`]+")
URL_TRAILING_PUNCTUATION = ".,:;"
FEEDBACK_ID_PATTERN = re.compile(
    r"(?i)(?:/feedback\s+)?session id\s*[:=-]\s*"
    r"(?!pending|placeholder|todo|tbd|missing)([A-Za-z0-9_-]{12,})"
)
GPT56_LIVE_EVIDENCE_PATTERN = re.compile(
    r"(?i)(?:"
    r"(?:live\s+)?gpt[- ]?5\.6\s+(?:review|api|responses api|evidence)"
    r"|(?:live\s+)?(?:review|api|responses api|evidence)\s+.*gpt[- ]?5\.6"
    r").*(?:complete|completed|pass|passed|captured|response id|resp_[A-Za-z0-9_-]+)"
)
BLOCKED_EVIDENCE_TERMS = (
    "blocked",
    "do not claim",
    "do not submit",
    "does not",
    "missing",
    "no live",
    "has not",
    "not been",
    "not captured",
    "not complete",
    "not configured",
    "not run",
    "only after",
    "pending",
    "placeholder",
    "todo",
    "without making a network call",
)
TRACK_NAMES = (
    "Apps for Your Life",
    "Work and Productivity",
    "Developer Tools",
    "Education",
)
REQUIRED_KEYWORDS = (
    "working project",
    "installation instructions",
    "supported platforms",
    "category",
    "project description",
    "demo video",
    "code repository",
    "repository URL",
    "sample data",
    "README",
    "/feedback",
)
ACCOUNT_KEYWORDS = (
    "api credits",
    "codex credits",
    "devpost account",
    "openai/codex access",
    "openai account",
)
BLOCKER_FACT_TERMS = (
    "blocked",
    "not captured",
    "not complete",
    "not inserted",
    "not yet",
    "pending",
)
HTTP_OK_MIN = 200
HTTP_REDIRECT_MAX_EXCLUSIVE = 400
HTTP_NOT_FOUND = 404
HTTP_GONE = 410


@dataclass(frozen=True)
class DraftAnswers:
    title: str = ""
    short_description: str = ""
    what_it_does: str = ""
    why_it_can_win: str = ""


@dataclass(frozen=True)
class EventSnapshot:
    name: str
    event_url: str
    deadline: str
    sources: tuple[str, ...]
    tracks: tuple[str, ...]
    required_materials: tuple[str, ...]
    account_requirements: tuple[str, ...]
    source_notes: tuple[str, ...]
    draft_answers: DraftAnswers
    captured_at: str


@dataclass(frozen=True)
class SecretFinding:
    path: str
    label: str
    line: int


@dataclass(frozen=True)
class RepoEvidence:
    root: str
    readme_paths: tuple[str, ...]
    license_paths: tuple[str, ...]
    setup_paths: tuple[str, ...]
    test_files: tuple[str, ...]
    sample_data: tuple[str, ...]
    video_assets: tuple[str, ...]
    video_urls: tuple[str, ...]
    deck_assets: tuple[str, ...]
    public_urls: tuple[str, ...]
    codex_mentions: tuple[str, ...]
    gpt56_mentions: tuple[str, ...]
    gpt56_live_evidence_paths: tuple[str, ...]
    feedback_mentions: tuple[str, ...]
    devpost_flow_paths: tuple[str, ...]
    secret_findings: tuple[SecretFinding, ...]
    scanned_files: int


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    status: str
    detail: str


@dataclass(frozen=True)
class PublicUrlCheck:
    url: str
    expectation: str
    status: str
    http_status: int | None
    detail: str


@dataclass(frozen=True)
class SubmissionPacket:
    event: EventSnapshot
    evidence: RepoEvidence
    checks: tuple[ReadinessCheck, ...]
    decision: str
    blockers: tuple[str, ...]
    generated_at: str
    public_url_checks: tuple[PublicUrlCheck, ...] = ()


@dataclass
class _EvidenceCollector:
    readmes: list[str]
    licenses: list[str]
    setup_paths: list[str]
    tests: list[str]
    samples: list[str]
    videos: list[str]
    decks: list[str]
    urls: list[str]
    video_urls: list[str]
    codex_mentions: list[str]
    gpt56_mentions: list[str]
    gpt56_live_evidence_paths: list[str]
    feedback_mentions: list[str]
    devpost_flow_paths: list[str]
    secrets: list[SecretFinding]
    scanned_files: int = 0

    def add_path(self, path: Path, rel: str) -> None:
        lower_rel = rel.lower()
        suffix = path.suffix.lower()
        if path.name.lower().startswith("readme"):
            self.readmes.append(rel)
        if path.name.upper().startswith("LICENSE"):
            self.licenses.append(rel)
        if suffix in VIDEO_SUFFIXES:
            self.videos.append(rel)
        if suffix in DECK_SUFFIXES:
            self.decks.append(rel)
        if "test" in lower_rel and suffix == ".py":
            self.tests.append(rel)
        if (
            any(part in lower_rel for part in ("reports/", "fixtures/", "examples/", "sample"))
            and suffix in SAMPLE_SUFFIXES
        ):
            self.samples.append(rel)
        if (
            "devpost-registration-gate" in lower_rel
            or "devpost-draft-access-recheck" in lower_rel
        ):
            self.devpost_flow_paths.append(rel)

    def add_text(self, rel: str, text: str) -> None:
        self.scanned_files += 1
        if re.search(r"\b(setup|install|usage|run|quickstart)\b", text, re.IGNORECASE):
            self.setup_paths.append(rel)
        if "codex" in text.lower():
            self.codex_mentions.append(rel)
        if "gpt-5.6" in text.lower() or "gpt 5.6" in text.lower():
            self.gpt56_mentions.append(rel)
        if _has_live_gpt56_evidence(text):
            self.gpt56_live_evidence_paths.append(rel)
        if FEEDBACK_ID_PATTERN.search(text):
            self.feedback_mentions.append(rel)
        found_urls = [
            clean_url
            for url in URL_PATTERN.findall(text)
            if _is_usable_public_url(clean_url := _clean_extracted_url(url))
        ]
        self.urls.extend(found_urls)
        self.video_urls.extend(
            url
            for url in found_urls
            if any(
                host in url.lower()
                for host in ("youtube.com", "youtu.be", "vimeo.com", "youku.com")
            )
        )
        self.secrets.extend(_find_secret_lines(rel, text))

    def to_evidence(self, root: Path) -> RepoEvidence:
        return RepoEvidence(
            root=str(root),
            readme_paths=_unique(self.readmes),
            license_paths=_unique(self.licenses),
            setup_paths=_unique(self.setup_paths),
            test_files=_unique(self.tests),
            sample_data=_unique(self.samples),
            video_assets=_unique(self.videos),
            video_urls=_unique(self.video_urls),
            deck_assets=_unique(self.decks),
            public_urls=_unique(self.urls)[:40],
            codex_mentions=_unique(self.codex_mentions),
            gpt56_mentions=_unique(self.gpt56_mentions),
            gpt56_live_evidence_paths=_unique(self.gpt56_live_evidence_paths),
            feedback_mentions=_unique(self.feedback_mentions),
            devpost_flow_paths=_unique(self.devpost_flow_paths),
            secret_findings=tuple(self.secrets),
            scanned_files=self.scanned_files,
        )


def _new_collector() -> _EvidenceCollector:
    return _EvidenceCollector(
        readmes=[],
        licenses=[],
        setup_paths=[],
        tests=[],
        samples=[],
        videos=[],
        decks=[],
        urls=[],
        video_urls=[],
        codex_mentions=[],
        gpt56_mentions=[],
        gpt56_live_evidence_paths=[],
        feedback_mentions=[],
        devpost_flow_paths=[],
        secrets=[],
    )


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _unique(items: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = item.strip().rstrip(".,")
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return tuple(result)


def _bullet_text(line: str) -> str:
    return line.strip().lstrip("-*[] xX").strip()


def _is_markdown_bullet(line: str) -> bool:
    return line.strip().startswith(("-", "*"))


def _is_draft_answer_line(line: str) -> bool:
    stripped = line.strip().lower()
    return stripped.startswith(
        (
            ">",
            "title:",
            "short description:",
            "what it does:",
            "why it can win:",
        )
    )


def _is_source_only_line(line: str) -> bool:
    text = _bullet_text(line)
    return bool(URL_PATTERN.fullmatch(text))


def _bullet_items(lines: list[str]) -> tuple[str, ...]:
    items: list[str] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                items.append(" ".join(current))
                current = []
            continue
        if _is_markdown_bullet(line):
            if current:
                items.append(" ".join(current))
            current = [_bullet_text(line)]
            continue
        if current and line[:1].isspace() and not _is_draft_answer_line(line):
            current.append(stripped)
            continue
        if current:
            items.append(" ".join(current))
            current = []
    if current:
        items.append(" ".join(current))
    return tuple(items)


def _fact_line(line: str) -> str:
    if _is_draft_answer_line(line) or _is_source_only_line(line):
        return ""
    return _bullet_text(line)


def _clean_markdown_value(value: str) -> str:
    clean = value.strip().strip()
    if clean.startswith(">"):
        clean = clean[1:].strip()
    return clean.strip("`").strip()


def _extract_inline_value(lines: list[str], label: str) -> str:
    label_lower = label.lower()
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith(label_lower):
            return _clean_markdown_value(stripped[len(label) :])
    return ""


def _extract_blockquote_after(lines: list[str], label: str) -> str:
    label_lower = label.lower()
    for index, line in enumerate(lines):
        if not line.strip().lower().startswith(label_lower):
            continue
        values: list[str] = []
        for follow in lines[index + 1 :]:
            stripped = follow.strip()
            if not stripped:
                if values:
                    break
                continue
            if stripped.startswith(">"):
                values.append(_clean_markdown_value(stripped))
                continue
            if values:
                break
            if not stripped.startswith("#"):
                return _clean_markdown_value(stripped)
        return " ".join(values)
    return ""


def _extract_draft_answers(lines: list[str]) -> DraftAnswers:
    return DraftAnswers(
        title=_extract_inline_value(lines, "Title:"),
        short_description=_extract_blockquote_after(lines, "Short description:"),
        what_it_does=_extract_blockquote_after(lines, "What it does:"),
        why_it_can_win=_extract_blockquote_after(lines, "Why it can win:"),
    )


def parse_event_packet(path: Path) -> EventSnapshot:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    heading = next(
        (line.lstrip("# ").strip() for line in lines if line.startswith("# ")),
        path.stem,
    )
    urls = _unique(
        [
            clean_url
            for url in URL_PATTERN.findall(text)
            if _is_usable_public_url(clean_url := _clean_extracted_url(url))
        ],
    )
    event_url = next((url for url in urls if "devpost.com" in url), urls[0] if urls else "")
    deadline = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- Public deadline:"):
            deadline = stripped.removeprefix("- Public deadline:").strip()
            break
        if stripped.startswith("Deadline:"):
            deadline = stripped.removeprefix("Deadline:").strip()
            break
    tracks = tuple(track for track in TRACK_NAMES if track.lower() in text.lower())
    required = [
        fact
        for item in _bullet_items(lines)
        if (fact := _fact_line(item))
        if not any(term in fact.lower() for term in BLOCKER_FACT_TERMS)
        if any(keyword.lower() in fact.lower() for keyword in REQUIRED_KEYWORDS)
    ]
    accounts = [
        fact
        for item in _bullet_items(lines)
        if (fact := _fact_line(item))
        if any(term in fact.lower() for term in ACCOUNT_KEYWORDS)
    ]
    notes = [
        fact
        for line in lines
        if (fact := _fact_line(line))
        if any(term in fact.lower() for term in ("rules", "participant", "deadline", "eligible"))
    ]
    return EventSnapshot(
        name=heading,
        event_url=event_url,
        deadline=deadline,
        sources=urls,
        tracks=tracks,
        required_materials=_unique(required)[:12],
        account_requirements=_unique(accounts)[:8],
        source_notes=_unique(notes)[:12],
        draft_answers=_extract_draft_answers(lines),
        captured_at=_now_iso(),
    )


def _is_scannable(path: Path) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES


def _relative_parts(path: Path, root: Path) -> tuple[str, ...]:
    return path.relative_to(root).parts


def _read_text(path: Path) -> str:
    if path.stat().st_size > MAX_TEXT_BYTES:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _find_secret_lines(rel: str, text: str) -> tuple[SecretFinding, ...]:
    findings: list[SecretFinding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "OPENAI_API_KEY" in line and "Bearer $" in line:
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(SecretFinding(rel, label, line_number))
    return tuple(findings)


def _has_live_gpt56_evidence(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(">"):
            continue
        lower = line.lower()
        if any(term in lower for term in BLOCKED_EVIDENCE_TERMS):
            continue
        if GPT56_LIVE_EVIDENCE_PATTERN.search(line):
            return True
    return False


def _is_usable_public_url(url: str) -> bool:
    if "{" in url or "}" in url:
        return False
    parsed = parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    query = parse.parse_qs(parsed.query, keep_blank_values=True)
    return not any(key == "url" and values == [""] for key, values in query.items())


def _clean_extracted_url(url: str) -> str:
    return unescape(url.strip().split("<", maxsplit=1)[0]).rstrip(URL_TRAILING_PUNCTUATION)


def scan_repo_evidence(root: Path) -> RepoEvidence:
    collector = _new_collector()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in _relative_parts(path, root)):
            continue
        rel = path.relative_to(root).as_posix()
        collector.add_path(path, rel)
        if not _is_scannable(path):
            continue
        if rel.startswith(SUBMISSION_EVIDENCE_TEXT_SKIP_PREFIXES) or any(
            fragment in rel.lower() for fragment in SUBMISSION_EVIDENCE_TEXT_SKIP_FRAGMENTS
        ):
            continue
        text = _read_text(path)
        if not text:
            continue
        collector.add_text(rel, text)
    return collector.to_evidence(root)


def _check(name: str, *, passed: bool, detail: str) -> ReadinessCheck:
    return ReadinessCheck(name=name, status="pass" if passed else "missing", detail=detail)


def assess_readiness(event: EventSnapshot, evidence: RepoEvidence) -> SubmissionPacket:
    rules_posted = any("official rules" in note.lower() for note in event.source_notes)
    checks = (
        _check(
            "official rules captured",
            passed=rules_posted,
            detail="Packet records Official Rules source state.",
        ),
        _check(
            "README present",
            passed=bool(evidence.readme_paths),
            detail=", ".join(evidence.readme_paths),
        ),
        _check(
            "license present",
            passed=bool(evidence.license_paths),
            detail=", ".join(evidence.license_paths),
        ),
        _check(
            "public repository URL present",
            passed=_has_public_repo_url(evidence),
            detail=_repo_url(evidence),
        ),
        _check(
            "setup path present",
            passed=bool(evidence.setup_paths),
            detail=", ".join(evidence.setup_paths[:5]),
        ),
        _check(
            "tests present",
            passed=bool(evidence.test_files),
            detail=f"{len(evidence.test_files)} test files",
        ),
        _check(
            "sample data present",
            passed=bool(evidence.sample_data),
            detail=", ".join(evidence.sample_data[:5]),
        ),
        _check(
            "Codex evidence present",
            passed=bool(evidence.codex_mentions),
            detail=", ".join(evidence.codex_mentions[:5]),
        ),
        _check(
            "GPT-5.6 evidence present",
            passed=bool(evidence.gpt56_mentions),
            detail=", ".join(evidence.gpt56_mentions[:5]),
        ),
        _check(
            "live GPT-5.6 review evidence present",
            passed=bool(evidence.gpt56_live_evidence_paths),
            detail=", ".join(evidence.gpt56_live_evidence_paths[:5]),
        ),
        _check(
            "/feedback Session ID present",
            passed=bool(evidence.feedback_mentions),
            detail=", ".join(evidence.feedback_mentions[:5]),
        ),
        _check(
            "public demo video present",
            passed=bool(evidence.video_urls),
            detail=", ".join(evidence.video_urls[:3]),
        ),
        _check(
            "secret scan clear",
            passed=not evidence.secret_findings,
            detail=f"{len(evidence.secret_findings)} findings",
        ),
    )
    blockers = tuple(check.name for check in checks if check.status != "pass")
    if evidence.secret_findings or not rules_posted:
        decision = "stop"
    elif blockers:
        decision = "downgrade"
    else:
        decision = "go"
    return SubmissionPacket(
        event=event,
        evidence=evidence,
        checks=checks,
        decision=decision,
        blockers=blockers,
        generated_at=_now_iso(),
    )


def _video_oembed_url(url: str) -> str:
    lower = url.lower()
    if "youtube.com/oembed" in lower or "vimeo.com/api/oembed" in lower:
        return url
    if "youtu.be/" in lower or "youtube.com/watch" in lower:
        encoded_url = parse.quote(url, safe=":/")
        return f"https://www.youtube.com/oembed?url={encoded_url}&format=json"
    if "vimeo.com/" in lower:
        return "https://vimeo.com/api/oembed.json?url=" + parse.quote(url, safe=":/")
    return url


def _verification_targets(
    packet: SubmissionPacket,
    required_urls: tuple[str, ...],
) -> tuple[str, ...]:
    targets: list[str] = []
    repo = _repo_url(packet.evidence)
    if repo.startswith("http"):
        targets.append(repo)
    targets.extend(_video_oembed_url(url) for url in packet.evidence.video_urls)
    targets.extend(required_urls)
    return _unique(targets)


def _is_http_url(url: str) -> bool:
    return parse.urlparse(url).scheme in {"http", "https"}


def _fetch_status(url: str, timeout_seconds: float) -> tuple[int | None, str]:
    if not _is_http_url(url):
        return None, "unsupported URL scheme"
    req = request.Request(  # noqa: S310
        url,
        method="GET",
        headers={"User-Agent": "submitops-scout/0.1 public-url-verifier"},
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:  # noqa: S310
            response.read(1)
            return response.status, f"HTTP {response.status}"
    except error.HTTPError as exc:
        return exc.code, f"HTTP {exc.code}"
    except error.URLError as exc:
        return None, f"{exc.__class__.__name__}: {exc.reason}"
    except TimeoutError:
        return None, "TimeoutError"


def _verify_required_url(url: str, timeout_seconds: float) -> PublicUrlCheck:
    status_code, detail = _fetch_status(url, timeout_seconds)
    passed = (
        status_code is not None
        and HTTP_OK_MIN <= status_code < HTTP_REDIRECT_MAX_EXCLUSIVE
    )
    return PublicUrlCheck(
        url=url,
        expectation="reachable",
        status="pass" if passed else "missing",
        http_status=status_code,
        detail=detail,
    )


def _verify_absent_url(url: str, timeout_seconds: float) -> PublicUrlCheck:
    status_code, detail = _fetch_status(url, timeout_seconds)
    passed = status_code in {HTTP_NOT_FOUND, HTTP_GONE}
    return PublicUrlCheck(
        url=url,
        expectation="absent",
        status="pass" if passed else "stop",
        http_status=status_code,
        detail=detail,
    )


def verify_public_urls(
    packet: SubmissionPacket,
    *,
    required_urls: tuple[str, ...] = (),
    absent_urls: tuple[str, ...] = (),
    timeout_seconds: float = 10.0,
) -> SubmissionPacket:
    url_checks = tuple(
        _verify_required_url(url, timeout_seconds)
        for url in _verification_targets(packet, required_urls)
    ) + tuple(_verify_absent_url(url, timeout_seconds) for url in _unique(list(absent_urls)))
    url_readiness_checks = tuple(
        ReadinessCheck(
            name=f"public URL {check.expectation}: {check.url}",
            status="pass" if check.status == "pass" else "missing",
            detail=check.detail,
        )
        for check in url_checks
    )
    checks = packet.checks + url_readiness_checks
    blockers = tuple(check.name for check in checks if check.status != "pass")
    if any(check.status == "stop" for check in url_checks) or packet.decision == "stop":
        decision = "stop"
    elif blockers:
        decision = "downgrade"
    else:
        decision = "go"
    return SubmissionPacket(
        event=packet.event,
        evidence=packet.evidence,
        checks=checks,
        decision=decision,
        blockers=blockers,
        generated_at=_now_iso(),
        public_url_checks=url_checks,
    )


def packet_to_dict(packet: SubmissionPacket) -> dict[str, Any]:
    return asdict(packet)


def _bullets(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None found"


def _pick_track(event: EventSnapshot) -> str:
    draft_text = (
        f"{event.draft_answers.title} "
        f"{event.draft_answers.short_description} "
        f"{event.draft_answers.what_it_does} "
        f"{event.draft_answers.why_it_can_win}"
    ).lower()
    for track in event.tracks:
        if track.lower() in draft_text:
            return track
    if "developer tool" in draft_text or "devops" in draft_text:
        return "Developer Tools"
    if "Developer Tools" in event.tracks:
        return "Developer Tools"
    return event.tracks[0] if event.tracks else "BLOCKED: choose category in Devpost"


def _first_url_with(urls: tuple[str, ...], fragment: str) -> str:
    return next((url for url in urls if fragment in url.lower()), "")


def _has_public_repo_url(evidence: RepoEvidence) -> bool:
    repo_hosts = ("github.com/", "gitlab.com/", "bitbucket.org/")
    return any(host in url.lower() for url in evidence.public_urls for host in repo_hosts)


def _repo_url(evidence: RepoEvidence) -> str:
    url = _first_url_with(evidence.public_urls, "github.com/")
    if url:
        return url
    url = _first_url_with(evidence.public_urls, "gitlab.com/")
    if url:
        return url
    url = _first_url_with(evidence.public_urls, "bitbucket.org/")
    if url:
        return url
    return "BLOCKED: public repository URL not verified yet"


def _video_url(evidence: RepoEvidence) -> str:
    if evidence.video_urls:
        return evidence.video_urls[0]
    return "BLOCKED: public YouTube demo URL not recorded yet"


def _feedback_value(evidence: RepoEvidence) -> str:
    if evidence.feedback_mentions:
        return "Evidence found in " + ", ".join(evidence.feedback_mentions[:3])
    return "BLOCKED: paste /feedback Codex Session ID from primary build thread"


def _gpt56_live_value(evidence: RepoEvidence) -> str:
    if evidence.gpt56_live_evidence_paths:
        return "Evidence found in " + ", ".join(evidence.gpt56_live_evidence_paths[:3])
    return "BLOCKED: run live GPT-5.6 review only after verified no-billing/free-credit boundary"


def _public_url_verification_section(packet: SubmissionPacket) -> str:
    if not packet.public_url_checks:
        return ""
    rows = "\n".join(
        f"- {check.status.upper()}: {check.expectation} {check.url} - {check.detail}"
        for check in packet.public_url_checks
    )
    return f"""
## Public URL Verification

{rows}
"""


def _devpost_flow_section(evidence: RepoEvidence) -> str:
    if not evidence.devpost_flow_paths:
        return ""
    paths = ", ".join(evidence.devpost_flow_paths[:3])
    return f"""
## Live Devpost State

- Event registration and draft-access evidence found in {paths}.
- Project draft creation/access: BLOCKED by Devpost reCAPTCHA after `Create
  project`; direct edit access is not stable until the entrant completes the
  visible CAPTCHA and the draft preview is checked.
"""


def _codex_credits_section(event: EventSnapshot) -> str:
    event_lines = (*event.required_materials, *event.account_requirements, *event.source_notes)
    credit_lines = [
        item
        for item in event_lines
        if "codex credits" in item.lower() or "api credits" in item.lower()
    ]
    if not credit_lines:
        return ""
    status = "Submitted; approval/code delivery pending."
    if not any("submitted" in item.lower() for item in credit_lines):
        status = "Not yet confirmed in the packet."
    api_boundary = "Do not treat this as OpenAI API credit proof."
    if not any("not api" in item.lower() or "api credits" in item.lower() for item in event_lines):
        api_boundary = "Verify whether the credit source applies before any billable path."
    return f"""
## Codex Credits State

- Request status: {status}
- Boundary: {api_boundary}
"""


def render_devpost_field_map(packet: SubmissionPacket) -> str:
    answers = packet.event.draft_answers
    title = answers.title or packet.event.name.removesuffix(" Packet")
    tagline = answers.short_description or (
        "SubmitOps Scout turns hackathon rules and repository evidence into a guarded "
        "submission command center."
    )
    what_it_does = answers.what_it_does or (
        "It scans event requirements and local project evidence, maps missing proof, "
        "generates readiness packets, and blocks unsupported final-submission claims."
    )
    why_it_can_win = answers.why_it_can_win or (
        "It solves a real builder problem at deadline time: truthful, complete, "
        "judge-ready submissions without losing the human approval boundary."
    )
    blockers = _bullets(packet.blockers)
    paste_status = "PASTE-READY" if not packet.blockers else "DRAFT - DO NOT FINAL SUBMIT"
    return f"""# OpenAI Build Week Devpost Field Map

Generated: {packet.generated_at}
Status: {paste_status}

## Source Snapshot

- Event: {packet.event.name}
- Event URL: {packet.event.event_url or "Unknown"}
- Deadline: {packet.event.deadline or "Unknown"}
- Captured at: {packet.event.captured_at}

## Core Fields

- Project title: {title}
- Category: {_pick_track(packet.event)}
- Short description: {tagline}
- Repository URL: {_repo_url(packet.evidence)}
- Demo video URL: {_video_url(packet.evidence)}
- /feedback Codex Session ID: {_feedback_value(packet.evidence)}
- Live GPT-5.6 review evidence: {_gpt56_live_value(packet.evidence)}
{_devpost_flow_section(packet.evidence)}
{_codex_credits_section(packet.event)}
{_public_url_verification_section(packet)}

## Project Description

{what_it_does}

## Codex and GPT-5.6 Usage

Codex was used to build the Python/uv CLI, source packet parser, repository
evidence scanner, readiness gate, tests, and generated submission artifacts.
The project includes a GPT-5.6 Responses API review payload generator so a
verified no-billing live review can check the final packet for unsupported
claims before Devpost submission. Current live evidence gate: {_gpt56_live_value(packet.evidence)}.

## Judge Testing Instructions

```bash
uv sync --all-groups
uv run submitops-scout fixtures/openai-build-week-packet.md . \\
  --out reports/openai-build-week-submitops-scout.md \\
  --json reports/openai-build-week-submitops-scout.json \\
  --devpost-map submission/openai-build-week-devpost-field-map.md \\
  --gpt56-payload reports/openai-build-week-gpt56-payload.json \\
  --gpt56-status
uv run pytest
uv run ruff check .
uv run ty check src tests
```

## Rubric Fit

- Technological implementation: non-trivial CLI, structured packets, tests,
  secret scan, and explicit go/downgrade/stop decisioning.
- Design: runnable developer-tool workflow with generated Markdown/JSON outputs.
- Potential impact: helps hackathon builders avoid missing proof, stale rules,
  and unsupported final-submission claims.
- Quality of idea: applies Codex to the real last-mile submission workflow that
  this hackathon itself requires.

## Why It Can Win

{why_it_can_win}

## Current Blockers

{blockers}
"""


def render_markdown(packet: SubmissionPacket) -> str:
    checks = "\n".join(
        f"- {check.status.upper()}: {check.name} - {check.detail or 'no detail'}"
        for check in packet.checks
    )
    secrets = "\n".join(
        f"- {finding.path}:{finding.line} {finding.label}"
        for finding in packet.evidence.secret_findings
    )
    return f"""# SubmitOps Scout Packet

Generated: {packet.generated_at}
Decision: {packet.decision.upper()}

## Event Snapshot

- Event: {packet.event.name}
- URL: {packet.event.event_url or "Unknown"}
- Deadline: {packet.event.deadline or "Unknown"}
- Captured at: {packet.event.captured_at}

## Tracks

{_bullets(packet.event.tracks)}

## Required Materials

{_bullets(packet.event.required_materials)}

## Account Requirements

{_bullets(packet.event.account_requirements)}

## Repository Evidence

- Root: {packet.evidence.root}
- Scanned text files: {packet.evidence.scanned_files}
- README: {", ".join(packet.evidence.readme_paths) or "missing"}
- License: {", ".join(packet.evidence.license_paths) or "missing"}
- Tests: {len(packet.evidence.test_files)}
- Sample data: {", ".join(packet.evidence.sample_data[:6]) or "missing"}
- Video URLs: {", ".join(packet.evidence.video_urls) or "missing"}
- Video assets: {", ".join(packet.evidence.video_assets) or "missing"}
- Devpost flow evidence: {", ".join(packet.evidence.devpost_flow_paths) or "missing"}
- Live GPT-5.6 evidence: {", ".join(packet.evidence.gpt56_live_evidence_paths) or "missing"}
- Public URLs found: {len(packet.evidence.public_urls)}
{_public_url_verification_section(packet)}

## Readiness Checks

{checks}

## Blockers

{_bullets(packet.blockers)}

## Secret Findings

{secrets or "- None"}
"""


def write_packet(packet: SubmissionPacket, markdown_path: Path, json_path: Path) -> None:
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_markdown(packet), encoding="utf-8")
    json_path.write_text(json.dumps(packet_to_dict(packet), indent=2), encoding="utf-8")


def write_devpost_field_map(packet: SubmissionPacket, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_devpost_field_map(packet), encoding="utf-8")
