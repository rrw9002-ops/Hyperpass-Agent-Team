"""Maintainer-only: refresh distribution hashes after reviewing the file list."""
from __future__ import annotations
import json
from verify import ROOT, candidate_files, safe_file, sha

if __name__ == "__main__":
    files = {name: sha(safe_file(ROOT, name)) for name in candidate_files(ROOT)}
    data = {"version": (ROOT / "VERSION").read_text().strip(), "files": files,
            "meaning": "Distribution integrity only; not a signature, financial validation, or host readiness proof."}
    (ROOT / "bundle-manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded {len(files)} distribution files. Review manifest changes before publishing.")
