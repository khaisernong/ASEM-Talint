# UM Hackathon Domain 2 Copilot Instructions

This repository exists to build a judge-aligned decision intelligence system for UM Hackathon Domain 2.

## Mission

- Keep Z.AI GLM in the core reasoning path of the shipped product.
- Optimize for decision intelligence, not generic chat or automation.
- Treat product docs, tests, and submission artifacts as first-class outputs.

## Non-Negotiable Rules

- Do not replace runtime reasoning with a non-Z.AI model in the shipped path.
- If a fallback is needed, label it clearly as degraded or non-judge-path behavior.
- Never invent competition facts, model access, KPI values, or benchmarks.
- Mark unknown items as `UNSPECIFIED` and assumptions as `ASSUMPTION`.
- Never hardcode secrets, tokens, or private links.
- Do not automate final submission to the hackathon website.

## Architecture

- Keep business logic separate from provider clients, prompt builders, validators, and UI code.
- Prefer a provider abstraction such as `LLMProvider` with a primary `ZAIProvider` implementation.
- Treat any ILMU integration as optional and disabled by default unless organizer approval is documented.
- Keep deterministic math, KPI calculations, and rule checks in code rather than free-form model output.
- Ask the model for JSON when the next component expects machine-readable output, then validate the schema.

## Engineering

- Use environment variables for model IDs, base URLs, limits, and credentials.
- Log request status, latency, and token usage where available.
- Chunk, truncate, summarize, or reject oversized inputs before provider calls.
- Fail safely on provider, parsing, or schema-validation errors.
- Prefer server-side model calls and redact sensitive values from logs.

## Documentation And Testing

- Write for judges, not only for internal engineering use.
- Keep PRD, SAD, QATD, README, and demo narratives aligned with the actual code path.
- Include measurable KPI formulas or bounded estimates instead of invented impact claims.
- Cover happy path, invalid input, provider failure, schema failure, and AI-output contract checks.

## Completion Bar

Before calling work complete, check:

- Z.AI GLM is still central in the implementation and narrative.
- Docs, diagrams, and code still agree.
- External claims or borrowed material are flagged for citation.
- Final packaging steps remain manual and reviewable.