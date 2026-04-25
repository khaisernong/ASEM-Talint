---
description: "Use when writing or reviewing tests, QA documents, risk analysis, acceptance criteria, or CI quality gates for the UM Hackathon project. Covers AI-output validation and submission-ready evidence."
name: "Hackathon QA"
applyTo: "tests/**, .github/workflows/**, **/*test*.ts, **/*test*.tsx, **/*test*.js, **/*test*.py, **/*spec*.ts, **/*spec*.tsx, **/*spec*.js, **/*spec*.py"
---

# QA Priorities

- Cover one end-to-end happy path for the core decision workflow.
- Cover invalid input, missing data, provider failure, and schema-validation failure.
- Add at least one non-functional check for latency, payload size, or token usage when practical.
- Include AI-output contract checks for valid JSON, required keys, populated explanation fields, and graceful degradation on missing inputs.

# Evidence Expectations

- Keep tests traceable to requirements or user stories.
- Surface risks with severity and mitigation, not only pass/fail results.
- Prefer reproducible checks over manual claims.
- Keep CI focused on build, lint, tests, and artifact packaging, not final website submission.