"""Build a distribution exclusively from the verified positive manifest."""
from __future__ import annotations
import hashlib
import json
import zipfile
from pathlib import Path
from verify import ROOT, safe_file, verify


def build(root: Path = ROOT, destination: Path | None = None) -> Path:
    errors = verify(root)
    if errors:
        raise ValueError("Refusing to package invalid distribution: " + "; ".join(errors))
    manifest = json.loads((root / "bundle-manifest.json").read_text(encoding="utf-8"))
    destination = destination or root / "dist"
    destination.mkdir(parents=True, exist_ok=True)
    version = manifest["version"]
    target = destination / f"Hyperpass-Agent-Team-{version}.zip"
    prefix = "Hyperpass-Agent-Team/"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(manifest["files"]):
            info = zipfile.ZipInfo(prefix + name, date_time=(2026, 11, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, safe_file(root, name).read_bytes())
        info = zipfile.ZipInfo(prefix + "bundle-manifest.json", date_time=(2026, 11, 22, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, (root / "bundle-manifest.json").read_bytes())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix(".zip.sha256").write_text(f"{digest}  {target.name}\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    print(build())
