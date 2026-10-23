"""Count and verify the PDFs recorded in data/manifest.csv."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from pypdf import PdfReader

RAW_DIR = Path("data/raw/irdai")
MANIFEST = Path("data/manifest.csv")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_dataset(raw_dir: Path = RAW_DIR, manifest: Path = MANIFEST) -> tuple[int, int, list[str]]:
    pages = 0
    files = 0
    problems: list[str] = []
    with manifest.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            path = raw_dir / row["local_filename"]
            if not path.exists():
                problems.append(f"missing: {path}")
                continue
            try:
                count = len(PdfReader(path).pages)
            except Exception as exc:  # pypdf exposes several parse-error classes
                problems.append(f"broken: {path} ({type(exc).__name__})")
                continue
            files += 1
            pages += count
            print(f"{count:5d} pages  {path}")
            if count != int(row["page_count"]):
                problems.append(f"page-count mismatch: {path} ({count} != {row['page_count']})")
            if file_sha256(path) != row["sha256"]:
                problems.append(f"hash mismatch: {path}")
    return files, pages, problems


def main() -> int:
    files, pages, problems = verify_dataset()
    print(f"\nPDF files: {files} | PDF pages: {pages} | problems: {len(problems)}")
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
