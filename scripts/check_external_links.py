#!/usr/bin/env python3
"""检查所有条目 .md 文件中的外部链接（advisory only——不阻塞 CI）。"""
import re
import urllib.request
import urllib.error
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = PROJECT_ROOT / "entries"

url_pattern = re.compile(r"\]\((https?://[^)\s]+)\)")
seen = set()
failed = 0

for entry_dir in sorted(ENTRIES_DIR.iterdir()):
    if not entry_dir.is_dir():
        continue
    md = entry_dir / f"{entry_dir.name}.md"
    if not md.exists():
        continue
    for url in url_pattern.findall(md.read_text(encoding="utf-8")):
        url = url.rstrip(".)")
        if url in seen:
            continue
        seen.add(url)
        if "arxiv.org" in url or "github.com" in url:
            print(f"  SKIP  (rate-limited host) {url}")
            continue
        try:
            req = urllib.request.Request(url, method="HEAD")
            req.add_header("User-Agent", "NRR-CI/1.0")
            urllib.request.urlopen(req, timeout=15)
            print(f"  OK  {url}")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                print(f"  SKIP  {e.code} {url}")
                continue
            print(f"  FAIL  {e.code} {url}")
            failed += 1
        except Exception:
            print(f"  SKIP  (timeout/DNS) {url}")

print(
    f"External links: {len(seen)} checked/skipped, {failed} failed "
    "(advisory only — does not block CI)"
)
