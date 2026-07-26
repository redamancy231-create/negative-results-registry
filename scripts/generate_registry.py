#!/usr/bin/env python3
"""从 entries/ 目录生成 registry.json 聚合索引。

用法:
    python scripts/generate_registry.py

读取 entries/ 下所有 NRR-YYYY-NNN/NRR-YYYY-NNN.json，
校验后合并入 registry.json 的 entries 数组，更新 stats 计数。
"""

import json
import sys
from datetime import date
from pathlib import Path
from collections import Counter

try:
    import jsonschema  # type: ignore[import-untyped]
    HAS_JSONSCHEMA = True
except ImportError:
    jsonschema = None  # type: ignore[assignment]
    HAS_JSONSCHEMA = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = PROJECT_ROOT / "entries"
REGISTRY_PATH = PROJECT_ROOT / "registry.json"
SCHEMA_PATH = PROJECT_ROOT / "schema" / "entry.schema.json"


def validate_entry(entry: dict, schema: dict) -> list[str]:
    """校验单个条目，返回错误消息列表。无错误时返回空列表。"""
    errors = []
    if jsonschema is not None:
        try:
            validator = jsonschema.Draft202012Validator(schema)
            for err in validator.iter_errors(entry):
                errors.append(f"  Schema: {err.message} (path: {'/'.join(str(p) for p in err.absolute_path)})")
        except Exception as e:
            errors.append(f"  Schema validation failed: {e}")
    else:
        errors.append("  WARNING: jsonschema not installed; skipping schema validation")

    # Cross-field checks
    eid = entry.get("id", "")
    # ID pattern
    import re
    if not re.match(r"^NRR-\d{4}-\d{3}$", eid):
        errors.append(f"  ID pattern mismatch: '{eid}' (expected NRR-YYYY-NNN)")

    # ID year vs date year consistency
    entry_date = entry.get("date", "")
    if eid and entry_date:
        id_year = eid[4:8]
        date_year = entry_date[:4]
        if id_year != date_year:
            errors.append(f"  ID year ({id_year}) != date year ({date_year})")

    # lessons_learned count
    lessons = entry.get("lessons_learned", [])
    if len(lessons) > 5:
        errors.append(f"  lessons_learned has {len(lessons)} items (max 5)")

    # tags count
    tags = entry.get("tags", [])
    if len(tags) > 10:
        errors.append(f"  tags has {len(tags)} items (max 10)")

    return errors


def validate_all(entries: list[dict], schema: dict) -> int:
    """校验所有条目。返回错误数，非零时向 stderr 输出错误详情。"""
    error_count = 0
    seen_ids = set()
    for entry in entries:
        eid = entry.get("id", "<missing>")
        # Duplicate ID check
        if eid in seen_ids:
            print(f"ERROR: Duplicate ID: {eid}", file=sys.stderr)
            error_count += 1
            continue
        seen_ids.add(eid)

        # Validate
        errs = validate_entry(entry, schema)
        if errs:
            print(f"ERROR: {eid}:", file=sys.stderr)
            for e in errs:
                print(e, file=sys.stderr)
            error_count += 1

    return error_count


def load_schema():
    """加载 entry JSON Schema。"""
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def load_existing_registry():
    """加载现有 registry.json。"""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"metadata": {"total_entries": 0}, "entries": [], "stats": {}}


def collect_entries():
    """遍历 entries/ 收集所有 .json 条目。同时检查 .md 双件和目录名一致性。"""
    entries = []
    if not ENTRIES_DIR.exists():
        return entries

    for entry_dir in sorted(ENTRIES_DIR.iterdir()):
        if not entry_dir.is_dir():
            continue
        dir_name = entry_dir.name
        json_file = entry_dir / f"{dir_name}.json"
        md_file = entry_dir / f"{dir_name}.md"

        # Check both files exist
        if not json_file.exists():
            print(f"ERROR: Missing JSON: {dir_name}/{dir_name}.json", file=sys.stderr)
            continue
        if not md_file.exists():
            print(f"WARNING: Missing Markdown: {dir_name}/{dir_name}.md", file=sys.stderr)

        with open(json_file, "r", encoding="utf-8") as f:
            entry = json.load(f)

        # Check ID matches directory name
        if entry.get("id") != dir_name:
            print(f"ERROR: ID mismatch: json.id='{entry.get('id')}' vs dir='{dir_name}'", file=sys.stderr)
            continue

        entries.append(entry)
    return entries


def compute_stats(entries):
    """计算聚合统计。"""
    domains = Counter()
    categories = Counter()
    years = Counter()
    models = Counter()

    for e in entries:
        domains[e.get("domain", "unknown")] += 1
        categories[e.get("category", "unknown")] += 1
        if "date" in e:
            years[e["date"][:4]] += 1
        for m in e.get("models_used", []):
            models[m] += 1

    return {
        "by_domain": dict(domains),
        "by_category": dict(categories),
        "by_year": dict(years),
        "models_used": dict(models),
    }


def main():
    schema = load_schema()
    registry = load_existing_registry()
    entries = collect_entries()

    # Validate before proceeding
    if schema:
        error_count = validate_all(entries, schema)
        if error_count > 0:
            print(f"\n{error_count} validation error(s) found. Aborting.", file=sys.stderr)
            print("Fix errors above or run with --force to override.", file=sys.stderr)
            if "--force" not in sys.argv:
                sys.exit(1)
    else:
        print("WARNING: schema/entry.schema.json not found; skipping validation", file=sys.stderr)

    today = date.today().isoformat()
    registry["metadata"]["last_updated"] = today
    registry["metadata"]["total_entries"] = len(entries)
    registry["entries"] = entries
    registry["stats"] = compute_stats(entries)

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    # 同步到 docs/ 供 GitHub Pages 部署
    docs_registry = PROJECT_ROOT / "docs" / "registry.json"
    with open(docs_registry, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    print(f"registry.json updated: {len(entries)} entries")


if __name__ == "__main__":
    main()
