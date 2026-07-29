#!/usr/bin/env python3
"""一站式构建入口——生成三语 registry + 更新 README + 校验一致性。

用法:
    python scripts/build_all.py          # 完整构建
    python scripts/build_all.py --check   # 只验证，不修改文件
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import generate_registry
import update_readme


def check_id_sets():
    """验证三语 registry 的条目 ID 集合一致，且根目录与 docs/ 镜像字节一致。"""
    import json

    errors = []
    registries = {}

    # Load root registries
    for suffix in ["", "-en", "-zh-Hant"]:
        name = f"registry{suffix}.json"
        path = PROJECT_ROOT / name
        docs_path = PROJECT_ROOT / "docs" / name

        if not path.exists():
            errors.append(f"MISSING: {name}")
            continue

        with open(path, encoding="utf-8") as f:
            registries[suffix] = json.load(f)

        # Check docs mirror
        if not docs_path.exists():
            errors.append(f"MISSING: docs/{name}")
        elif path.read_bytes() != docs_path.read_bytes():
            errors.append(f"BYTE DIFFER: {name} vs docs/{name}")

    if len(registries) < 3:
        errors.append(f"Only {len(registries)}/3 registries found")
        return errors

    # Compare ID sets
    ids = {}
    for suffix, data in registries.items():
        ids[suffix] = {e["id"] for e in data.get("entries", [])}
        if suffix:
            only_here = ids[suffix] - ids[""]
            if only_here:
                errors.append(f"ID SET: registry{suffix}.json has {len(only_here)} IDs not in registry.json: {sorted(only_here)[:5]}")

    # Check entry counts
    counts = {s: len(data.get("entries", [])) for s, data in registries.items()}
    if len(set(counts.values())) > 1:
        errors.append(f"ENTRY COUNT MISMATCH: {counts}")

    if not errors:
        print("  ID sets: OK (all 3 registries share identical IDs)")
        print(f"  Entry count: {counts['']} (consistent across all locales)")
        print("  Root/docs mirror: OK (byte-identical)")

    return errors


def main():
    parser = argparse.ArgumentParser(description="One-command build for all registry artifacts")
    parser.add_argument("--check", action="store_true", help="Validate only, do not write")
    args = parser.parse_args()

    if args.check:
        print("build_all --check: validating existing artifacts...")
        errors = check_id_sets()
        if errors:
            print("\nVALIDATION FAILED:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("All checks passed.")
        return

    print("=== 1/4: Generating zh-CN registry ===")
    generate_registry.main_impl(lang=None)

    print("\n=== 2/4: Generating EN registry ===")
    generate_registry.main_impl(lang="en")

    print("\n=== 3/4: Generating zh-Hant registry ===")
    generate_registry.main_impl(lang="zh-Hant")

    print("\n=== 4/4: Updating READMEs ===")
    update_readme.main_impl()

    print("\n=== Validating ===")
    errors = check_id_sets()
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nBuild complete. 6 registry files + 3 READMEs updated.")


if __name__ == "__main__":
    main()
