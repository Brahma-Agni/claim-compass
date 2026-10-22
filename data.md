# ClaimCompass data strategy

ClaimCompass depends on trustworthy, version-aware source data. A confident answer based on an outdated rule is worse than returning no answer, so documents must be collected, verified, and tracked before they are chunked or embedded.

## 1. Data sources and authority

Use sources in this order:

| Tier | Source | Use |
|---|---|---|
| 1 | IRDAI regulations, gazette notifications, master circulars, and amendments | Primary evidence for answers |
| 2 | IRDAI FAQs and official clarifications | Supporting explanation; do not use in place of a controlling Tier 1 source |
| 3 | Insurer policy wording, schedules, and endorsements | Required for insurer-, product-, or policy-specific questions |
| 4 | IRDAI press releases and consumer guides | Background and discovery only |
| Excluded | Blogs, news reports, and insurance aggregator summaries | Never use as final evidence |

Initial official sources:

- [IRDAI consolidated regulations](https://irdai.gov.in/consolidated-gazette-notified-regulations)
- [IRDAI circulars](https://irdai.gov.in/circulars)
- [IRDAI Health Department FAQs](https://irdai.gov.in/health-dept)
- IRDAI (Insurance Products) Regulations, 2024
- Master Circular on Health Insurance Business dated 29 May 2024, reference `IRDAI/HLT/CIR/PRO/84/5/2024`
- IRDAI (Protection of Policyholders' Interests, Operations and Allied Matters of Insurers) Regulations, 2024
- Master Circular on Protection of Policyholders' Interests dated 5 September 2024, reference `IRDAI/PP&GR/CIR/MISC/117/9/2024`
- Applicable amendments and older rules needed to answer historical-date questions

The team must verify every title, reference number, effective date, status, and source URL against the official IRDAI website when the document is collected.

## 2. Version and lifecycle tracking

Do not use publication date as the only date. Each document must record:

- publication date;
- effective-from date;
- effective-to or withdrawal date;
- active, archived, withdrawn, draft, or superseded status;
- documents that it supersedes;
- documents that amend or supersede it;
- source URL and retrieval date;
- file checksum.

Drafts and exposure drafts must never be mixed with enforceable regulations. Historical documents may remain searchable, but retrieval must filter them using the date relevant to the user's question.

Example document record:

```json
{
  "document_id": "irdai-hlt-cir-pro-84-5-2024",
  "title": "Master Circular on Health Insurance Business",
  "reference_number": "IRDAI/HLT/CIR/PRO/84/5/2024",
  "document_type": "master_circular",
  "authority": "IRDAI",
  "publication_date": "2024-05-29",
  "effective_from": "2024-05-29",
  "effective_to": null,
  "status": "active",
  "supersedes": [],
  "amended_by": [],
  "language": "en",
  "source_url": "official IRDAI document URL",
  "page_count": null,
  "sha256": "checksum of the original file",
  "retrieved_at": "YYYY-MM-DD"
}
```

Values in this example must be verified before ingestion.

## 3. Storage layout

```text
data/
|-- manifest.csv
|-- raw/
|   `-- irdai/
|-- extracted/
|   |-- text/
|   `-- tables/
|-- normalized/
|-- chunks/
|-- rejected/
`-- sample/
eval/
|-- questions.jsonl
`-- expected_citations.jsonl
tests/
`-- fixtures/
```

- `data/raw/` contains immutable original downloads and is not committed.
- `data/manifest.csv` is the committed source registry.
- `data/extracted/` contains page-aware extracted text and tables.
- `data/normalized/` contains cleaned text that remains traceable to raw pages.
- `data/chunks/` contains generated chunk records ready for indexing.
- `data/rejected/` contains corrupt, duplicate, unsupported, or failed-OCR files with rejection reasons.
- `data/sample/` contains two or three legally redistributable samples or small extracted fixtures.
- `eval/` contains citation-verified evaluation cases.

Never overwrite a raw file. If a source changes, save the new file as a new version, calculate a new checksum, and update the manifest relationship.

## 4. Manifest fields

`data/manifest.csv` should contain at least:

```text
document_id,title,reference_number,document_type,authority,
publication_date,effective_from,effective_to,status,language,
source_url,local_filename,page_count,sha256,retrieved_at,
supersedes,amended_by,licence_notes,ingestion_status,review_notes
```

Document IDs should be stable and readable. Use the official reference number when available, normalized to lowercase with punctuation replaced by hyphens.

## 5. Extraction requirements

Every extracted block must preserve:

- source document ID;
- PDF page number;
- printed page number, when different;
- heading hierarchy;
- regulation, clause, or sub-clause number;
- annexure number;
- table identity and structure;
- footnotes;
- language.

Extraction must account for:

- scanned pages that require OCR;
- Hindi and English appearing together;
- broken Unicode and joined words;
- repeating headers and footers;
- two-column layouts;
- tables that lose row and column relationships;
- different PDF and printed page numbers;
- headings that occur on a page before their content;
- image-only or digitally signed gazette documents.

Flag a document for manual review when:

- more than 10% of its pages have almost no extracted text;
- replacement characters such as `�` appear repeatedly;
- expected clause sequences disappear;
- extracted and manifest page counts differ;
- a meaningful table cannot be reconstructed.

## 6. Normalization

Normalization may remove repeated headers, repeated footers, and accidental whitespace, but it must not change legal wording. Keep both the original extracted text and normalized text so that every chunk can be audited.

Do not silently:

- rewrite dates or monetary values;
- expand abbreviations inside quoted source text;
- merge clauses from different pages without page metadata;
- translate source text and treat the translation as authoritative;
- remove provisos, exceptions, notes, or footnotes.

## 7. Chunking strategy

Chunk by legal structure rather than only by token count. Apply this order:

1. regulation or clause;
2. sub-clause;
3. heading-defined section;
4. page boundary;
5. token limit.

Initial parameters to evaluate:

- target size: 400-700 tokens;
- maximum size: about 900 tokens;
- overlap: 50-100 tokens;
- do not overlap into an unrelated section;
- include the complete heading path in each chunk;
- keep definitions near rules that depend on them where possible;
- keep small tables intact;
- split large tables by logical row groups while repeating column headers.

These values are starting points, not fixed requirements. Final values must be selected using retrieval evaluation.

Example chunk:

```json
{
  "chunk_id": "irdai-hlt-cir-pro-84-5-2024:p12:c4.2",
  "document_id": "irdai-hlt-cir-pro-84-5-2024",
  "page_start": 12,
  "page_end": 13,
  "printed_page_start": 9,
  "heading_path": ["Claims procedure", "Cashless authorization"],
  "clause_number": "4.2",
  "text": "Full clause text...",
  "document_type": "master_circular",
  "authority_level": 1,
  "effective_from": "2024-05-29",
  "effective_to": null,
  "status": "active",
  "language": "en",
  "source_url": "official URL",
  "content_hash": "hash of normalized chunk text"
}
```

Chunk IDs must be deterministic so reprocessing updates existing records instead of creating duplicates.

## 8. Vectorization and retrieval

Store the chunk text, embedding, and metadata separately. Record the embedding model name and version for each indexing run so the index can be rebuilt reproducibly.

Vector search alone is not enough for legal material because questions may depend on exact reference numbers, clauses, dates, and abbreviations. Use hybrid retrieval:

```text
question
  -> detect intent and relevant date
  -> filter by lifecycle and source metadata
  -> keyword/BM25 search plus vector search
  -> rerank candidates
  -> include adjacent clauses when needed
  -> answer with document, clause, and page citations
```

Useful filters include:

- effective date range;
- active or historical status;
- document type;
- authority level;
- language;
- insurer;
- product name or UIN for policy documents.

A starting retrieval configuration can fetch 15-30 candidates, rerank them, and send the best 4-8 coherent passages to the answer model. Tune these values against the evaluation set.

## 9. Citation requirements

Citation metadata must be stored before vectorization. An embedding cannot restore a page number or clause number that was discarded during extraction.

Each answer should identify:

```text
Document title
Official reference number
Clause or regulation number
PDF page number
Effective date
Official source URL
```

The answer must also distinguish between a binding source, an IRDAI explanation, and policy wording. When sources conflict, the application should not guess; it should show the conflict or request human review.

## 10. Public and private data

The shared knowledge index is for public regulatory documents and approved public policy wording.

Claim files can contain names, policy numbers, contact details, Aadhaar information, diagnoses, medical reports, and hospital records. Do not put this information in the shared regulatory index. Private claim data requires:

- separate tenant- or case-specific storage;
- encryption in transit and at rest;
- access control;
- retention and deletion rules;
- redaction before external model calls where possible;
- audit logging;
- explicit authorization before it is used for evaluation or training.

Application logs should avoid storing full user questions by default because questions may contain personal health information.

## 11. Evaluation dataset

Each evaluation case should record the expected evidence, not only the expected prose answer:

```json
{
  "question": "What is the cashless preauthorization time limit?",
  "relevant_date": "2025-01-10",
  "expected_document_ids": ["irdai-hlt-cir-pro-84-5-2024"],
  "expected_pages": [12],
  "expected_clauses": ["4.2"],
  "answerable": true,
  "risk_level": "medium"
}
```

All illustrative page and clause values must be checked against the collected document.

Measure:

- correct document retrieval;
- correct page and clause retrieval;
- applicability on the relevant date;
- answer support from retrieved text;
- citation correctness;
- correct refusal when evidence is missing;
- correct distinction between regulations, FAQs, and policy wording.

At least 20-30% of evaluation questions should cover difficult cases such as historical rules, amendments, multi-page answers, policy-specific questions, missing evidence, and misleading assumptions.

## 12. First data milestone

Do not optimize for 800 pages immediately. Start with a small verified vertical slice:

1. Collect four to six authoritative documents.
2. Complete the manifest and document relationships.
3. Extract text while preserving pages, headings, clauses, and tables.
4. Manually inspect every page of two representative documents.
5. Produce deterministic chunks.
6. Create 10-20 questions with manually verified citations.
7. Compare keyword, vector, and hybrid retrieval.
8. Expand the corpus only after citation accuracy is acceptable.

The initial quality gate is not the number of embedded pages. It is whether ClaimCompass retrieves the controlling source, for the correct date, with an accurate page and clause citation.
