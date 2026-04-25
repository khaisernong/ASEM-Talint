# Preliminary Round Pitch Deck Script

Deck status: Draft  
Target runtime: 10 minutes  
Intended output: speaker notes and slide-copy source for the final deck

## Slide 1. ASEM Talint

### On-slide copy

- Dashboard-first semiconductor talent decision intelligence
- Deterministic scoring plus Z.AI GLM structured reasoning
- Built for training-path fit, evidence review, and market-context visibility

### Speaker notes

We built ASEM Talint to help training operators make auditable decisions about who should enter a semiconductor-aligned pathway and what support they need next. The product is not a generic chatbot. It combines deterministic scoring, official market signals, resume evidence, and Z.AI GLM-generated structured explanation inside one review dashboard.

### Visual suggestion

- product title
- team name and members
- one dashboard screenshot hero image

## Slide 2. Problem: Placement Decisions Are Still Fragmented

### On-slide copy

- candidate readiness is reviewed manually and inconsistently
- missing inputs, access constraints, and labor-market context are often separated
- pathway decisions should connect training to real economic outcomes

### Speaker notes

The core problem is not just ranking candidates. Training operators need to know whether a candidate is ready, what evidence is missing, whether the pathway is geographically and economically sensible, and what next step is justified. Today, those signals are often scattered across manual documents, resume review, and disconnected labor-market data.

### Suggested citation footer

- UMHackathon Domain 2 brief
- UMHackathon 2026 Judging Criteria

## Slide 3. Economic Theory: What Friction We Reduce

### On-slide copy

- human capital allocation for scarce training seats
- signaling under information asymmetry from resumes and credentials
- search and matching frictions across candidate, track, and employer
- spatial and wage frictions across access and economic payoff

### Speaker notes

Economically, ASEM Talint is addressing several frictions at once rather than only automating a form. Training seats are scarce, so this is a human-capital allocation problem. Resumes and credentials are noisy signals, so this is also an information-asymmetry and signaling problem. Candidate quality alone does not guarantee a good path or employer outcome, so this is a matching problem. And because semiconductor opportunities cluster geographically and differ in wage potential, this is also a spatial-friction and mobility problem. Our current product layers map directly to those frictions: scoring for screening, resume parsing for signals, Market Studio and OJT matching for fit, accessibility for cluster access, wage mobility for directional economic payoff, and ERP Bridge for lower coordination cost.

### Visual suggestion

- one friction-to-feature diagram
- labels connecting scoring, resume parsing, matching, accessibility, wage mobility, and ERP Bridge

## Slide 4. Why This Matters in Malaysia Now

### On-slide copy

- "Made by Malaysia" raises the bar for local value creation
- talent pathways need stronger links to vendors, SMEs, and industry demand
- training decisions should be explainable, evidence-backed, and fast

### Speaker notes

Malaysia's industrial direction is increasingly framed around "Made by Malaysia", which emphasizes local sourcing, vendor development, SME participation in value chains, and stronger connections between investment and capability building. That means talent-allocation decisions need to be more deliberate. Our product treats candidate placement as a decision-intelligence problem tied to economic mobility rather than an administrative checklist.

### Suggested citation footer

- New Straits Times, 5 Feb 2026, "Shift to 'Made by Malaysia' strategy"

## Slide 5. User and Decision Workflow

### On-slide copy

- primary user: training reviewer or program lead
- secondary user: employer-partnership or OJT reviewer
- workflow: ingest evidence, score fit, inspect context, choose next action

### Speaker notes

Our primary user is the training reviewer who needs to decide whether a candidate fits a specific pathway. A supporting user is the employer-partnership team that wants to see whether the pathway aligns with OJT and wage outcomes. The workflow is simple: submit candidate and track data, enrich with resume evidence, compute deterministic fit, review market context, and then inspect the structured recommendation.

### Visual suggestion

- three-step workflow graphic
- one user-story callout from the PRD

## Slide 6. MVP Scope

### On-slide copy

- one candidate-to-track fit workflow
- resume parsing for PDF and DOCX with OCR fallback
- wage, employer-demand, accessibility, OJT, and wage-mobility panels
- degraded local demo route clearly separated from judged flow

### Speaker notes

We kept the MVP narrow on purpose. The preliminary-round prototype focuses on one decision workflow and the evidence around it. That gives judges something concrete and testable instead of a broad but shallow platform claim. We explicitly separate what is shipped now from what remains out of scope, such as production authentication, reviewer case management, and full operational analytics.

### Visual suggestion

- in-scope versus out-of-scope panel
- screenshot with dashboard sections highlighted

## Slide 7. Why Z.AI GLM Is Central

### On-slide copy

- Z.AI GLM is the judged reasoning path
- deterministic scoring stays in code
- model output is constrained to structured JSON
- no silent replacement with another reasoning model

### Speaker notes

This slide is important for judging eligibility. Z.AI GLM is not an optional plugin in our design. It is the reasoning model in the shipped judge path. We keep weights, thresholds, missing-input handling, and confidence baselines in code, then use Z.AI GLM to generate the structured recommendation and explanation. An optional ILMU compatibility route exists, but it is clearly outside the judged path.

### Visual suggestion

- architecture snippet showing scoring, prompt builder, Z.AI provider, and validated response contract

## Slide 8. System Architecture and Feasibility

### On-slide copy

- FastAPI app serves dashboard, decision routes, resume routes, and market routes
- typed models and provider abstraction keep the system modular
- prompt budgets, token budgets, and upload limits are enforced
- official-data slices are normalized locally for preliminary feasibility

### Speaker notes

Technically, the system is straightforward and defensible. The app is built in FastAPI, with typed request and response models. The decision engine computes deterministic context first, the prompt builder packages bounded JSON evidence, and the provider validates the model response before it reaches the API consumer. Resume intake and market-signal routes sit beside that core flow rather than being bolted on later.

That architecture also matches the economics. Deterministic scoring handles the screening problem, market and OJT services handle the matching problem, accessibility handles spatial friction, and the ERP Bridge reduces coordination cost when institutions want to operationalize the result in their own systems.

### Visual suggestion

- one high-level architecture diagram
- one short sequence diagram for candidate-track fit

## Slide 9. Live Demo

### On-slide copy

- parse resume into structured evidence
- refresh market panels
- pause on the GIS accessibility figure and ranked hotspot list
- run live Z.AI decision route
- inspect recommendation, tradeoffs, and missing inputs

### Speaker notes

During the live demo, we will show the dashboard starting from the sample candidate payload. Then we will apply resume evidence, refresh the wage and employer-demand context, and pause on the GIS accessibility panel. That panel now uses compact numbered hotspot markers with a separate ranked list underneath, so judges can read the spatial evidence clearly instead of parsing overlapping labels. After that, we run the live Z.AI route. The goal is to show that the prototype does not just produce a recommendation, but also explains what drove it and what remains uncertain.

### Demo checklist on slide or presenter view

1. Show `/health` or runtime-ready status.
2. Parse and apply resume.
3. Refresh market panels.
4. Show the numbered accessibility figure and ranked hotspot list, or use [assets/dashboard-gis-accessibility-panel.png](./assets/dashboard-gis-accessibility-panel.png) if a still image is needed in the deck.
5. Run live Z.AI decision.
6. Open recommendation and raw structured response.

## Slide 10. Engineering Quality and Risk Control

### On-slide copy

- tests cover happy path, invalid input, OCR fallback, and provider contract failures
- provider output is validated before use
- malformed or empty model output fails visibly
- risks are identified with mitigation, not hidden

### Speaker notes

We wanted the judges to see that this is an engineering build, not only a prompt demo. The repository includes integration tests for the decision flow and health behavior, unit tests for prompt construction and provider parsing, and parser tests for OCR fallback and upload constraints. That gives us a clear quality story for the preliminary round while staying honest about what is still `UNSPECIFIED`.

### Visual suggestion

- short test-results strip
- one risk table excerpt from the QATD

## Slide 11. Feasibility, Honesty, and Submission Readiness

### On-slide copy

- feasible prototype for Domain 2 decision intelligence
- Z.AI GLM remains central in product, architecture, and demo
- PRD, SAD, QATD, repository, deck, and video are submission-ready in structure

### Speaker notes

Our claim is not that this is already a full production platform. Our claim is that the prototype is technically coherent, domain-fit, and feasible to extend. We are explicit about what is already working, what depends on the judged Z.AI path, and what remains `UNSPECIFIED`. That makes the submission stronger and more credible for the preliminary round.

### Closing line

ASEM Talint turns candidate placement from a manual review task into an auditable, market-aware, Z.AI-centered decision workflow.

## Presenter Notes

- keep the total spoken delivery under 10 minutes
- if the live Z.AI route is not ready, do not substitute the optional ILMU route and describe it as equivalent
- keep citations visible on slides that reference the handbook, judging criteria, or the NST article
- avoid unsupported adoption or ROI claims; use the PRD evaluation formulas instead of invented outcome metrics

## References

- [Pitch deck outline](./pitch-deck-outline.md)
- [PRD draft](./PRD.md)
- [Economic theory anchor](./economic-theory-anchor.md)
- [SAD draft](./SAD.md)
- [QATD draft](./QATD.md)
- [Video demo runbook](./video-demo-runbook.md)
- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [UMHackathon2026 Judging Criteria](../../UMHackathon2026%20Judging%20Criteria.pdf)
- [Shift to 'Made by Malaysia' strategy, New Straits Times, 5 Feb 2026](https://www.nst.com.my/news/nation/2026/02/1371466/shift-made-malaysia-strategy)