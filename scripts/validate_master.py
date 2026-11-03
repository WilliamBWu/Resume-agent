#!/usr/bin/env python3
"""Validate resume agent master files exist and experience/project entries have required YAML fields."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "data/master/profile.md",
    "data/master/experience.md",
    "data/master/projects.md",
    "data/master/CHANGELOG.md",
)

ENTRY_FILES = (
    "data/master/experience.md",
    "data/master/projects.md",
)

YAML_FENCE = re.compile(r"```yaml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
REQUIRED_ENTRY_KEYS = ("id", "type", "period")


def validate_master(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required file: {rel}")

    for rel in ENTRY_FILES:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        fences = YAML_FENCE.findall(text)
        headings = re.findall(r"^## .+$", text, re.MULTILINE)
        if not headings:
            continue
        if not fences:
            errors.append(f"{rel}: found ## headings but no ```yaml entry blocks")
            continue
        for i, body in enumerate(fences, start=1):
            keys = {
                line.split(":", 1)[0].strip()
                for line in body.splitlines()
                if line.strip() and not line.strip().startswith("#") and ":" in line
            }
            missing = [k for k in REQUIRED_ENTRY_KEYS if k not in keys]
            if missing:
                errors.append(
                    f"{rel}: yaml block #{i} missing keys: {', '.join(missing)}"
                )
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_master(root)
    if errors:
        print("INVALID master:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: master structure valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
