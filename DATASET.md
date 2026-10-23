# Dataset

The first verified corpus contains 197 pages from four official IRDAI documents.
The immutable PDFs live in `data/raw/irdai/` and are intentionally not committed.
Checksums and lifecycle metadata are recorded in `data/manifest.csv`.

**Product:** ClaimCompass (regulation copilot)
**Official publisher:** Insurance Regulatory and Development Authority of India (IRDAI)
**Why trusted:** Every document was downloaded from `irdai.gov.in` and is linked to
its official document-detail record below.

| Document | Official record | Pages | Language | Retrieved |
|---|---|---:|---|---|
| Master Circular on Health Insurance Business, 2024 | [IRDAI/HLT/CIR/PRO/84/5/2024](https://irdai.gov.in/document-detail?documentId=4942918) | 17 | English | 2026-10-23 |
| IRDAI (Insurance Products) Regulations, 2024 | [IRDAI/Reg/8/202/2024](https://irdai.gov.in/document-detail?documentId=4590475) | 39 | Hindi and English | 2026-10-23 |
| IRDAI (Protection of Policyholder's Interests, Operations and Allied Matters of Insurers) Regulations, 2024 | [IRDAI/Reg/11/205/2024](https://irdai.gov.in/document-detail?documentId=4590885) | 32 | Hindi and English | 2026-10-23 |
| Master Circular on Protection of Policyholders' Interests, 2024 | [IRDAI/PP&GR/CIR/MISC/117/9/2024](https://irdai.gov.in/document-detail?documentId=5625747) | 109 | English | 2026-10-23 |

## Samples

`data/sample/` contains page-aware text extracts for claims handling, cashless
authorization, discharge, rejection, grievances, and Ombudsman escalation. The
filename and page markers keep each extract traceable to its source PDF.

## Download and verify

Install the development requirements, then run:

```bash
python tools/download.py urls.txt
python tools/count_pages.py
```

The downloader checks `robots.txt`, uses an identifiable user agent, waits two
seconds between requests, rejects non-PDF responses, and never silently overwrites
an existing document. If a permitted source serves different bytes at the same URL,
it preserves the old snapshot and saves a dated `.changed-...` copy for review. The
verification command checks all four files against the manifest page counts and
SHA-256 hashes.

### Current access limitation

On 2026-10-23, `https://irdai.gov.in/robots.txt` declared `Disallow: /` for all
automated user agents. Accordingly, `tools/download.py` stops before requesting the
PDFs. To rebuild while this rule remains in force, open each official document-detail
record in the table above, download its attachment manually if the website terms
continue to permit it, place it at the manifest's `local_filename`, and run
`python tools/count_pages.py`. Do not bypass the restriction. The existing raw files
remain the verified snapshot identified by their retrieval date and hashes.

Current verification: **4 PDFs, 197 pages, 0 broken files, 0 hash mismatches**.
All pages were checked for extractable text; one bilingual Gazette cover page has no
body text and is recorded in the manifest review notes. The corpus contains public
regulatory material, not private customer records or personal health data.

## Reuse terms

IRDAI's [website policy](https://irdai.gov.in/website-policies) permits accurate
reproduction with prominent source acknowledgement, except for material identified
as third-party copyright. ClaimCompass must retain IRDAI attribution and the official
source URL whenever an extract is displayed or redistributed.

The policy and automated-access conditions were reviewed on 2026-10-23. Automated
collection is currently blocked by `robots.txt` as documented above and must remain
stopped while that rule is present. Collection must also stop if a login or CAPTCHA
is required or the website policy changes.

## File naming

The manifest is the authoritative mapping from source, publication date and title to
each local filename. The four original filenames predate this convention and remain
unchanged so their recorded hashes and references stay stable. New files should use
`irdai_YYYY-MM-DD_title.pdf`.
