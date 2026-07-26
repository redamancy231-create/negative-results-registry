#!/usr/bin/env python3
"""从 registry.json + entry_sources.json 自动更新 README 中的统计数字和条目概览表。

用法:
    python scripts/update_readme.py          # 更新三语 README
    python scripts/update_readme.py --check  # 仅检查漂移（CI 模式），不修改文件

通过 HTML 注释标记识别需替换的段落：
    <!-- AUTO_GENERATED: entries_badge --> ... <!-- AUTO_GENERATED_END -->
    <!-- AUTO_GENERATED: summary_line --> ... <!-- AUTO_GENERATED_END -->
    <!-- AUTO_GENERATED: entry_table --> ... <!-- AUTO_GENERATED_END -->
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "registry.json"
SOURCES_PATH = PROJECT_ROOT / "scripts" / "entry_sources.json"

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

# 每种语言使用的列标题
COLUMN_HEADERS = {
    "zh-CN": ["ID", "来源", "领域", "类型"],
    "en": ["ID", "Source", "Domain", "Type"],
    "zh-Hant": ["ID", "來源", "領域", "類型"],
}

MARKER_PATTERN = re.compile(
    r"<!-- AUTO_GENERATED: (\w+) -->.*?<!-- AUTO_GENERATED_END -->", re.DOTALL
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_badge(total_entries):
    """生成 Entries badge 行。"""
    return (
        f"[![Entries](https://img.shields.io/badge/Entries-{total_entries}"
        f"-brightgreen.svg)]()"
    )


def generate_summary(lang, entries, source_map):
    """生成摘要行（已收录 N 条目，覆盖 X 领域 × Y 类型...）。"""
    total = len(entries)
    domains = sorted(set(e["domain"] for e in entries))
    categories = sorted(set(e["category"] for e in entries))

    domain_count = len(domains)
    category_count = len(categories)

    # 全部 schema 中的领域/类型数
    schema_domains = 12
    schema_categories = 9

    # 唯一来源项目数
    own_sources = set()
    external_sources = set()
    for e in entries:
        src = source_map.get(e["id"], {})
        source_name = src.get("source", "unknown")
        if src.get("is_own_project", False):
            own_sources.add(source_name)
        else:
            external_sources.add(source_name)

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


def generate_table(lang, entries, source_map):
    """生成条目概览表。"""
    headers = COLUMN_HEADERS[lang]
    domain_i18n = DOMAIN_I18N[lang]
    category_i18n = CATEGORY_I18N[lang]

    lines = []
    # 表头
    lines.append(
        "| " + " | ".join(headers) + " |"
    )
    # 分隔线
    lines.append("|" + "|".join(["------" for _ in headers]) + "|")

    for e in entries:
        eid = e["id"]
        source = source_map.get(eid, {}).get("source", "unknown")
        domain_label = domain_i18n.get(e["domain"], e["domain"])
        category_label = category_i18n.get(e["category"], e["category"])
        lines.append(
            f"| {eid} | {source} | {domain_label} | {category_label} |"
        )

    return "\n".join(lines)


def replace_markers(content, marker_name, replacement):
    """替换 content 中指定 marker 之间的内容。返回新 content 和是否发生替换。"""
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


def process_readme(lang, entries, source_map, check_only=False):
    """处理一个 README 文件。"""
    readme_path = README_PATHS[lang]
    if not readme_path.exists():
        print(f"  SKIP: {readme_path} not found")
        return True

    content = readme_path.read_text(encoding="utf-8")

    # 检查是否存在所需标记
    required_markers = ["entries_badge", "summary_line", "entry_table"]
    missing = [m for m in required_markers if f"AUTO_GENERATED: {m}" not in content]
    if missing:
        print(f"  WARNING: {readme_path.name} missing markers: {missing}")
        # 非致命——允许渐进式迁移

    total = len(entries)

    # 生成内容
    badge = generate_badge(total)
    summary = generate_summary(lang, entries, source_map)
    table = generate_table(lang, entries, source_map)

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
        else:
            # 标记不存在时跳过（非致命）
            pass

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
            print(f"  UNCHANGED: {readme_path.name} (no markers found?)")
        return True


def main():
    check_only = "--check" in sys.argv

    if not REGISTRY_PATH.exists():
        print(f"ERROR: registry.json not found at {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(1)

    registry = load_json(REGISTRY_PATH)
    entries = registry.get("entries", [])

    source_map = {}
    if SOURCES_PATH.exists():
        sources_data = load_json(SOURCES_PATH)
        source_map = sources_data.get("entries", {})

    # 按 ID 排序
    entries_sorted = sorted(entries, key=lambda e: e["id"])

    mode = "CHECK" if check_only else "UPDATE"
    print(f"=== README {mode} ===\n")

    all_ok = True
    for lang in ["zh-CN", "en", "zh-Hant"]:
        print(f"[{lang}]")
        ok = process_readme(lang, entries_sorted, source_map, check_only)
        if not ok:
            all_ok = False

    print()
    if check_only:
        if all_ok:
            print("All READMEs in sync with registry.json")
            sys.exit(0)
        else:
            print("README drift detected! Run: python scripts/update_readme.py")
            sys.exit(1)
    else:
        print("Done.")


if __name__ == "__main__":
    main()
