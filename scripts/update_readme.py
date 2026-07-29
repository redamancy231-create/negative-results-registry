#!/usr/bin/env python3
"""从 registry.json 自动更新 README 中的统计数字和条目概览表。

用法:
    python scripts/update_readme.py          # 更新三语 README
    python scripts/update_readme.py --check  # 仅检查漂移（CI 模式），不修改文件

通过 HTML 注释标记识别需替换的段落：
    <!-- AUTO_GENERATED: entries_badge --> ... <!-- AUTO_GENERATED_END -->
    <!-- AUTO_GENERATED: summary_line --> ... <!-- AUTO_GENERATED_END -->
    <!-- AUTO_GENERATED: entry_table --> ... <!-- AUTO_GENERATED_END -->

数据来源：registry.json 中的条目（Schema V2 起 source_project/source_authors/analyst
均为条目内嵌字段，无需额外映射文件）。
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "registry.json"

README_PATHS = {
    "zh-CN": PROJECT_ROOT / "README.md",
    "en": PROJECT_ROOT / "en" / "README.md",
    "zh-Hant": PROJECT_ROOT / "zh-Hant" / "README.md",
}

# 领域和类型的三语翻译表
DOMAIN_I18N = {
    "zh-CN": {
        "prompt-engineering": "Prompt 工程",
        "code-review": "代码审查",
        "methodology-extraction": "方法论提取",
        "workflow-orchestration": "工作流编排",
        "document-generation": "文档生成",
        "multi-model-collaboration": "多模型协作",
        "quantitative-research": "量化研究",
        "academic-writing": "学术写作",
        "tool-building": "工具开发",
        "skill-design": "Skill 设计",
        "benchmarking": "基准测试",
        "other": "其他",
    },
    "en": {
        "prompt-engineering": "Prompt Engineering",
        "code-review": "Code Review",
        "methodology-extraction": "Methodology Extraction",
        "workflow-orchestration": "Workflow Orchestration",
        "document-generation": "Document Generation",
        "multi-model-collaboration": "Multi-Model Collaboration",
        "quantitative-research": "Quantitative Research",
        "academic-writing": "Academic Writing",
        "tool-building": "Tool Development",
        "skill-design": "Skill Design",
        "benchmarking": "Benchmarking",
        "other": "Other",
    },
    "zh-Hant": {
        "prompt-engineering": "Prompt 工程",
        "code-review": "程式碼審查",
        "methodology-extraction": "方法論提取",
        "workflow-orchestration": "工作流程編排",
        "document-generation": "檔案生成",
        "multi-model-collaboration": "多模型協作",
        "quantitative-research": "量化研究",
        "academic-writing": "學術寫作",
        "tool-building": "工具開發",
        "skill-design": "Skill 設計",
        "benchmarking": "基準測試",
        "other": "其他",
    },
}

CATEGORY_I18N = {
    "zh-CN": {
        "null-result": "零结果",
        "ceiling-effect": "天花板效应",
        "worse-than-baseline": "劣于基线",
        "failed-to-replicate": "复现失败",
        "methodology-failure": "方法失败",
        "abandoned-dead-end": "死胡同",
        "hypothesis-falsified": "假设被证伪",
        "tool-unfit-for-purpose": "工具不适用",
        "other": "其他",
    },
    "en": {
        "null-result": "Null Result",
        "ceiling-effect": "Ceiling Effect",
        "worse-than-baseline": "Worse Than Baseline",
        "failed-to-replicate": "Failed to Replicate",
        "methodology-failure": "Methodology Failure",
        "abandoned-dead-end": "Abandoned Dead End",
        "hypothesis-falsified": "Hypothesis Falsified",
        "tool-unfit-for-purpose": "Tool Unfit for Purpose",
        "other": "Other",
    },
    "zh-Hant": {
        "null-result": "零結果",
        "ceiling-effect": "天花板效應",
        "worse-than-baseline": "劣於基線",
        "failed-to-replicate": "重現失敗",
        "methodology-failure": "方法失敗",
        "abandoned-dead-end": "死胡同",
        "hypothesis-falsified": "假設遭證偽",
        "tool-unfit-for-purpose": "工具不適用",
        "other": "其他",
    },
}

COLUMN_HEADERS = {
    "zh-CN": ["ID", "来源", "领域", "类型"],
    "en": ["ID", "Source", "Domain", "Type"],
    "zh-Hant": ["ID", "來源", "領域", "類型"],
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_badge(total_entries):
    return (
        f"[![Entries](https://img.shields.io/badge/Entries-{total_entries}"
        f"-brightgreen.svg)](https://redamancy231-create.github.io/negative-results-registry/)"
    )


def is_own_project(entry):
    """第一方条目：source_authors == analyst == submitted_by（均为同一维护者）。"""
    return (
        entry.get("source_authors", "") == entry.get("analyst", "")
        and entry.get("source_authors", "") == entry.get("submitted_by", "")
    )


def generate_summary(lang, entries):
    """生成摘要行。"""
    total = len(entries)
    domain_count = len(set(e["domain"] for e in entries))
    category_count = len(set(e["category"] for e in entries))
    schema_domains = 12
    schema_categories = 9

    own_sources = set()
    external_sources = set()
    for e in entries:
        sp = e.get("source_project", "unknown")
        if is_own_project(e):
            own_sources.add(sp)
        else:
            external_sources.add(sp)

    templates = {
        "zh-CN": (
            f"当前已收录 **{total} 个条目**，覆盖 {domain_count} 个领域 × "
            f"{category_count} 种类型（Schema 共 {schema_domains} 领域 × "
            f"{schema_categories} 类型），来自 {len(own_sources)} 个自有公开项目"
            f" + {len(external_sources)} 个外部来源（学术论文 + 开源项目）："
        ),
        "en": (
            f"The registry currently contains **{total} entries** spanning "
            f"{domain_count} domains × {category_count} types (out of a "
            f"{schema_domains}-domain × {schema_categories}-type schema), "
            f"drawn from {len(own_sources)} of our own public projects + "
            f"{len(external_sources)} external sources (academic papers + "
            f"open-source projects):"
        ),
        "zh-Hant": (
            f"目前已收錄 **{total} 個條目**，涵蓋 {domain_count} 個領域 × "
            f"{category_count} 種類型（Schema 共 {schema_domains} 領域 × "
            f"{schema_categories} 類型），來自 {len(own_sources)} 個自有公開專案"
            f" + {len(external_sources)} 個外部來源（學術論文 + 開源專案）："
        ),
    }
    return templates[lang]


def generate_table(lang, entries):
    """生成条目概览表（来源列取自 entry.source_project）。"""
    headers = COLUMN_HEADERS[lang]
    domain_i18n = DOMAIN_I18N[lang]
    category_i18n = CATEGORY_I18N[lang]

    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["------" for _ in headers]) + "|",
    ]

    for e in entries:
        eid = e["id"]
        source = e.get("source_project", "unknown")
        domain_label = domain_i18n.get(e["domain"], e["domain"])
        category_label = category_i18n.get(e["category"], e["category"])
        lines.append(
            f"| {eid} | {source} | {domain_label} | {category_label} |"
        )

    return "\n".join(lines)


def replace_markers(content, marker_name, replacement):
    pattern = (
        r"<!-- AUTO_GENERATED: " + marker_name + r" -->.*?"
        r"<!-- AUTO_GENERATED_END -->"
    )
    new_text = (
        f"<!-- AUTO_GENERATED: {marker_name} -->\n"
        f"{replacement}\n"
        f"<!-- AUTO_GENERATED_END -->"
    )
    new_content, count = re.subn(pattern, new_text, content, flags=re.DOTALL)
    return new_content, count > 0


def process_readme(lang, entries, check_only=False):
    readme_path = README_PATHS[lang]
    if not readme_path.exists():
        print(f"  SKIP: {readme_path} not found")
        return True

    content = readme_path.read_text(encoding="utf-8")

    required_markers = ["entries_badge", "summary_line", "entry_table"]
    missing = [m for m in required_markers if f"AUTO_GENERATED: {m}" not in content]
    if missing:
        print(f"  WARNING: {readme_path.name} missing markers: {missing}")

    badge = generate_badge(len(entries))
    summary = generate_summary(lang, entries)
    table = generate_table(lang, entries)

    new_content = content
    changed = False

    for marker_name, generated in [
        ("entries_badge", badge),
        ("summary_line", summary),
        ("entry_table", table),
    ]:
        new_content, replaced = replace_markers(new_content, marker_name, generated)
        if replaced:
            changed = True

    if check_only:
        if content != new_content:
            print(f"  DRIFT: {readme_path.name} would be modified")
            return False
        else:
            print(f"  OK: {readme_path.name}")
            return True
    else:
        if changed:
            readme_path.write_text(new_content, encoding="utf-8")
            print(f"  UPDATED: {readme_path.name}")
        else:
            print(f"  UNCHANGED: {readme_path.name}")
        return True


def main_impl(check_only=False):
    """Programmatic entry point for build_all.py."""
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"registry.json not found at {REGISTRY_PATH}")

    registry = load_json(REGISTRY_PATH)
    entries = sorted(registry.get("entries", []), key=lambda e: e["id"])

    mode = "CHECK" if check_only else "UPDATE"
    print(f"=== README {mode} ===\n")

    for lang in ["zh-CN", "en", "zh-Hant"]:
        print(f"[{lang}]")
        process_readme(lang, entries, check_only)

    print()


def main():
    check_only = "--check" in sys.argv
    try:
        main_impl(check_only=check_only)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print("Done.")


if __name__ == "__main__":
    main()
