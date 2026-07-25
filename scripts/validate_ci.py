#!/usr/bin/env python3
"""CI 校验脚本：JSON Schema 校验 + 内部链接检查 + registry.json 一致性。

在 GitHub Actions 中运行，也支持本地手动执行。
用法: python scripts/validate_ci.py [--skip-external-links]
"""

import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    jsonschema = None
    HAS_JSONSCHEMA = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = PROJECT_ROOT / "entries"
SCHEMA_PATH = PROJECT_ROOT / "schema" / "entry.schema.json"
REGISTRY_PATH = PROJECT_ROOT / "registry.json"

EXIT_CODE = 0


def fail(msg: str):
    global EXIT_CODE
    print(f"  FAIL  {msg}")
    EXIT_CODE = 1


def ok(msg: str):
    print(f"  OK    {msg}")


# ── Schema Validation ──────────────────────────────────────────────

def validate_schema():
    print("\n=== Schema Validation ===")
    if not HAS_JSONSCHEMA:
        print("  SKIP  jsonschema not installed")
        return

    if not SCHEMA_PATH.exists():
        fail(f"Schema file not found: {SCHEMA_PATH}")
        return

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    if not ENTRIES_DIR.exists():
        fail(f"Entries directory not found: {ENTRIES_DIR}")
        return

    validator = jsonschema.Draft202012Validator(schema)  # type: ignore[union-attr]
    entry_count = 0
    seen_ids = set()

    for entry_dir in sorted(ENTRIES_DIR.iterdir()):
        if not entry_dir.is_dir():
            continue
        dir_name = entry_dir.name
        json_file = entry_dir / f"{dir_name}.json"
        md_file = entry_dir / f"{dir_name}.md"

        if not json_file.exists():
            fail(f"{dir_name}: missing .json")
            continue
        if not md_file.exists():
            fail(f"{dir_name}: missing .md")
            # non-fatal — continue with JSON check

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                entry = json.load(f)
        except json.JSONDecodeError as e:
            fail(f"{dir_name}: invalid JSON — {e}")
            continue

        entry_count += 1
        eid = entry.get("id", "<missing>")

        # ID pattern
        if not re.match(r"^NRR-\d{4}-\d{3}$", eid):
            fail(f"{eid}: ID pattern mismatch (expected NRR-YYYY-NNN)")

        # ID == directory name
        if eid != dir_name:
            fail(f"{eid}: ID != directory name '{dir_name}'")

        # Duplicate ID
        if eid in seen_ids:
            fail(f"{eid}: duplicate ID")
        seen_ids.add(eid)

        # ID year vs date year
        entry_date = entry.get("date", "")
        if eid and entry_date:
            id_year = eid[4:8]
            date_year = entry_date[:4]
            if id_year != date_year:
                fail(f"{eid}: ID year ({id_year}) != date year ({date_year})")

        # Schema validation
        errors = list(validator.iter_errors(entry))
        if errors:
            for err in errors:
                path = "/".join(str(p) for p in err.absolute_path) if err.absolute_path else "(root)"
                fail(f"{eid}: schema — {err.message} (at {path})")
        else:
            ok(f"{eid}: schema valid")

        # lessons_learned count
        lessons = entry.get("lessons_learned", [])
        if len(lessons) > 5:
            fail(f"{eid}: {len(lessons)} lessons (max 5)")

        # tags count
        tags = entry.get("tags", [])
        if len(tags) > 10:
            fail(f"{eid}: {len(tags)} tags (max 10)")

    print(f"\n  Total: {entry_count} entries checked")


# ── Internal Link Check ────────────────────────────────────────────

def check_internal_links():
    print("\n=== Internal Links ===")
    if not ENTRIES_DIR.exists():
        return

    md_link_pattern = re.compile(r'\]\(([^)]+)\)')

    for entry_dir in sorted(ENTRIES_DIR.iterdir()):
        if not entry_dir.is_dir():
            continue
        md_file = entry_dir / f"{entry_dir.name}.md"
        if not md_file.exists():
            continue

        content = md_file.read_text(encoding="utf-8")
        links = md_link_pattern.findall(content)

        for link in links:
            # Skip external URLs, anchors, and mailto
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue

            # Resolve relative to the .md file's directory
            target = (md_file.parent / link).resolve()
            if not target.exists():
                fail(f"{entry_dir.name}: broken link → {link}")


# ── External Link Check ────────────────────────────────────────────

def check_external_links():
    print("\n=== External Links ===")
    if not ENTRIES_DIR.exists():
        return

    url_pattern = re.compile(r'\]\((https?://[^)\s]+)\)')
    seen_urls = set()
    checked = 0
    failed = 0
    skipped = 0

    for entry_dir in sorted(ENTRIES_DIR.iterdir()):
        if not entry_dir.is_dir():
            continue
        md_file = entry_dir / f"{entry_dir.name}.md"
        if not md_file.exists():
            continue

        urls = url_pattern.findall(md_file.read_text(encoding="utf-8"))
        for url in urls:
            url = url.rstrip(".)")
            if url in seen_urls:
                continue
            seen_urls.add(url)

            # Skip arxiv.org and github.com — rate-limited for automated HEAD requests
            if "arxiv.org" in url or "github.com" in url:
                skipped += 1
                continue

            try:
                req = urllib.request.Request(url, method="HEAD")
                req.add_header("User-Agent", "NRR-CI/1.0")
                urllib.request.urlopen(req, timeout=15)
                checked += 1
            except urllib.error.HTTPError as e:
                # 403/429 are rate-limiting, not broken links
                if e.code in (403, 429):
                    skipped += 1
                else:
                    fail(f"{e.code} {url}")
                    failed += 1
            except Exception:
                skipped += 1  # timeout / DNS — don't fail CI on network issues

    print(f"\n  Checked: {checked}  Skipped: {skipped}  Failed: {failed}")


# ── Registry Consistency ───────────────────────────────────────────

def check_registry_consistency():
    print("\n=== Registry Consistency ===")
    if not REGISTRY_PATH.exists():
        fail(f"registry.json not found: {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    # Count actual entries on disk
    actual_entries = []
    if ENTRIES_DIR.exists():
        for entry_dir in sorted(ENTRIES_DIR.iterdir()):
            if not entry_dir.is_dir():
                continue
            json_file = entry_dir / f"{entry_dir.name}.json"
            if json_file.exists():
                with open(json_file, "r", encoding="utf-8") as f:
                    actual_entries.append(json.load(f))

    # total_entries match
    declared = registry["metadata"]["total_entries"]
    actual = len(actual_entries)
    if declared != actual:
        fail(f"registry.json total_entries={declared} but disk has {actual}")
    else:
        ok(f"total_entries: {declared} == disk entries ({actual})")

    # entries[] count match
    registry_entries = len(registry.get("entries", []))
    if registry_entries != actual:
        fail(f"registry.json entries[] length={registry_entries} but disk has {actual}")
    else:
        ok(f"entries[] length: {registry_entries} == disk entries ({actual})")

    # Stats consistency (spot-check by_domain)
    from collections import Counter
    domains = Counter(e.get("domain", "unknown") for e in actual_entries)
    declared_domains = registry.get("stats", {}).get("by_domain", {})
    for domain, count in domains.items():
        if declared_domains.get(domain) != count:
            fail(f"stats.by_domain['{domain}']: registry={declared_domains.get(domain)} != actual={count}")
    if domains.keys() == declared_domains.keys():
        ok("stats.by_domain: all keys match")
    else:
        ok("stats.by_domain: keys differ (non-fatal)")


# ── Main ───────────────────────────────────────────────────────────

def main():
    skip_external = "--skip-external-links" in sys.argv

    validate_schema()
    check_internal_links()
    check_registry_consistency()

    if not skip_external:
        check_external_links()
    else:
        print("\n=== External Links ===  SKIP (--skip-external-links)")

    print(f"\n{'='*40}")
    if EXIT_CODE == 0:
        print("CI PASSED")
    else:
        print(f"CI FAILED ({EXIT_CODE} error(s))")
    sys.exit(EXIT_CODE)


if __name__ == "__main__":
    main()
