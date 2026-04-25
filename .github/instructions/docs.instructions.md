---
description: "Use when drafting or editing hackathon-facing docs such as PRD, SAD, QATD, README, submission notes, demo scripts, or pitch content. Enforces judge alignment, citation hygiene, and Z.AI GLM centrality."
name: "UM Hackathon Docs"
applyTo: "README.md, docs/**/*.md, docs/**/*.mdx, submission/**/*.md"
---

# Judge-Facing Documentation Rules

- Write for UM Hackathon judges, not only for maintainers.
- State the target user, business problem, measurable impact, and MVP scope early.
- Make the Z.AI GLM role explicit whenever the product, architecture, or demo is described.
- Mark gaps as `UNSPECIFIED` and assumptions as `ASSUMPTION`.
- Do not leave unsupported claims, fake metrics, or placeholder prose unmarked.
- Keep citations visible for external facts, templates, datasets, or reused ideas.

# Required Angles By Artifact

- PRD: problem, user, business objective, why Z.AI GLM is required, prompting strategy, fallback behavior, cost and performance constraints.
- SAD: concrete architecture, prompt construction, context handling, token limits, response parsing, schema validation, core sequence flow.
- QATD: traceability, 5x5 risk matrix, execution strategy, quality gates, happy path, negative path, NFR coverage, AI-output validation.
- README: setup, environment variables, demo flow, tests, architecture summary, compliance note, KPI framing, limitations.

# Style

- Prefer specific evidence over slogans.
- Keep explanations concise enough to present in a pitch.
- Make it obvious how the implementation would be judged.