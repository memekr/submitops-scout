from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from submitops_scout.core import (
    assess_readiness,
    parse_event_packet,
    scan_repo_evidence,
    write_devpost_field_map,
    write_packet,
)
from submitops_scout.gpt56_adapter import connector_status, write_review_payload


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
        "--gpt56-status",
        action="store_true",
        help="Print GPT-5.6 connector status without making a network request.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    packet = assess_readiness(parse_event_packet(args.event_packet), scan_repo_evidence(args.repo))
    write_packet(packet, args.out, args.json)
    if args.devpost_map:
        write_devpost_field_map(packet, args.devpost_map)
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
