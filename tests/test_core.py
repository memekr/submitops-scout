from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from submitops_scout import core
from submitops_scout.core import (
    assess_readiness,
    parse_event_packet,
    render_devpost_field_map,
    scan_repo_evidence,
    verify_public_urls,
)
from submitops_scout.gpt56_adapter import Gpt56ReviewConfig, build_review_payload, connector_status

if TYPE_CHECKING:
    import pytest


def _write_project(root: Path) -> None:
    (root / "src" / "sample").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "reports").mkdir()
    (root / "README.md").write_text(
        """# Demo

## Usage

Run this project with Codex-built setup instructions.
It integrates GPT-5.6 through a Responses API review payload.
Live GPT-5.6 review evidence status: complete; response id resp_123456789abc.
Primary /feedback Session ID: sess_123456789abc.
Demo: https://youtu.be/example
Repository: https://github.com/memekr/demo
Mirror: `https://github.com/memekr/demo-mirror`
OEmbed: 'https://www.youtube.com/oembed?url=https://youtu.be/example&format=json'
Colon suffix: https://youtu.be/example:
""",
        encoding="utf-8",
    )
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (root / "src" / "sample" / "__init__.py").write_text("", encoding="utf-8")
    (root / "tests" / "test_sample.py").write_text(
        "def test_ok():\n    assert True\n",
        encoding="utf-8",
    )
    (root / "reports" / "sample.json").write_text('{"ok": true}\n', encoding="utf-8")


def test_parse_event_packet_extracts_openai_build_week_facts(tmp_path: Path) -> None:
    packet = tmp_path / "openai.md"
    packet.write_text(
        """# OpenAI Build Week Packet

Event URL: https://openai.devpost.com/

- Public deadline: July 21, 2026, 5:00 PM PT.
- Official Rules are posted and reviewed.
- Participants: about 12,000.

Required:
- A working project built with Codex and GPT-5.6.
- A demo video.
- A code repository.
- /feedback Codex Session ID.
- Developer Tools

Title: `SubmitOps Scout: Codex-Powered Submission Command Center`

Short description:

> SubmitOps Scout helps builders turn hackathon rules and repo evidence into a ready packet.
""",
        encoding="utf-8",
    )

    snapshot = parse_event_packet(packet)

    assert snapshot.event_url == "https://openai.devpost.com/"
    assert "July 21" in snapshot.deadline
    assert "Developer Tools" in snapshot.tracks
    assert snapshot.draft_answers.title == (
        "SubmitOps Scout: Codex-Powered Submission Command Center"
    )
    assert "ready packet" in snapshot.draft_answers.short_description
    assert any("feedback" in item.lower() for item in snapshot.required_materials)


def test_repo_evidence_scan_and_readiness_go(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "src" / "placeholder.py").write_text(
        """
YOUTUBE_OEMBED = "https://www.youtube.com/oembed?url={encoded_url}&format=json"
VIMEO_OEMBED = "https://vimeo.com/api/oembed.json?url="
""",
        encoding="utf-8",
    )
    (tmp_path / "submission").mkdir()
    (tmp_path / "submission" / "openai-devpost-field-map.md").write_text(
        "Generated output with stale URL https://youtu.be/example:\n",
        encoding="utf-8",
    )
    event = tmp_path / "event.md"
    event.write_text(
        """# OpenAI Build Week Packet
- Public deadline: July 21, 2026, 5:00 PM PT.
- Official Rules are posted and reviewed.
- A working project built with Codex and GPT-5.6.
- A public YouTube demo video.
- A code repository with README.
- /feedback Codex Session ID.
""",
        encoding="utf-8",
    )

    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))

    assert packet.decision == "go"
    assert not packet.blockers
    assert "https://github.com/memekr/demo-mirror" in packet.evidence.public_urls
    assert "https://github.com/memekr/demo-mirror`" not in packet.evidence.public_urls
    assert "https://www.youtube.com/oembed?url=https://youtu.be/example&format=json" in (
        packet.evidence.public_urls
    )
    assert "https://www.youtube.com/oembed?url=https://youtu.be/example&format=json'" not in (
        packet.evidence.public_urls
    )
    assert "https://www.youtube.com/oembed?url={encoded_url}&format=json" not in (
        packet.evidence.public_urls
    )
    assert "https://vimeo.com/api/oembed.json?url=" not in packet.evidence.public_urls
    assert "https://youtu.be/example:" not in packet.evidence.public_urls


def test_public_url_verification_records_reachable_and_absent_urls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_project(tmp_path)
    event = tmp_path / "event.md"
    event.write_text(
        """# OpenAI Build Week Packet
- Public deadline: July 21, 2026, 5:00 PM PT.
- Official Rules are posted and reviewed.
- A working project built with Codex and GPT-5.6.
- A public YouTube demo video.
- A code repository with README.
- /feedback Codex Session ID.
""",
        encoding="utf-8",
    )
    seen: list[str] = []

    def fake_fetch_status(url: str, timeout_seconds: float) -> tuple[int | None, str]:
        del timeout_seconds
        seen.append(url)
        if url.endswith("/.env"):
            return 404, "HTTP 404"
        return 200, "HTTP 200"

    monkeypatch.setattr(core, "_fetch_status", fake_fetch_status)

    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))
    verified = verify_public_urls(
        packet,
        required_urls=("https://raw.githubusercontent.com/memekr/demo/main/README.md",),
        absent_urls=("https://raw.githubusercontent.com/memekr/demo/main/.env",),
    )

    assert verified.decision == "go"
    assert verified.public_url_checks
    assert all(check.status == "pass" for check in verified.public_url_checks)
    assert "https://github.com/memekr/demo" in seen
    assert "https://www.youtube.com/oembed?url=https://youtu.be/example&format=json" in seen


def test_forbidden_public_url_forces_stop(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_project(tmp_path)
    event = tmp_path / "event.md"
    event.write_text(
        """# OpenAI Build Week Packet
- Public deadline: July 21, 2026, 5:00 PM PT.
- Official Rules are posted and reviewed.
- A working project built with Codex and GPT-5.6.
- A public YouTube demo video.
- A code repository with README.
- /feedback Codex Session ID.
""",
        encoding="utf-8",
    )

    def fake_fetch_status(url: str, timeout_seconds: float) -> tuple[int | None, str]:
        del url, timeout_seconds
        return 200, "HTTP 200"

    monkeypatch.setattr(core, "_fetch_status", fake_fetch_status)

    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))
    verified = verify_public_urls(
        packet,
        absent_urls=("https://raw.githubusercontent.com/memekr/demo/main/.env",),
    )

    assert verified.decision == "stop"
    assert any(
        blocker == "public URL absent: https://raw.githubusercontent.com/memekr/demo/main/.env"
        for blocker in verified.blockers
    )


def test_readiness_downgrades_when_external_video_and_feedback_are_missing(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "README.md").write_text(
        "# Demo\n\nUsage with Codex and GPT-5.6, but no public video yet.\n",
        encoding="utf-8",
    )
    event = tmp_path / "event.md"
    event.write_text("# OpenAI Build Week Packet\n- Official Rules are posted.\n", encoding="utf-8")

    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))

    assert packet.decision == "downgrade"
    assert "live GPT-5.6 review evidence present" in packet.blockers
    assert "/feedback Session ID present" in packet.blockers
    assert "public demo video present" in packet.blockers


def test_blocker_language_does_not_count_as_live_gpt56_evidence(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "README.md").write_text(
        """# Demo

Usage with Codex and GPT-5.6.
Do not submit until /feedback evidence and the live GPT-5.6/no-billing boundary are complete.
No live GPT-5.6 review call has been run with verified free credits.
""",
        encoding="utf-8",
    )
    event = tmp_path / "event.md"
    event.write_text("# OpenAI Build Week Packet\n- Official Rules are posted.\n", encoding="utf-8")

    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))

    assert not packet.evidence.gpt56_live_evidence_paths
    assert "live GPT-5.6 review evidence present" in packet.blockers


def test_devpost_field_map_uses_draft_answers_and_blockers(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "README.md").write_text(
        "# Demo\n\nUsage with Codex and GPT-5.6, but no public video yet.\n",
        encoding="utf-8",
    )
    event = tmp_path / "event.md"
    event.write_text(
        """# OpenAI Build Week Packet
- Public deadline: July 21, 2026, 5:00 PM PT.
- Official Rules are posted.
- Developer Tools

Title: `SubmitOps Scout: Codex-Powered Submission Command Center`

Short description:

> Guarded Devpost readiness for Codex-built projects.

What it does:

> It maps hackathon rules to repository proof and exact blockers.
""",
        encoding="utf-8",
    )
    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))

    field_map = render_devpost_field_map(packet)

    assert "Status: DRAFT - DO NOT FINAL SUBMIT" in field_map
    assert "Project title: SubmitOps Scout: Codex-Powered Submission Command Center" in field_map
    assert "Category: Developer Tools" in field_map
    assert "BLOCKED: public YouTube demo URL not recorded yet" in field_map
    assert "BLOCKED: run live GPT-5.6 review" in field_map
    assert "/feedback Session ID present" in field_map


def test_secret_finding_forces_stop(tmp_path: Path) -> None:
    _write_project(tmp_path)
    (tmp_path / "README.md").write_text(
        "Usage with Codex, GPT-5.6, /feedback, https://youtu.be/example\n",
        encoding="utf-8",
    )
    fake_key = "sk-" + "abcdefghijklmnopqrstuvwxyz"
    (tmp_path / "leak.md").write_text(
        f"OPENAI_API_KEY={fake_key}\n",
        encoding="utf-8",
    )
    event = tmp_path / "event.md"
    event.write_text("# OpenAI Build Week Packet\n- Official Rules are posted.\n", encoding="utf-8")

    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))

    assert packet.decision == "stop"
    assert packet.evidence.secret_findings[0].path == "leak.md"


def test_gpt56_review_payload_is_json_object_request(tmp_path: Path) -> None:
    _write_project(tmp_path)
    event = tmp_path / "event.md"
    event.write_text("# OpenAI Build Week Packet\n- Official Rules are posted.\n", encoding="utf-8")
    packet = assess_readiness(parse_event_packet(event), scan_repo_evidence(tmp_path))

    payload = build_review_payload(packet, Gpt56ReviewConfig(model="gpt-5.6-terra"))

    assert payload["model"] == "gpt-5.6-terra"
    assert payload["text"] == {"format": {"type": "json_object"}}
    assert "PACKET_JSON" in json.dumps(payload)


def test_gpt56_connector_status_does_not_expose_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-" + "secret-value-that-should-not-print")

    status = connector_status()

    assert "configured" in status
    assert "sk-secret" not in status
