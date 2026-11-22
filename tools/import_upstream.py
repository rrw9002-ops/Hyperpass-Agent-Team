"""Maintainer-only import of pinned, Apache-2.0 research methods.

No networking, package installation or execution of upstream code. Student use
does not invoke this script. Every imported source and adapted file is hashed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "a15871c922870f9803f819d9b994888ec81eabc1"
REPOSITORY = "https://github.com/moneybuilderjay-cmyk/Hyperpass-Tradingagent"
ROLES = {
    "fundamental-analyst": "fundamental",
    "technical-analyst": "technical",
    "news-analyst": "news",
    "macro-analyst": "macro",
    "instrument-analyst": "instrument",
    "valuation-analyst": "valuation",
    "portfolio-manager": "portfolio",
    "risk-manager": "risk",
    "judgment-reviewer": "judgment",
}
REFS = ROOT / ".agents/skills/hyperpass-team/references"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def import_sources(source: Path) -> None:
    # Verify the claimed pin, not merely the hash of arbitrary local inputs.
    import os
    env = dict(os.environ)
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    revision = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"],
                              env=env, check=True, capture_output=True, text=True).stdout.strip()
    if revision != COMMIT:
        raise ValueError(f"source revision is not pinned commit {COMMIT}")
    manifests = []

    def capture(relative: str, key: str) -> str:
        raw = (source / relative).read_bytes()
        pinned = subprocess.run(["git", "-C", str(source), "show", f"{COMMIT}:{relative}"],
                                env=env, check=True, capture_output=True).stdout
        if raw.replace(b"\r\n", b"\n") != pinned.replace(b"\r\n", b"\n"):
            raise ValueError(f"source differs from pinned commit: {relative}")
        snapshot = ROOT / "provenance/upstream" / f"{key}.txt"
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(raw)
        manifests.append({"source": relative, "snapshot": snapshot.relative_to(ROOT).as_posix(),
                          "sha256": digest(raw), "source_url": f"{REPOSITORY}/blob/{COMMIT}/{relative}"})
        return raw.decode("utf-8-sig").replace("\r\n", "\n")

    base = "workspace_templates/modules/repo-skills/files"
    for role, method in ROLES.items():
        role_source = f"workspace_templates/modules/fixed-subagents/files/.codex/agents/{role}.toml"
        config = capture(role_source, role)
        description = re.search(r'^description = "(.*)"$', config, re.M).group(1)
        skill_source = f"{base}/.tradingcodex/subagents/skills/{role}/tcx-{method}/SKILL.md"
        original = capture(skill_source, f"method-{role}")
        body = original.split("---", 2)[2].lstrip()
        # Only storage/transport/execution surfaces change. Domain method remains.
        body = re.sub(r"Codex-native state access:\n.*?(?=Universe method:)",
                      "Research-edition state access:\n\n- Use only user-supplied, dated holdings or portfolio files. Do not query or sync broker accounts. Missing or stale portfolio inputs limit the dependent conclusions.\n\n", body, flags=re.S)
        body = body.replace("authenticated", "reviewed file-native")
        body = body.replace("Authenticated", "Reviewed file-native")
        body = body.replace("with their service receipts/content\n  hashes and handoff states; retrieve artifacts by exact ID", "with exact file versions, observed child attribution and handoff states; read those versions by exact path")
        body = body.replace("reviewed file-native IDs, receipts/hashes", "exact accepted file versions and observed child attribution")
        body = body.replace("object required by the artifact tool", "object in the report metadata")
        body = body.replace("installed skills, data, policy, and adapter boundaries",
                            "available research methods and data")
        body = re.sub(r"Write outputs under `trading/reports/[^`]+/`\.",
                      "Write the assigned versioned role report in the current run, following `../records.md`.", body)
        note = ("> Research-edition adaptation: source method preserved; service identities and\n"
                "> persistence are mapped to reviewed file records. This is not authenticated\n"
                "> provenance. Any draft/approval readiness below describes analysis only; no\n"
                "> order draft, approval, account access or execution is available. Final action\n"
                "> readiness always remains `research-only`. Read `../child-contract.md`.\n\n")
        target = REFS / "methods" / f"{role}.md"
        if role in {"risk-manager", "portfolio-manager", "instrument-analyst"}:
            note += ("> Absent execution infrastructure limits action readiness only. Do not block\n"
                     "> supported research merely because this edition has no broker adapter or\n"
                     "> approval service. Preserve instrument-specific research/data gaps separately.\n\n")
        write(target, note + body)
        manifests[-1]["adapted"] = target.relative_to(ROOT).as_posix()
        manifests[-1]["adapted_sha256"] = digest(target.read_bytes())
        instructions = (
            f"You are the exact {role} specialist in the Hyperpass research team.\n"
            "Read .agents/skills/hyperpass-team/references/child-contract.md and\n"
            f".agents/skills/hyperpass-team/references/methods/{role}.md before substantive work.\n"
            "Stay within your parent's bounded brief. Use the assigned run and output path.\n"
            "Return actual evidence and a saved versioned report; never fabricate execution.\n"
            "This edition has no TradingCodex service or broker authority. Never call account,\n"
            "order, approval or credential tools. Do not change configuration or role rules.\n"
        )
        if role == "judgment-reviewer":
            instructions += ("Independently adjudicate accepted inputs under the same mandate. Do not\n"
                             "collect replacement primary research, browse for a new thesis, size a position\n"
                             "or change the user's frame. Name the evidence owner for required revisions.\n")
        if role == "risk-manager":
            instructions += "Your independent risk judgment is not a service approval or permission to trade.\n"
        write(ROOT / ".codex/agents" / f"{role}.toml",
              f'name = "{role}"\ndescription = {json.dumps(description)}\n\ndeveloper_instructions = """\n{instructions}"""\n')

    for name in ("data-qc", "scenarios", "forecast", "anti-overfit"):
        original = capture(f"{base}/.tradingcodex/subagents/skills/shared/tcx-{name}/SKILL.md", f"shared-{name}")
        target = REFS / f"{name}.md"
        body = original.split("---", 2)[2].lstrip()
        if name == "forecast":
            body = body.replace("Write scoreable records under `trading/forecasts/` only after accepted\nevidence supports the forecast.",
                                "Children propose forecasts only within their assigned run-local report.\nHead Manager may promote a scoreable record under `trading/forecasts/` only\nafter accepted evidence supports it, preserving its upstream version and source IDs.")
        write(target, body)
        manifests[-1].update(adapted=target.relative_to(ROOT).as_posix(), adapted_sha256=digest(target.read_bytes()))
    framing = capture(f"{base}/.agents/skills/tcx-workflow/playbooks/research-framing.md", "research-framing")
    write(REFS / "research-framing.md", framing)
    for path, name in (
        (f"{base}/.agents/skills/tcx-workflow/SKILL.md", "workflow"),
        (f"{base}/.agents/skills/tcx-workflow/playbooks/context-overlays.md", "context-overlays"),
        (f"{base}/.tradingcodex/subagents/skills/shared/tcx-source-gate/SKILL.md", "source-gate"),
        ("workspace_templates/modules/codex-base/files/.codex/prompts/base_instructions/head-manager.md", "head-manager"),
        ("workspace_templates/modules/codex-base/files/.codex/prompts/base_instructions/fixed-role.md", "fixed-role"),
    ):
        capture(path, name)
    shutil.copyfile(source / "LICENSE", ROOT / "LICENSE")
    capture("NOTICE", "NOTICE")
    write(ROOT / "provenance/upstream-manifest.json", json.dumps({
        "repository": REPOSITORY, "commit": COMMIT, "upstream_version": "2.1.3",
        "edition": "research-only", "files": manifests,
        "adaptations": ["File-native research replaces service persistence; no authentication-equivalence claim.",
                        "No broker/account/order/approval operations in this edition.",
                        "Current supported native custom-agent schema; parent model/permissions/MCP inherited.",
                        "Role-specific analytic method text preserved except explicit transport/storage wording."]
    }, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    import_sources(args.source.resolve())
