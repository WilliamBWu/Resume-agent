from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_master import validate_master  # noqa: E402


def test_missing_profile_reports_error(tmp_path: Path):
    master = tmp_path / "data" / "master"
    master.mkdir(parents=True)
    (master / "experience.md").write_text(
        "---\nschema_version: 1\nupdated: 2026-09-14\n---\n\n# x\n",
        encoding="utf-8",
    )
    (master / "projects.md").write_text(
        "---\nschema_version: 1\nupdated: 2026-09-14\n---\n\n# x\n",
        encoding="utf-8",
    )
    (master / "CHANGELOG.md").write_text("# Master CHANGELOG\n", encoding="utf-8")
    errors = validate_master(tmp_path)
    assert any("profile.md" in e for e in errors)


def test_valid_minimal_master_passes(tmp_path: Path):
    master = tmp_path / "data" / "master"
    master.mkdir(parents=True)
    for name in ("profile.md", "experience.md", "projects.md"):
        (master / name).write_text(
            "---\nschema_version: 1\nupdated: 2026-09-14\n---\n\n# Title\n",
            encoding="utf-8",
        )
    (master / "CHANGELOG.md").write_text("# Master CHANGELOG\n", encoding="utf-8")
    assert validate_master(tmp_path) == []


def test_entry_missing_id_fails(tmp_path: Path):
    master = tmp_path / "data" / "master"
    master.mkdir(parents=True)
    for name in ("profile.md", "projects.md"):
        (master / name).write_text(
            "---\nschema_version: 1\nupdated: 2026-09-14\n---\n\n# Title\n",
            encoding="utf-8",
        )
    (master / "CHANGELOG.md").write_text("# c\n", encoding="utf-8")
    (master / "experience.md").write_text(
        "---\nschema_version: 1\nupdated: 2026-09-14\n---\n\n"
        "# 工作与实习经历\n\n## Bad Entry\n\n"
        "```yaml\ntype: work\ntitle: 工程师\ncompany: X\nperiod: 2024~2025\n```\n\n"
        "- did stuff\n",
        encoding="utf-8",
    )
    errors = validate_master(tmp_path)
    assert any("id" in e.lower() for e in errors)
