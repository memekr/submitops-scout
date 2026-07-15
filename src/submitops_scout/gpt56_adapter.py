from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from submitops_scout.core import SubmissionPacket, packet_to_dict


@dataclass(frozen=True)
class Gpt56ReviewConfig:
    model: str = "gpt-5.6"
    api_key_env: str = "OPENAI_API_KEY"
    reasoning_effort: str = "low"


def connector_status(config: Gpt56ReviewConfig | None = None) -> str:
    resolved = config or Gpt56ReviewConfig()
    if os.environ.get(resolved.api_key_env):
        return f"configured for {resolved.model} via {resolved.api_key_env}"
    return f"not configured; set {resolved.api_key_env} to run live {resolved.model} review"


def build_review_payload(
    packet: SubmissionPacket,
    config: Gpt56ReviewConfig | None = None,
) -> dict[str, Any]:
    resolved = config or Gpt56ReviewConfig()
    evidence = packet_to_dict(packet)
    prompt = (
        "Review this hackathon submission packet. Use only the supplied JSON. "
        "Return JSON with keys decision, strongest_evidence, missing_evidence, "
        "unsupported_claims, and next_action. Do not invent external facts."
    )
    return {
        "model": resolved.model,
        "reasoning": {"effort": resolved.reasoning_effort},
        "input": [
            {"role": "system", "content": "You are a precise submission readiness reviewer."},
            {
                "role": "user",
                "content": f"{prompt}\n\nPACKET_JSON:\n{json.dumps(evidence, sort_keys=True)}",
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }


def write_review_payload(packet: SubmissionPacket, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(build_review_payload(packet), indent=2), encoding="utf-8")
