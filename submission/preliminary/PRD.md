# ASEM Talint Product Requirement Document (PRD)

Document version: 0.1  
Round: Preliminary  
Working status: Draft for PDF export

## 1. Project Overview

### Problem Statement

ASEM and similar talent-pipeline operators need a repeatable way to evaluate whether a candidate is ready for a semiconductor-aligned training track, what evidence supports that recommendation, what gaps remain, and whether the pathway is economically meaningful. Current manual review is slower, harder to standardize, and weaker at connecting candidate evidence to local demand, wage mobility, and access constraints.

### Target Domain

Economic empowerment and decision intelligence for semiconductor talent development in Malaysia, with an initial focus on candidate-to-track fit decisions for training and OJT pathways.

### Proposed Solution Summary

ASEM Talint combines deterministic scoring, official-data slices, resume parsing, and Z.AI GLM-based structured reasoning into a dashboard-first review workflow. The current prototype accepts a candidate profile and a target training track, computes an auditable suitability context, then asks Z.AI GLM to produce a structured recommendation, tradeoffs, pathway steps, and validation notes in JSON.

## 2. Background & Business Objective

### Background of the Problem

Malaysia's industrial direction is increasingly framed around moving from "Made in Malaysia" to "Made by Malaysia", with stronger local sourcing, vendor development, SME participation in value chains, and tighter links between investment projects, training, and research partnerships. That direction makes talent-allocation quality more important: training seats, employer partnerships, and pathway recommendations need to be evidence-based rather than purely manual.

### Importance of Solving This Issue

The product aims to help a training operator:

- reduce the friction of screening candidates against semiconductor pathways
- surface missing evidence before a human reviewer makes a placement decision
- tie readiness recommendations to labor-market context such as employer demand, accessibility, and wage uplift signals
- preserve a judge-visible AI path in which Z.AI GLM contributes structured reasoning, not opaque free-form output

### Strategic Fit / Impact

The prototype aligns with UM Hackathon Domain 2 because it treats AI as decision support for economic mobility rather than generic chat. It also aligns with the judging requirement that Z.AI be used in the reasoning path. The current measurable prototype outputs are:

- suitability score breakdown with weighted sub-scores
- confidence baseline adjusted by missing inputs
- structured recommendation, tradeoffs, and pathway steps
- official-data-backed wage and employer-demand slices
- resume extraction outcomes including warnings and PII redactions

For the preliminary round, the team can evaluate feasibility using measurable, non-invented validation formulas rather than unverified business-impact claims:

- contract-valid decision rate = decision responses parsed into the required structured contract / total live decision requests
- median live decision latency = median `usage.latency_ms` across live decision calls in the demo-ready environment
- structured resume yield = successful resume parses containing at least one structured skill tag, project, internship, or certification / total successful resume parses
- reviewer evidence completeness = 1 - (`missing_inputs` count / tracked required inputs) for a submitted request
- pathway economic uplift signal = target estimated wage - current estimated wage from the wage-mobility panel

ASSUMPTION: downstream business KPIs such as actual placement conversion, retention, and wage outcomes will be defined with ASEM or a comparable training operator after preliminary validation.

### Economic Theory Anchor

Economically, ASEM Talint is designed to reduce five linked frictions in talent allocation rather than only produce a recommendation:

- human capital allocation friction, because training seats and OJT opportunities are scarce investments
- information asymmetry and signaling friction, because resumes, certifications, and project evidence are noisy and inconsistently interpreted
- matching and search friction, because candidate quality alone does not guarantee a good track or employer match
- spatial friction, because semiconductor opportunities cluster geographically and are not equally reachable
- wage-mobility uncertainty, because pathway value depends partly on whether it plausibly improves earnings

This explains the current product structure. Candidate scoring addresses readiness, resume parsing standardizes signals, Market Studio and OJT layers address matching, accessibility panels address cluster access, wage-mobility panels address directional economic payoff, and the ERP Bridge lowers coordination costs for institutional adoption. The current prototype is therefore best described as partial-equilibrium decision support for training-path allocation, not as a causal estimator of long-run labor-market outcomes.

See the companion note at [submission/preliminary/economic-theory-anchor.md](./economic-theory-anchor.md).

## 3. Product Purpose

### 3.1 Main Goal of the System

Provide a dashboard-first decision support system that helps training operators place candidates into the most suitable semiconductor-aligned pathway with explicit evidence, constraints, and next steps.

### 3.2 Intended Users (Target Audience)

- ASEM training operations reviewers
- program leads responsible for cohort selection
- employer-partnership teams evaluating OJT fit
- judges reviewing whether the solution is technically feasible and domain-aligned

## 4. System Functionalities

### 4.1 Description

The system operates as a FastAPI application with a browser dashboard. A candidate profile and target training track are submitted to the API. The system calculates deterministic readiness signals, merges optional resume-derived evidence, and requests a structured JSON explanation from Z.AI GLM. The dashboard also exposes wage, accessibility, OJT, and wage-mobility slices so the decision is reviewed in context rather than as a standalone AI answer.

### 4.2 Key Functionalities

- Candidate-track fit decision endpoint at `POST /v1/decisions/candidate-track-fit`
- Dashboard for payload review, live decision execution, and result inspection
- Resume upload and parsing for PDF or DOCX files at `POST /v1/resumes/parse`
- OCR fallback for image-only PDFs
- Wage, employer-demand, accessibility, OJT matching, and wage-mobility endpoints
- Health route that reports whether the live Z.AI route and optional ILMU route are configured
- Degraded local demo mode for UI validation only

### 4.3 AI Model & Prompt Design

#### 4.3.1 Model Selection

The judged reasoning path uses Z.AI GLM through an OpenAI-compatible chat-completions interface. This is mandatory for judging eligibility and remains the only shipped judge-path reasoning provider. An ILMU-compatible route exists only as optional non-judge-path infrastructure.

#### 4.3.2 Prompting Strategy

The prompt strategy is structured and bounded rather than open-ended:

- a system prompt requires valid JSON only
- deterministic context is computed in code before the model call
- required response fields are listed explicitly
- the model is told not to fabricate missing values and not to emit raw chain-of-thought

#### 4.3.3 Context & Input Handling

The model receives:

- candidate data, with free-text notes truncated to a configured budget
- target-track data
- deterministic context including score breakdown, missing inputs, and top skill gaps
- optional compacted `resume_evidence` instead of the raw parsed resume object

The current prompt budgets are implementation-backed rather than aspirational:

- Z.AI completion budget defaults to `ZAI_MAX_TOKENS=1200`
- prompt note budget defaults to `PROMPT_NOTES_MAX_CHARS=1500`
- optional ILMU route uses a tighter note budget and a higher completion cap because the compatibility path required different tuning during validation

#### 4.3.4 Fallback & Failure Behavior

- if Z.AI configuration is missing, the health route reports the missing environment variables
- if the live provider fails, the API returns a `502` with a provider error rather than silently substituting a different model
- a local demo endpoint exists for dashboard validation but is explicitly labeled degraded and non-judge-path
- optional ILMU routing is disabled until its environment variables are configured and is not part of the judged runtime path

## 5. User Stories & Use Cases

| ID | User story | Acceptance signal |
| --- | --- | --- |
| US-1 | As an ASEM reviewer, I want to submit a candidate and track so I can see a structured fit recommendation. | API returns a typed response with context, explanation, and usage metadata. |
| US-2 | As a reviewer, I want missing inputs surfaced clearly so I know what evidence is absent before making a decision. | Response includes `missing_inputs` and confidence is reduced when data is missing. |
| US-3 | As an operator, I want to upload a resume instead of retyping it manually. | Resume parser extracts structured evidence, warns on truncation, and redacts contact PII in preview output. |
| US-4 | As a program lead, I want to see wage and employer-demand signals next to the recommendation. | Dashboard loads official-data-backed wage and employer-demand slices. |
| US-5 | As a judge, I want the role of Z.AI GLM to be explicit and non-optional in the shipped reasoning path. | The live decision route uses Z.AI, and degraded or optional routes are labeled separately. |

## 6. Features Included (Scope Definition)

- one candidate-to-track fit workflow
- typed request and response contracts
- deterministic scoring for suitability and missing-input handling
- Z.AI GLM structured explanation output
- optional resume evidence extracted from PDF and DOCX
- OCR fallback for image-only PDFs
- dashboard panels for decision review and market context
- fixture-backed official-data slices for wages, hotspots, and employer demand
- optional ILMU compatibility route kept outside the judge path

## 7. Features Not Included (Scope Control)

- multi-tenant account management
- production authentication and role-based access control
- persistent reviewer case management database
- automated final submission to the UMHackathon website
- full admissions workflow, cohort scheduling, or CRM integration
- generalized chatbot interface
- unsupported replacement of the judge-path Z.AI provider with another reasoning model

## 8. Assumptions & Constraints

### Assumptions

- ASSUMPTION: the preliminary pitching environment will have an authorized Z.AI key and model for the final recorded demonstration.
- ASSUMPTION: the public repository URL will be available before final packaging; the current public URL is `UNSPECIFIED`.

### Operational Constraints

- The current prototype evaluates one training-path fit workflow only.
- The current official-data layer uses normalized local CSV slices rather than a production database.
- Real ASEM internal schemas and deployment targets remain `UNSPECIFIED`.
- The submission workflow allows one final official website submission attempt only.

### Cost and Performance Constraints

- Model calls should remain server-side and credentialed through environment variables rather than client-side secrets.
- Prompt and completion budgets are deliberately bounded, with `PROMPT_NOTES_MAX_CHARS` and `ZAI_MAX_TOKENS` limiting request size and output volume.
- Provider timeout is bounded by `ZAI_TIMEOUT_SECONDS`, which defaults to 30 seconds in the current implementation.
- Resume uploads are capped at 2,000,000 bytes, and parsed text is truncated to a bounded processing window before structured extraction.
- If the live judged route fails, the system must fail visibly rather than silently substitute a non-Z.AI reasoning provider.

## 9. Risks & Questions Throughout Development

- Z.AI authentication or quota issues can block the live judged path if not validated before recording and submission.
- Model outputs can be malformed, truncated, or empty if token budgets are misconfigured.
- Resume OCR quality can degrade on low-quality scans or handwriting.
- Official-data slices can become stale if ingestion refreshes are not run before packaging evidence.
- The public GitHub link remains `UNSPECIFIED` until the team finalizes what can be shared publicly.
- Open questions around production deployment, reviewer workflow persistence, and cohort-level analytics remain `UNSPECIFIED` for the preliminary round.

## References

- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [UMHackathon2026 Product Requirement Documentation (Sample)](../../UMHackathon2026%20Product%20Requirement%20Documentation%20%28Sample%29.pdf)
- [UMHackathon2026 Judging Criteria](../../UMHackathon2026%20Judging%20Criteria.pdf)
- [Shift to 'Made by Malaysia' strategy, New Straits Times, 5 Feb 2026](https://www.nst.com.my/news/nation/2026/02/1371466/shift-made-malaysia-strategy)
- [Project README](../../README.md)

