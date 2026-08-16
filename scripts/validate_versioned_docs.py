#!/usr/bin/env python3
"""Validate a milestone-oriented project documentation tree."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def local_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")].strip()
    else:
        title_match = re.match(
            r"""^(.*?)(?:\s+(?:"[^"]*"|'[^']*'|\([^)]*\)))$""",
            target,
        )
        if title_match:
            target = title_match.group(1).strip()

    if not target or target.startswith("#"):
        return None

    lowered = target.lower()
    if lowered.startswith(
        ("http://", "https://", "mailto:", "tel:", "data:", "app://")
    ):
        return None

    return unquote(target.split("#", 1)[0])


def validate_markdown_links(docs_dir: Path) -> list[str]:
    errors: list[str] = []

    for markdown_file in docs_dir.rglob("*.md"):
        content = markdown_file.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(content):
            target = local_link_target(match.group(1))
            if target is None:
                continue

            target_path = Path(target)
            if target_path.is_absolute():
                resolved = target_path
            else:
                resolved = (markdown_file.parent / target_path).resolve()

            if not resolved.exists():
                relative_file = markdown_file.relative_to(docs_dir.parent)
                errors.append(f"{relative_file}: 链接目标不存在：{target}")

    return errors


def validate_project(project_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    docs_dir = project_root / "docs"
    docs_readme = docs_dir / "README.md"
    versions_dir = docs_dir / "versions"

    if not docs_dir.is_dir():
        return ["缺少 docs/ 目录。"], warnings

    if not docs_readme.is_file():
        errors.append("缺少 docs/README.md。")

    if not versions_dir.is_dir():
        errors.append("缺少 docs/versions/ 目录。")
        return errors, warnings

    version_dirs = sorted(
        path for path in versions_dir.iterdir() if path.is_dir()
    )

    if not version_dirs:
        errors.append("docs/versions/ 中没有版本目录。")

    readme_content = (
        docs_readme.read_text(encoding="utf-8") if docs_readme.is_file() else ""
    )

    for version_dir in version_dirs:
        version = version_dir.name
        relative_version_dir = version_dir.relative_to(project_root)

        if not VERSION_RE.fullmatch(version):
            warnings.append(f"{relative_version_dir}: 目录名不是标准 vX.Y.Z 格式。")

        for required_name in ("requirements.md", "completion.md"):
            required_file = version_dir / required_name
            if not required_file.is_file():
                errors.append(f"{relative_version_dir}: 缺少 {required_name}。")

        version_readmes = [
            path for path in version_dir.iterdir()
            if path.is_file() and path.name.lower() == "readme.md"
        ]
        if version_readmes:
            errors.append(f"{relative_version_dir}: 版本目录不应包含 README.md。")

        required_links = (
            f"versions/{version}/requirements.md",
            f"versions/{version}/completion.md",
        )
        for link in required_links:
            if link not in readme_content.replace("\\", "/"):
                errors.append(f"docs/README.md 未链接到 {link}。")

    errors.extend(validate_markdown_links(docs_dir))
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查按里程碑组织的 docs 目录。"
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="项目根目录，默认是当前目录。",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    errors, warnings = validate_project(project_root)

    for warning in warnings:
        print(f"警告：{warning}")

    if errors:
        for error in errors:
            print(f"错误：{error}")
        print(f"验证失败：{len(errors)} 个错误，{len(warnings)} 个警告。")
        return 1

    print(f"验证通过：0 个错误，{len(warnings)} 个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
