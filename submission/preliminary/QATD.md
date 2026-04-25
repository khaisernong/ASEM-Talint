# ASEM Talint Quality Assurance Testing Document (QATD)

Document version: 0.1  
Round: Preliminary  
Working status: Draft for PDF export

## Document Control

| Field | Detail |
| --- | --- |
| System Under Test (SUT) | ASEM Talint |
| Team Repo URL | https://github.com/khaisernong/ASEM-Talint |
| Project Board URL | `UNSPECIFIED` |
| Live Deployment URL | Local validation instance at `http://127.0.0.1:8001`; public deployment URL is `UNSPECIFIED` |
| Objective | Validate that the prototype can produce a structured candidate-track recommendation, handle malformed inputs safely, preserve Z.AI as the judged reasoning path, and expose enough market and resume evidence to support a feasibility review. |

## PRELIMINARY ROUND (Test Strategy & Planning)

## 1. Scope & Requirements Traceability

This section maps the current product requirements to concrete validation evidence.

### 1.1 In-Scope Core Features

- live candidate-track fit decision endpoint
- dashboard availability and decision review surface
- degraded demo route labeled as non-judge-path
- resume parsing for PDF and DOCX uploads
- OCR fallback for image-only PDFs
- market-signal endpoints for wages, employer demand, accessibility, OJT, and wage mobility
- optional ILMU compatibility route outside the judge path

### 1.2 Out-of-Scope

- production authentication and authorization
- persistent reviewer workflow management
- public cloud deployment hardening
- final website submission automation

### 1.3 Requirements Traceability Matrix

| Requirement ID | Requirement | Evidence |
| --- | --- | --- |
| FR-1 | System returns a typed decision result for a valid candidate-track payload. | Integration tests for `/v1/decisions/candidate-track-fit` and `/v1/decisions/candidate-track-fit/ilmu`. |
| FR-2 | Invalid decision payloads are rejected safely. | Integration test expects `422` on incomplete payloads. |
| FR-3 | Dashboard HTML exposes the review surface and route options. | Integration test checks dashboard content and labels. |
| FR-4 | Health route reports missing provider configuration clearly. | Integration test checks readiness flags and missing environment-variable messages. |
| FR-5 | Resume parser extracts structured evidence and supports OCR fallback. | Unit tests cover DOCX extraction, PDF extraction, OCR fallback, and oversize rejection. |
| FR-6 | Model outputs must satisfy a strict JSON contract. | Unit tests validate parse success, invalid contract failure, fenced JSON handling, and retry after malformed payloads. |

## 2. Risk Assessment & Mitigation Strategy

Risk score uses the sample-document formula: `Risk Score = Likelihood x Severity`.

| Technical Risk | Likelihood (1-5) | Severity (1-5) | Risk Score | Mitigation Strategy | Testing Approach |
| --- | --- | --- | --- | --- | --- |
| Z.AI authentication failure blocks the judged live path. | 4 | 5 | 20 | Validate `/health` and a live call before recording the pitch video; do not silently swap in another reasoning model. | Manual live-call check plus provider-error-path validation. |
| Provider returns malformed, fenced, truncated, or empty JSON. | 4 | 4 | 16 | Enforce JSON response format, validate against `DecisionExplanation`, clean fenced JSON, retry malformed payloads, and return `502` on failure. | Unit tests for invalid contract, fenced JSON, null content, and retry behavior. |
| Resume PDF has no extractable text. | 3 | 4 | 12 | Use OCR fallback when direct text is too weak and surface parser warnings. | Unit tests for OCR fallback path. |
| Oversized uploads or invalid file types disrupt review flow. | 3 | 3 | 9 | Enforce file-size cap and supported extensions at the API boundary. | Unit tests for oversize rejection and resume-parse error handling. |
| Official-data slices are stale or incomplete. | 3 | 3 | 9 | Keep ingestion sources explicit, preserve source manifest, and avoid unsupported claims about coverage. | Manual refresh check of data files plus route-level sanity inspection. |
| Missing candidate inputs reduce decision reliability. | 4 | 3 | 12 | Surface `missing_inputs`, lower confidence baseline, and avoid fabricating missing values. | Integration and provider tests inspect missing-input handling and contract fields. |

### Risk Assessment Scoring Criteria

| Likelihood | Meaning |
| --- | --- |
| 1 | Rare |
| 2 | Unlikely |
| 3 | Possible |
| 4 | Likely |
| 5 | Almost Certain |

| Severity | Meaning |
| --- | --- |
| 1 | Negligible impact |
| 2 | Minor impact |
| 3 | Moderate impact |
| 4 | Major impact |
| 5 | Critical failure |

## 3. Test Environment & Execution Strategy

| Area | Current approach |
| --- | --- |
| Runtime | Local Python virtual environment |
| API validation | FastAPI `TestClient` integration tests |
| Unit validation | `pytest` unit tests for prompt building, provider parsing, and resume parsing |
| Dashboard validation | Manual browser checks against local `uvicorn` server |
| Provider simulation | Fake or recording HTTP clients in unit tests |
| Test data | Synthetic candidate fixtures plus local official-data CSV slices |

Execution strategy for the preliminary round:

- run targeted unit and integration tests before packaging
- recheck `/health` in the exact environment used for the recorded demo
- verify that the live judged route is Z.AI-backed and not replaced by the optional ILMU or demo route
- verify that resume parsing and market panels still load in the dashboard

## 4. CI/CD Release Thresholds & Automation Gates

### 4.1 Integration Thresholds (Merging to Main)

- all targeted `pytest` suites must pass
- no known failing tests on the core decision workflow
- dashboard HTML must still expose the judged and degraded route labels clearly
- provider-contract tests must pass before accepting prompt or parser changes

### 4.2 Deployment Thresholds (Pushing to Production)

Production deployment gates are `UNSPECIFIED` because the repository currently validates through local and test execution rather than a published production pipeline.

For preliminary packaging, the practical release gate is:

- all local validation steps pass
- citations are present in submission artifacts
- public repository readiness is reviewed manually
- final website submission is performed manually once only

## 5. Test Case Specifications (Drafts)

| Test ID | Scenario | Expected Result | Evidence Type |
| --- | --- | --- | --- |
| TC-01 | Submit a valid candidate-track payload to the live decision route. | API returns `200` with typed context, explanation, and usage fields. | Integration test |
| TC-02 | Submit an invalid decision payload missing required fields. | API returns `422` validation failure. | Integration test |
| TC-03 | Load the dashboard root. | HTML contains dashboard title, route buttons, resume-intake controls, and national-strategy note. | Integration test plus manual browser check |
| TC-04 | Parse a DOCX resume containing project, internship, and certification text. | Structured `resume_context` is returned and contact PII is redacted from preview output. | Unit test |
| TC-05 | Parse an image-only PDF resume. | OCR fallback runs and parser returns structured evidence plus warning. | Unit test |
| TC-06 | Parse a malformed provider payload missing required explanation fields. | Provider validation raises a controlled error and the API surfaces a provider failure rather than invalid data. | Unit test |
| TC-07 | Receive fenced JSON from the optional compatibility provider. | Parser strips fences and validates the structured contract. | Unit test |

## 6. AI Output & Boundary Testing (Drafts)

### 6.1 Prompt/Response Contract Checks

The AI-output checks focus on whether the provider response can be trusted by the next component, not only whether the text sounds plausible. Current validation checks include:

- valid JSON object output
- required explanation keys populated
- model output can be parsed into `DecisionExplanation`
- empty assistant content becomes a clear provider error
- fenced JSON can be cleaned safely

### 6.2 Oversized / Larger Input Test

- resume uploads above the byte limit are rejected
- free-text notes are truncated before provider calls
- resume summaries and detail fields are compacted before prompt construction

### 6.3 Adversarial / Edge Prompt Test

- missing candidate scores should not be hallucinated into concrete values
- invalid provider payloads should fail closed instead of being passed through
- optional compatibility-provider behavior must not be described as the judged runtime path

### 6.4 Hallucination Handling

The system prompt explicitly instructs the model not to fabricate missing values. Deterministic scoring surfaces `missing_inputs`, and the output contract requires those fields to remain visible in the explanation. This keeps the prototype closer to an auditable decision-support tool than a free-form assistant.

## 7. Test Strategy & Plan Sign-Off

Preliminary-round sign-off owner, date, and approval chain are `UNSPECIFIED` and should be completed before PDF export.

## References

- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [UMHakcathon2026 Sample Testing Analysis Documentation (Preliminary)](../../UMHakcathon2026%20Sample%20Testing%20Analysis%20Documentation%20%28Preliminary%29.pdf)
- [UMHackathon2026 Judging Criteria](../../UMHackathon2026%20Judging%20Criteria.pdf)
- [Hackathon QA Instructions](../../.github/instructions/qa.instructions.md)
- [Integration tests for decision API](../../tests/integration/test_decision_api.py)
