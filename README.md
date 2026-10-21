Claim-Compass

IRDAI health insurance rules assistant with cost-aware AI model routing

Day 1 status: Project definition and planning. Implementation and dataset collection are in progress.

Problem
Health insurance claims executives at hospitals and third-party administrators (TPAs) must answer frequent questions about cashless authorisation, waiting periods, claim rejections, and policyholder rights. Finding the applicable rule in lengthy IRDAI regulations, master circulars, and guidelines takes time, and outdated or incorrect interpretations can affect claim handling. Using a powerful AI model for every query is costly, while using only a cheaper model can produce unreliable answers in complex or high-risk cases. ClaimCompass aims to provide source-grounded answers quickly by routing straightforward questions to a low-cost model and escalating sensitive or difficult questions to a stronger model or human reviewer.
Who it is for
- Primary user: A health insurance claims executive at a TPA office in Madurai, Tamil Nadu, who handles regulatory and claim-processing questions.
- Secondary user: A senior claims officer who reviews and approves AI-drafted responses or appeals for rejected claims.
Signature feature
Cost-aware model routing with a live INR cost meter: ClaimCompass chooses a low-cost model for straightforward IRDAI lookups and a stronger model for complex or high-risk questions, while showing which model responded, the estimated cost per answer, and supporting regulatory citations.
Hardest problem (my interview story)
The hardest challenge is reducing inference cost without compromising accuracy on important insurance questions. A simple question about a standard timeline may be handled by a fast, inexpensive model, but rejection, dispute, and exception-related questions require careful reasoning and sometimes human escalation. I will build and evaluate a lightweight question router, measure answer quality and cost against a strong-model-only baseline, and tune the routing threshold. The target is at least 60% lower average model cost per query with less than a 2-percentage-point drop in answer accuracy. High-risk outputs, including appeal drafts, will require senior officer approval before release.
Dataset
The knowledge base will use official IRDAI regulations, health insurance master circulars, guidelines, and policyholder-protection materials. The minimum target is 800+ source-document pages. Document and page counts will be updated after files are collected and verified; these are not yet completed dataset figures.
Source	Link	Documents	Pages	Licence / terms
IRDAI regulations	https://irdai.gov.in/regulations	TBD	TBD	Official public regulatory documents; verify website terms and any reuse restrictions before redistribution
IRDAI health insurance circulars and guidelines	https://irdai.gov.in/	TBD	TBD	Verify the terms for each downloaded document
Total (target)	—	TBD	800+ target	—


For each downloaded document, record its title, URL, publication/effective date, amendment or supersession status, page count, and local filename. See [DATASET.md](DATASET.md) for dataset tracking.
10 real questions
See [QUESTIONS.md](docs/QUESTIONS.md). Initial questions to include:
1. What is the maximum time allowed to decide a cashless pre-authorisation request?
2. How quickly should final cashless authorisation be issued after a discharge request?
3. What is the maximum waiting period for a disclosed pre-existing disease under the applicable rules?
4. Can a claim be rejected solely because of a pre-existing disease after 36 months of continuous coverage?
5. What must an insurer do before rejecting a health insurance claim?
6. What reasons and policy clauses must be communicated in a rejection letter?
7. What can a policyholder do when a cashless request is delayed?
8. What is the difference between cashless and reimbursement claims?
9. How should a claim executive identify which IRDAI circular applies to a claim filed on a particular date?
10. How can a policyholder challenge a rejection involving a policy exclusion or waiting period?
Answers must be grounded in the applicable IRDAI source and policy context; the system should flag uncertainty instead of guessing.

Run it
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# After an .env.example file has been added:
cp .env.example .env        # Windows: copy .env.example .env

# After the FastAPI app entry point is implemented:
uvicorn app.main:app --reload
curl http://localhost:8000/health
Day 1 note: These are the intended development commands. The app entry point, environment template, and health endpoint must exist before the full run sequence will work. Do not commit API keys or .env files.
Live link
Not deployed yet — planned for Week 2.
