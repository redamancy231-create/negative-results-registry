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
import socket
import ssl
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
    except urllib.error.URLError as e:
        reason = e.reason
        # DNS 解析失败、SSL 证书错误 → 可能是真死链
        if isinstance(reason, socket.gaierror):
            return ("broken", f"DNS: {reason}")
        if isinstance(reason, ssl.SSLError):
            return ("broken", f"SSL: {reason}")
        # 连接超时/拒绝 → 可能是临时网络问题
        return ("skipped", type(reason).__name__)
    except Exception as e:
        return ("skipped", type(e).__name__)


def main():
    strict = "--strict" in sys.argv

    # Windows 默认 GBK 控制台无法输出 emoji
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    seen_urls = set()
    entry_results = {}
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
        # 条目级计数不受全局去重影响
        entry_seen = set()

        for url in urls:
            url = url.rstrip(".)")
            if url in entry_seen:
                continue
            entry_seen.add(url)

            status, detail = classify_url(url)

            # 全局去重（仅影响 global_counts——避免同一 URL 重复计数）
            if url not in seen_urls:
                seen_urls.add(url)
                global_counts[status] += 1

            # 条目级计数——不受全局去重影响
            result[status] += 1

            if status != "verified":
                result["details"].append((status, detail, url))

        entry_results[eid] = result

    clean = 0
    dirty = 0

    for eid in sorted(entry_results):
        r = entry_results[eid]
        v, s, b = r["verified"], r["skipped"], r["broken"]

        if b == 0:
            icon = "✅"  # ✅
            clean += 1
        else:
            icon = "⚠️"  # ⚠️
            dirty += 1

        parts = [f"{v} verified", f"{s} skipped", f"{b} broken"]
        print(f"  {eid}: {', '.join(parts)} {icon}")

        for status, detail, url in r["details"]:
            tag = {"skipped": "SKIP", "broken": "BROKEN"}[status]
            print(f"    {tag}  {detail:12s}  {url}")

    print(f"\n  Total (unique URLs): {global_counts['verified']} verified, "
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
