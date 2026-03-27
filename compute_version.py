#!/usr/bin/env python3
"""Compute and optionally update the project version.

Usage:
    python compute_version.py [--ci] [--update]

Options:
    --ci      Read bump type from CHANGELOG.md <!-- bump: TYPE --> comment
    --update  Write the new version to VERSION file and update CHANGELOG.md
"""

import argparse
import re
import sys
from pathlib import Path


def read_version(version_file: Path) -> str:
    """Read the current version from VERSION file."""
    if not version_file.exists():
        return "0.0.0"
    return version_file.read_text().strip()


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse a semver string into (major, minor, patch)."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(version: str, bump_type: str) -> str:
    """Bump the version according to bump_type (major, minor, patch)."""
    major, minor, patch = parse_version(version)
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def get_bump_type_from_changelog(changelog_file: Path) -> str | None:
    """Extract bump type from <!-- bump: TYPE --> comment in CHANGELOG.md."""
    if not changelog_file.exists():
        return None
    content = changelog_file.read_text()
    match = re.search(r"<!--\s*bump:\s*(\w+)\s*-->", content)
    if match:
        return match.group(1).lower()
    return None


def has_unreleased_section(changelog_file: Path) -> bool:
    """Check if CHANGELOG.md has an ## Unreleased section."""
    if not changelog_file.exists():
        return False
    content = changelog_file.read_text()
    return bool(re.search(r"^##\s+Unreleased", content, re.MULTILINE))


def update_changelog_for_release(changelog_file: Path, new_version: str) -> None:
    """Replace ## Unreleased with ## vX.Y.Z and remove bump comment."""
    content = changelog_file.read_text()
    # Remove the bump comment
    content = re.sub(r"<!--\s*bump:\s*\w+\s*-->\n?", "", content)
    # Replace Unreleased with version
    content = re.sub(r"^(##\s+)Unreleased", rf"\1v{new_version}", content, flags=re.MULTILINE)
    changelog_file.write_text(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute and update project version")
    parser.add_argument("--ci", action="store_true", help="Read bump type from CHANGELOG.md")
    parser.add_argument("--update", action="store_true", help="Write new version to files")
    args = parser.parse_args()

    project_root = Path(__file__).parent
    version_file = project_root / "VERSION"
    changelog_file = project_root / "CHANGELOG.md"

    current_version = read_version(version_file)

    if args.ci:
        bump_type = get_bump_type_from_changelog(changelog_file)
        if not bump_type:
            print(f"No bump type found in CHANGELOG.md, current version: {current_version}")
            return 0
        if not has_unreleased_section(changelog_file):
            print(f"No Unreleased section in CHANGELOG.md, current version: {current_version}")
            return 0
    else:
        # Default to patch bump for non-CI usage
        bump_type = "patch"

    new_version = bump_version(current_version, bump_type)

    if args.update:
        version_file.write_text(f"{new_version}\n")
        if args.ci and has_unreleased_section(changelog_file):
            update_changelog_for_release(changelog_file, new_version)
        print(f"Updated version: {current_version} -> {new_version}")
    else:
        print(f"Current: {current_version}, Next ({bump_type}): {new_version}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
