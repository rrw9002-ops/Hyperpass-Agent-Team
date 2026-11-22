from __future__ import annotations
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from verify import candidate_files, release_path, sha, verify
from build_release import build


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "package"
        self.root.mkdir()
        manifest = json.loads((ROOT / "bundle-manifest.json").read_text(encoding="utf-8"))
        for name in [*manifest["files"], "bundle-manifest.json"]:
            out = self.root / name
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, out)

    def tearDown(self):
        self.temp.cleanup()

    def test_clean_package_and_nested_relocation(self):
        self.assertEqual(verify(self.root), [])
        nested = Path(self.temp.name) / "한글 공백 폴더" / "package"
        nested.parent.mkdir()
        shutil.copytree(self.root, nested)
        self.assertEqual(verify(nested), [])

    def test_private_records_never_packaged(self):
        sentinel = uuid.uuid4().hex
        for name in ("trading/runs/private.md", "context/investor-context.md", "wikis/personal.md",
                     "investment-brains/private.md", "strategies/private.md", ".env", "private.sqlite3"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(sentinel, encoding="utf-8")
        archive = build(self.root)
        with zipfile.ZipFile(archive) as z:
            self.assertTrue(all(sentinel.encode() not in z.read(name) for name in z.namelist()))
            self.assertIn("Hyperpass-Agent-Team/.codex/agents/risk-manager.toml", z.namelist())

    def test_tampered_profile_blocks_release(self):
        path = self.root / ".codex/agents/risk-manager.toml"
        path.write_text(path.read_text() + '\nmodel = "unauthorized"\n')
        self.assertTrue(verify(self.root))
        with self.assertRaises(ValueError):
            build(self.root)

    def test_unlisted_hook_or_skill_blocks_release(self):
        (self.root / ".codex/hooks.json").write_text('{}')
        self.assertTrue(any("unlisted" in e for e in verify(self.root)))

    def test_manifest_cannot_smuggle_private_file_or_traversal(self):
        for name in ("../secret.txt", "C:/secret.txt", "trading/private.md", ".env", "docs/../secret.txt", "docs\\secret.txt"):
            self.assertFalse(release_path(name), name)
        manifest = json.loads((self.root / "bundle-manifest.json").read_text())
        path = self.root / "context/private.md"
        path.write_text("private")
        manifest["files"]["context/private.md"] = sha(path)
        (self.root / "bundle-manifest.json").write_text(json.dumps(manifest))
        self.assertTrue(any("not a release path" in e for e in verify(self.root)))

    def test_removed_independent_role_fails(self):
        (self.root / ".codex/agents/judgment-reviewer.toml").unlink()
        self.assertTrue(verify(self.root))

    def test_rehashing_cannot_hide_upstream_change(self):
        manifest = json.loads((self.root / "bundle-manifest.json").read_text())
        name = "provenance/upstream/workflow.txt"
        (self.root / name).write_text("altered")
        manifest["files"][name] = sha(self.root / name)
        (self.root / "bundle-manifest.json").write_text(json.dumps(manifest))
        self.assertTrue(any("snapshot changed" in e for e in verify(self.root)))

    def test_archive_reproducible_and_extracts_as_valid_package(self):
        a = build(self.root, Path(self.temp.name) / "a").read_bytes()
        b_path = build(self.root, Path(self.temp.name) / "b")
        self.assertEqual(a, b_path.read_bytes())
        extraction = Path(self.temp.name) / "extract"
        with zipfile.ZipFile(b_path) as z:
            z.extractall(extraction)
        self.assertEqual(verify(extraction / "Hyperpass-Agent-Team"), [])


if __name__ == "__main__":
    unittest.main()
