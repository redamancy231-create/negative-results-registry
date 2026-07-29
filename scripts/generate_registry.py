#!/usr/bin/env python3
"""从 entries/ 目录生成 registry.json 聚合索引。

用法:
    python scripts/generate_registry.py
    python scripts/generate_registry.py --lang en
    python scripts/generate_registry.py --lang zh-Hant

读取 entries/ 下所有 NRR-YYYY-NNN/NRR-YYYY-NNN.json，
校验后合并入 registry.json 的 entries 数组，更新 stats 计数。
指定 --lang 时，从对应翻译 Markdown 提取内容字段并生成语言特定 registry。
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

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

TRANSLATABLE_FIELDS = (
    "title",
    "hypothesis",
    "method",
    "expected_result",
    "actual_result",
    "interpretation",
    "lessons_learned",
)

LANGUAGE_CONFIG = {
    "en": {
        "title_label": "Title",
        "sections": {
            "hypothesis": "Original Hypothesis",
            "method": "Method",
            "expected_result": "Expected Result",
            "actual_result": "Actual Result",
            "interpretation": "Why Did It Fail?",
            "lessons_learned": "What Did We Learn?",
        },
    },
    "zh-Hant": {
        "title_label": "標題",
        "sections": {
            "hypothesis": "原始假設",
            "method": "方法",
            "expected_result": "預期結果",
            "actual_result": "實際結果",
            "interpretation": "為什麼會失敗？",
            "lessons_learned": "學到了什麼？",
        },
    },
}


def parse_args():
    """解析命令列参数。"""
    parser = argparse.ArgumentParser(description="Generate the aggregated registry JSON files.")
    parser.add_argument(
        "--lang",
        choices=LANGUAGE_CONFIG,
        help="Generate a localized registry from translated entry Markdown.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Generate output even when source entry validation fails.",
    )
    return parser.parse_args()


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


def registry_path_for_lang(lang: str | None) -> Path:
    """返回指定语言的根目录 registry 输出路径。"""
    if lang is None:
        return REGISTRY_PATH
    return PROJECT_ROOT / f"registry-{lang}.json"


def load_existing_registry(registry_path: Path):
    """加载待更新的 registry；语言文件首次生成时复用默认 registry 元数据。"""
    source_path = registry_path if registry_path.exists() else REGISTRY_PATH
    if source_path.exists():
        with open(source_path, "r", encoding="utf-8") as f:
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


def extract_title(markdown: str, label: str) -> str | None:
    """从基本信息表格提取标题。"""
    pattern = re.compile(
        rf"^\|\s*\*\*{re.escape(label)}\*\*\s*\|\s*(.*?)\s*\|\s*$",
        re.MULTILINE,
    )
    match = pattern.search(markdown)
    if match:
        return match.group(1).strip()
    return None


def extract_section(markdown: str, heading: str) -> str | None:
    """提取三级标题下、下一个二级或三级标题前的 Markdown 内容。"""
    lines = markdown.splitlines()
    header = f"### {heading}"
    start = next((i + 1 for i, line in enumerate(lines) if line.strip() == header), None)
    if start is None:
        return None

    content = []
    for line in lines[start:]:
        stripped = line.lstrip()
        if stripped.startswith("### ") or stripped.startswith("## "):
            break
        content.append(line)

    while content and content[0].strip() == "":
        content.pop(0)
    while content and content[-1].strip() in {"", "---"}:
        content.pop()

    result = "\n".join(content).strip()
    return result or None


def extract_blockquote(section: str | None) -> str | None:
    """提取 section 开头的连续 Markdown 引用块。"""
    if not section:
        return None

    quote_lines = []
    started = False
    for line in section.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(">"):
            started = True
            quote_lines.append(re.sub(r"^>\s?", "", stripped))
        elif started:
            break
        elif stripped:
            break

    result = "\n".join(quote_lines).strip()
    return result or None


def extract_ordered_list(section: str | None) -> list[str] | None:
    """从 section 提取 Markdown 或 HTML 有序列表项。"""
    if not section:
        return None

    matches = re.findall(
        r"^\s*\d+\.\s+(.*?)(?=^\s*\d+\.\s+|\Z)",
        section,
        flags=re.MULTILINE | re.DOTALL,
    )
    lessons = [match.strip() for match in matches if match.strip()]
    if lessons:
        return lessons

    html_matches = re.findall(r"<li\b[^>]*>(.*?)</li>", section, flags=re.IGNORECASE | re.DOTALL)
    lessons = [re.sub(r"\s+", " ", match).strip() for match in html_matches if match.strip()]
    return lessons or None


def parse_translated_fields(markdown: str, lang: str) -> dict:
    """从指定语言的 Markdown 中解析可翻译字段。"""
    config = LANGUAGE_CONFIG[lang]
    sections = config["sections"]

    hypothesis_section = extract_section(markdown, sections["hypothesis"])
    expected_section = extract_section(markdown, sections["expected_result"])
    lessons_section = extract_section(markdown, sections["lessons_learned"])

    return {
        "title": extract_title(markdown, config["title_label"]),
        "hypothesis": extract_blockquote(hypothesis_section),
        "method": extract_section(markdown, sections["method"]),
        "expected_result": extract_blockquote(expected_section),
        "actual_result": extract_section(markdown, sections["actual_result"]),
        "interpretation": extract_section(markdown, sections["interpretation"]),
        "lessons_learned": extract_ordered_list(lessons_section),
    }


def localize_entries(entries: list[dict], lang: str) -> list[dict]:
    """使用对应语言 Markdown 覆盖条目的内容字段，解析失败时保留源 JSON 值。"""
    localized_entries = []
    for source_entry in entries:
        entry = dict(source_entry)
        entry_id = entry["id"]
        markdown_path = ENTRIES_DIR / entry_id / f"{entry_id}-{lang}.md"

        if not markdown_path.exists():
            print(
                f"WARNING: {entry_id}: missing translation Markdown {markdown_path.name}; "
                "using source JSON content",
                file=sys.stderr,
            )
            localized_entries.append(entry)
            continue

        with open(markdown_path, "r", encoding="utf-8") as f:
            translated = parse_translated_fields(f.read(), lang)

        for field in TRANSLATABLE_FIELDS:
            value = translated.get(field)
            if value is None:
                print(
                    f"WARNING: {entry_id}: could not parse '{field}' from "
                    f"{markdown_path.name}; using source JSON value",
                    file=sys.stderr,
                )
                continue
            entry[field] = value

        localized_entries.append(entry)

    return localized_entries


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


def write_registry(registry: dict, output_path: Path):
    """写入根目录 registry，并同步到 docs/。"""
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.write("\n")

    docs_registry = PROJECT_ROOT / "docs" / output_path.name
    with open(docs_registry, "w", encoding="utf-8", newline="\n") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return docs_registry


def main_impl(lang=None, force=False):
    """Programmatic entry point for build_all.py."""
    schema = load_schema()
    entries = collect_entries()

    if schema:
        error_count = validate_all(entries, schema)
        if error_count > 0:
            print(f"\n{error_count} validation error(s) found. Aborting.", file=sys.stderr)
            print("Fix errors above or run with --force to override.", file=sys.stderr)
            if not force:
                sys.exit(1)
    else:
        print("WARNING: schema/entry.schema.json not found; skipping validation", file=sys.stderr)

    if lang:
        entries = localize_entries(entries, lang)

    output_path = registry_path_for_lang(lang)
    registry = load_existing_registry(output_path)
    today = date.today().isoformat()
    registry["metadata"]["last_updated"] = today
    registry["metadata"]["total_entries"] = len(entries)
    registry["entries"] = entries
    registry["stats"] = compute_stats(entries)

    docs_registry = write_registry(registry, output_path)
    print(f"{output_path.name} updated: {len(entries)} entries")
    print(f"{docs_registry.relative_to(PROJECT_ROOT)} synchronized")


def main():
    args = parse_args()
    main_impl(lang=args.lang, force=args.force)


if __name__ == "__main__":
    main()
