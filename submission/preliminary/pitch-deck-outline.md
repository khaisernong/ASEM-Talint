# Preliminary Round Pitch Deck Outline

Deck status: Draft  
Target length: 10 minutes  
Recommended slide count: 11

## Slide 1. Title, Team, and One-Sentence Thesis

### Objective

State the product clearly in one sentence.

### Core message

ASEM Talint is a dashboard-first semiconductor talent decision system that combines deterministic readiness scoring, official market signals, resume evidence, and Z.AI GLM-based structured reasoning.

### On-screen proof

- product name
- team name and members
- short thesis sentence

## Slide 2. Domain Problem and Why It Matters

### Objective

Show domain-problem fit, not just technical ambition.

### Core message

- candidate-to-track decisions are hard to standardize
- manual review misses missing inputs, labor-market context, and readiness tradeoffs
- Malaysia's "Made by Malaysia" direction increases the need for talent decisions tied to local value creation and industry pathways
- pathway decisions should be defendable in economic as well as technical terms

### On-screen proof

- problem statement
- short policy-context citation
- pain points for reviewer workflow

## Slide 3. Economic Theory: What Friction We Reduce

### Objective

Anchor the product in economic logic, not only product features.

### Core message

- human capital allocation: scarce training seats should be assigned more deliberately
- signaling and information asymmetry: resumes and credentials are noisy signals that need structured interpretation
- search and matching frictions: the goal is candidate-pathway-employer fit, not raw ranking
- spatial and wage frictions: a role is not truly attractive if access and economic payoff are weak

### On-screen proof

- one simple friction map
- one line connecting each friction to a current product feature

## Slide 4. Users, User Stories, and Decision Workflow

### Objective

Make target users concrete.

### Core message

- primary user: training reviewer or program lead
- supporting user: employer-partnership or OJT reviewer
- decision flow: ingest candidate evidence, compute fit, inspect pathway and labor-market context, decide next action

### On-screen proof

- 2-3 user stories from the PRD
- one simple workflow diagram

## Slide 5. Product Overview and MVP Scope

### Objective

Demonstrate feature prioritization and MVP discipline.

### Core message

- one candidate-to-track fit workflow
- resume parsing with OCR fallback
- market-signal panels for wages, employer demand, accessibility, and wage mobility
- explicit degraded demo route for UI validation only

### On-screen proof

- dashboard screenshot using [assets/dashboard-gis-accessibility-panel.png](./assets/dashboard-gis-accessibility-panel.png) or an updated full-dashboard capture
- MVP in-scope versus out-of-scope list

## Slide 6. Why Z.AI GLM Is Central

### Objective

Address judging eligibility and technical intent directly.

### Core message

- Z.AI GLM is the judged reasoning path
- deterministic logic remains in code
- the model produces structured explanation JSON, not opaque free-form output
- optional ILMU compatibility exists but is not the judge path

### On-screen proof

- architecture snippet showing provider boundary
- one bullet on prompt contract
- one bullet on failure behavior with no silent model substitution

## Slide 7. System Architecture and Feasibility

### Objective

Cover system logic, architecture, and workflow integration.

### Core message

- FastAPI app serves dashboard, decision API, resume API, and market-signal API
- scoring weights and missing-input logic are deterministic
- provider client calls Z.AI through an OpenAI-compatible interface
- official-data slices are normalized locally for preliminary feasibility

### On-screen proof

- high-level architecture diagram
- sequence flow from request to decision response

## Slide 8. Live Demo Walkthrough

### Objective

Show the prototype rather than only talk about it.

### Core message

- load the dashboard
- parse a resume into structured evidence
- refresh market panels, including the cleaned GIS accessibility figure
- run the live Z.AI decision route
- inspect recommendation, missing inputs, and pathway steps

### On-screen proof

- actual dashboard interaction
- numbered hotspot figure plus ranked accessibility list, with [assets/dashboard-gis-accessibility-panel.png](./assets/dashboard-gis-accessibility-panel.png) available as the fallback still image
- health route showing Z.AI ready before demo call

## Slide 9. Engineering Quality and QA Evidence

### Objective

Answer code-quality and testing-feasibility criteria.

### Core message

- typed models and explicit provider boundaries keep the system modular
- tests cover happy path, invalid payloads, provider contract failures, fenced JSON, and OCR fallback
- parser warnings and provider usage metrics improve observability

### On-screen proof

- short test summary
- examples of controlled failure handling

## Slide 10. Product Feasibility, Risks, and Next Expansion

### Objective

Show the team understands limitations and a credible next step.

### Core message

- current prototype is feasible for preliminary validation
- production persistence, reviewer workflow management, and full analytics remain `UNSPECIFIED`
- main near-term risks are live-provider readiness, data refresh discipline, and public packaging quality

### On-screen proof

- one risk table or roadmap graphic
- one note on what is intentionally not claimed yet

## Slide 11. Closing and Submission Readiness

### Objective

End with clarity and control.

### Core message

- the solution fits Domain 2 because it supports economically meaningful pathway decisions
- Z.AI GLM remains central to the shipped reasoning path
- the submission pack includes PRD, SAD, QATD, repository, pitch deck, and demo video

### On-screen proof

- closing summary
- QR code or public repository link when finalized
- citation footer

## Timing Guide

| Segment | Time |
| --- | --- |
| Slides 1-3 | 2:30 |
| Slides 4-7 | 3:00 |
| Slide 8 live demo | 2:30 |
| Slides 9-11 | 2:00 |

## Deck Construction Notes

- keep citations visible on slides that reference policy, handbook rules, or external data
- do not present the optional ILMU route or degraded demo route as the judged runtime path
- do not claim production-scale impact metrics unless the value is verified; otherwise mark it `UNSPECIFIED` or as an `ASSUMPTION`
- show at least one repository or test artifact to support code-quality claims

## References

- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [UMHackathon2026 Judging Criteria](../../UMHackathon2026%20Judging%20Criteria.pdf)
- [Economic theory anchor](./economic-theory-anchor.md)
- [PRD draft](./PRD.md)
- [SAD draft](./SAD.md)
- [QATD draft](./QATD.md)
