"""Download the URLs in urls.txt without overwriting an existing snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import time
from datetime import date
from functools import cache
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.robotparser import RobotFileParser

import requests

RAW_DIR = Path("data/raw/irdai")
MANIFEST = Path("data/manifest.csv")
USER_AGENT = "ClaimCompass/1.0 (+https://github.com/Brahma-Agni/claim-compass)"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_urls(path: Path) -> list[str]:
    lines = (raw.strip() for raw in path.read_text().splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def manifest_rows(path: Path = MANIFEST) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["source_url"]: row for row in csv.DictReader(handle)}


def filename_for(url: str, rows: dict[str, dict[str, str]]) -> str:
    if url in rows:
        return rows[url]["local_filename"]
    name = Path(unquote(urlparse(url).path)).name or "download"
    return name.replace(" ", "-").lower()


@cache
def robot_rules(root: str) -> RobotFileParser | None:
    robots = RobotFileParser(f"{root}/robots.txt")
    try:
        robots.read()
    except OSError:
        print(f"warning: robots.txt unavailable for {root}; proceeding carefully")
        return None
    return robots


def robots_allows(url: str) -> bool:
    parsed = urlparse(url)
    rules = robot_rules(f"{parsed.scheme}://{parsed.netloc}")
    return rules is None or rules.can_fetch(USER_AGENT, url)


def download(url: str, rows: dict[str, dict[str, str]]) -> str:
    if not robots_allows(url):
        return f"BLOCKED by robots.txt: {url}"

    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    content = response.content
    if not content.startswith(b"%PDF"):
        raise ValueError(f"IRDAI returned non-PDF content for {url}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / filename_for(url, rows)
    digest = sha256(content)
    if target.exists():
        if sha256(target.read_bytes()) == digest:
            return f"unchanged {target}"
        changed_name = f"{target.stem}.changed-{date.today().isoformat()}-{digest[:12]}{target.suffix}"
        changed = target.with_name(changed_name)
        changed.write_bytes(content)
        return f"CHANGED upstream; preserved old file and saved review copy {changed}"

    expected = rows.get(url, {}).get("sha256")
    if expected and expected != digest:
        changed_name = f"{target.stem}.changed-{date.today().isoformat()}-{digest[:12]}{target.suffix}"
        changed = target.with_name(changed_name)
        changed.write_bytes(content)
        return f"CHANGED since manifest; saved review copy {changed}"
    target.write_bytes(content)
    return f"saved {target} ({len(content)} bytes, sha256 {digest})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url_file", nargs="?", type=Path, default=Path("urls.txt"))
    parser.add_argument("--delay", type=float, default=2.0, help="seconds between requests")
    args = parser.parse_args()
    rows = manifest_rows()
    urls = read_urls(args.url_file)
    for index, url in enumerate(urls):
        try:
            print(download(url, rows))
        except (OSError, requests.RequestException, ValueError) as exc:
            print(f"failed {url}: {exc}")
        if index < len(urls) - 1:
            time.sleep(args.delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
