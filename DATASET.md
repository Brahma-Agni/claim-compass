# Dataset

The first verified corpus contains 197 pages from four official IRDAI documents.
The immutable PDFs live in `data/raw/irdai/` and are intentionally not committed.
Checksums and lifecycle metadata are recorded in `data/manifest.csv`.

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

## Reuse terms

IRDAI's [website policy](https://irdai.gov.in/website-policies) permits accurate
reproduction with prominent source acknowledgement, except for material identified
as third-party copyright. ClaimCompass must retain IRDAI attribution and the official
source URL whenever an extract is displayed or redistributed.
