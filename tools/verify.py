"""Verify the distribution, not student financial conclusions or host readiness."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ROLES = {"fundamental-analyst", "technical-analyst", "news-analyst", "macro-analyst",
         "instrument-analyst", "valuation-analyst", "portfolio-manager", "risk-manager",
         "judgment-reviewer"}
TOP_FILES = {"AGENTS.md", "README.md", "START-HERE.md", "LICENSE", "NOTICE", "VERSION", ".gitignore"}
DIRECTORIES = {".codex", ".agents", "docs", "prompts", "examples", "provenance", "tools", "tests", ".github"}
PRIVATE_READMES = {"trading/README.md", "context/README.md"}


def release_path(name: str) -> bool:
    """Positive allowlist; never package runtime/private records or path aliases."""
    p = PurePosixPath(name)
    if "\\" in name or p.is_absolute() or str(p) != name or any(x in {"..", "."} for x in p.parts):
        return False
    if not p.parts or any(x in {"__pycache__", ".git", "node_modules"} for x in p.parts):
        return False
    if p.name.startswith(".env") or p.suffix in {".pyc", ".log", ".sqlite3", ".db"}:
        return False
    return name in TOP_FILES | PRIVATE_READMES or p.parts[0] in DIRECTORIES


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_file(root: Path, name: str) -> Path:
    if not release_path(name):
        raise ValueError(f"not a release path: {name}")
    path = root / name
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root.parent):
        raise ValueError(f"symlink not accepted: {name}")
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"missing or escaped file: {name}")
    return path


def candidate_files(root: Path) -> list[str]:
    # Enumerate only owned distribution trees, never students' data directories.
    found = []
    for name in sorted(TOP_FILES | PRIVATE_READMES):
        if (root / name).is_file():
            found.append(name)
    for name in sorted(DIRECTORIES):
        folder = root / name
        if folder.exists():
            for path in folder.rglob("*"):
                rel = path.relative_to(root).as_posix()
                if path.is_file() and release_path(rel):
                    found.append(rel)
    return sorted(found)


def verify(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads((root / "bundle-manifest.json").read_text(encoding="utf-8"))
        files = manifest["files"]
        if not isinstance(files, dict) or not files:
            raise ValueError("manifest files must be a nonempty mapping")
        if manifest["version"] != (root / "VERSION").read_text().strip():
            errors.append("manifest/package version mismatch")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-z0-9.]+)?", manifest["version"]):
            errors.append("unsafe or invalid version")
        for name, expected in files.items():
            try:
                if sha(safe_file(root, name)) != expected:
                    errors.append(f"hash mismatch: {name}")
            except (ValueError, OSError) as exc:
                errors.append(str(exc))
        extra = set(candidate_files(root)) - set(files)
        errors.extend(f"unlisted distribution file: {name}" for name in sorted(extra))
    except (KeyError, ValueError, OSError) as exc:
        return [f"invalid manifest: {exc}"]

    try:
        project = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
        if project != {"agents": {"enabled": True}}:
            errors.append("project config must only enable native agents; no MCP/permissions/model overrides")
        configs = list((root / ".codex/agents").glob("*.toml"))
        if {p.stem for p in configs} != ROLES:
            errors.append("nine-role profile set differs")
        for path in configs:
            role = tomllib.loads(path.read_text(encoding="utf-8"))
            if set(role) != {"name", "description", "developer_instructions"} or role["name"] != path.stem:
                errors.append(f"unsupported/misidentified role configuration: {path.name}")
            method = root / ".agents/skills/hyperpass-team/references/methods" / f"{path.stem}.md"
            if not method.is_file():
                errors.append(f"missing method: {path.stem}")
        skill = (root / ".agents/skills/hyperpass-team/SKILL.md").read_text(encoding="utf-8")
        if not skill.startswith("---\nname: hyperpass-team\ndescription: "):
            errors.append("invalid skill metadata")
        for source in root.glob(".agents/skills/hyperpass-team/**/*.md"):
            text = source.read_text(encoding="utf-8")
            for rel in re.findall(r"`((?:references/|methods/|\.\./)[\w./-]+\.md)`", text):
                if not (source.parent / rel).resolve().is_file():
                    errors.append(f"broken skill reference: {source.relative_to(root)} -> {rel}")
        upstream = json.loads((root / "provenance/upstream-manifest.json").read_text(encoding="utf-8"))
        for item in upstream["files"]:
            if sha(safe_file(root, item["snapshot"])) != item["sha256"]:
                errors.append(f"upstream snapshot changed: {item['snapshot']}")
            if "adapted" in item and sha(safe_file(root, item["adapted"])) != item["adapted_sha256"]:
                errors.append(f"adapted method changed without reviewed provenance: {item['adapted']}")
    except (ValueError, KeyError, OSError) as exc:
        errors.append(f"configuration/provenance error: {exc}")
    return errors


if __name__ == "__main__":
    problems = verify()
    print(json.dumps({"structural_validation": "fail" if problems else "pass", "errors": problems,
                      "native_role_execution": "not_tested_by_this_command", "broker_execution": "not_provided"}, indent=2))
    sys.exit(bool(problems))
