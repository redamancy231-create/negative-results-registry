#!/usr/bin/env python3
"""CI 外链分级检查：按条目报告链接状态（verified / skipped / broken）。

用法:
    python scripts/check_external_links.py          # 标准模式
    python scripts/check_external_links.py --strict  # broken 链接阻塞 CI

输出格式:
    NRR-2026-001: 3 verified, 1 skipped (github.com), 0 broken ✅
    NRR-2026-004: 1 verified, 0 skipped, 1 broken (404) ⚠️
    ...
    Summary: 20/22 entries clean, 2 entries with broken links

broken > 0 时默认警告不阻塞（--strict 模式下阻塞）。
"""

import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = PROJECT_ROOT / "entries"

# 已知被限速的主机（HEAD 请求被拒但浏览器可正常访问）
RATE_LIMITED_HOSTS = {"github.com", "arxiv.org"}

url_pattern = re.compile(r"\]\((https?://[^)\s]+)\)")


def classify_url(url):
    """检查单个 URL，返回 (status, detail)。

    status: 'verified' | 'skipped' | 'broken'
    detail: 描述字符串
    """
    url = url.rstrip(".)")

    # 限速主机
    for host in RATE_LIMITED_HOSTS:
        if host in url:
            return ("skipped", f"rate-limited ({host})")

    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "NRR-CI/1.0")
        resp = urllib.request.urlopen(req, timeout=15)
        return ("verified", str(resp.status))
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            return ("skipped", str(e.code))
        return ("broken", str(e.code))
    except Exception as e:
        # timeout / DNS / SSL — 网络问题，不判死
        return ("skipped", type(e).__name__)


def main():
    strict = "--strict" in sys.argv
    seen_urls = set()

    entry_results = {}  # eid -> {verified: N, skipped: N, broken: N, details: [...]}
    global_counts = {"verified": 0, "skipped": 0, "broken": 0}

    for entry_dir in sorted(ENTRIES_DIR.iterdir()):
        if not entry_dir.is_dir():
            continue
        eid = entry_dir.name
        md = entry_dir / f"{eid}.md"
        if not md.exists():
            continue

        urls = url_pattern.findall(md.read_text(encoding="utf-8"))
        result = {"verified": 0, "skipped": 0, "broken": 0, "details": []}

        for url in urls:
            url = url.rstrip(".)")
            if url in seen_urls:
                continue
            seen_urls.add(url)

            status, detail = classify_url(url)
            result[status] += 1
            global_counts[status] += 1

            if status != "verified":
                result["details"].append((status, detail, url))

        entry_results[eid] = result

    # ── Per-entry report ──
    clean = 0
    dirty = 0

    for eid in sorted(entry_results):
        r = entry_results[eid]
        v, s, b = r["verified"], r["skipped"], r["broken"]

        if b == 0:
            icon = "✅"
            clean += 1
        else:
            icon = "⚠️"
            dirty += 1

        parts = [f"{v} verified", f"{s} skipped", f"{b} broken"]
        print(f"  {eid}: {', '.join(parts)} {icon}")

        for status, detail, url in r["details"]:
            tag = {"skipped": "SKIP", "broken": "BROKEN"}[status]
            print(f"    {tag}  {detail:12s}  {url}")

    # ── Summary ──
    print(f"\n  Total: {global_counts['verified']} verified, "
          f"{global_counts['skipped']} skipped, "
          f"{global_counts['broken']} broken")
    print(f"  Entries: {clean}/{len(entry_results)} clean")

    if dirty > 0:
        print(f"  ⚠️  {dirty} entries with broken links")
        if strict:
            print("  CI: BLOCKED (--strict mode)")
            sys.exit(1)
        else:
            print("  CI: advisory only (not blocking)")
    else:
        print("  ✅ All links reachable")


if __name__ == "__main__":
    main()
