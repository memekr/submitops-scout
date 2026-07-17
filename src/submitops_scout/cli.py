from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from submitops_scout.core import (
    assess_readiness,
    parse_event_packet,
    scan_repo_evidence,
    verify_public_urls,
    write_devpost_field_map,
    write_packet,
)
from submitops_scout.gpt56_adapter import connector_status, write_review_payload
from submitops_scout.static_demo import write_static_demo


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="submitops-scout",
        description="Generate a hackathon submission readiness packet.",
    )
    parser.add_argument("event_packet", type=Path, help="Markdown packet with event source facts.")
    parser.add_argument("repo", type=Path, help="Project repository to scan.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/submission-readiness.md"),
        help="Markdown output path.",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path("reports/submission-readiness.json"),
        help="JSON output path.",
    )
    parser.add_argument(
        "--gpt56-payload",
        type=Path,
        help="Optional Responses API payload for GPT-5.6 review.",
    )
    parser.add_argument(
        "--devpost-map",
        type=Path,
        help="Optional Devpost field-map Markdown output path.",
    )
    parser.add_argument(
        "--static-demo",
        type=Path,
        help="Optional static HTML demo dashboard output path.",
    )
    parser.add_argument(
        "--gpt56-status",
        action="store_true",
        help="Print GPT-5.6 connector status without making a network request.",
    )
    parser.add_argument(
        "--verify-public-urls",
        action="store_true",
        help="Verify discovered repository and demo video URLs with HTTP checks.",
    )
    parser.add_argument(
        "--require-public-url",
        action="append",
        default=[],
        help="Additional public URL that must return an HTTP 2xx/3xx status.",
    )
    parser.add_argument(
        "--forbid-public-url",
        action="append",
        default=[],
        help="Sensitive URL that must return HTTP 404 or 410, such as a raw .env path.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    packet = assess_readiness(parse_event_packet(args.event_packet), scan_repo_evidence(args.repo))
    if args.verify_public_urls:
        packet = verify_public_urls(
            packet,
            required_urls=tuple(args.require_public_url),
            absent_urls=tuple(args.forbid_public_url),
        )
    write_packet(packet, args.out, args.json)
    if args.devpost_map:
        write_devpost_field_map(packet, args.devpost_map)
    if args.static_demo:
        write_static_demo(packet, args.static_demo)
    if args.gpt56_payload:
        write_review_payload(packet, args.gpt56_payload)
    if args.gpt56_status:
        print(connector_status())
    print(
        "SubmitOps Scout complete: "
        f"decision={packet.decision}, blockers={len(packet.blockers)}, report={args.out}"
    )


if __name__ == "__main__":
    main()
