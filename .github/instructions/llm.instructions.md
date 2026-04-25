---
description: "Use when creating or editing LLM provider code, decision engine logic, prompt builders, schema validators, or model-facing configuration. Covers Z.AI-first architecture, safe parsing, and provider boundaries."
name: "ZAI LLM Engineering"
applyTo: "src/llm/**, src/providers/**, **/*llm*.ts, **/*llm*.tsx, **/*llm*.js, **/*llm*.py, **/*provider*.ts, **/*provider*.js, **/*provider*.py"
---

# LLM Architecture Rules

- Keep `ZAIProvider` as the primary runtime provider.
- Do not scatter direct provider calls through business logic.
- Keep prompt construction, provider calls, parsing, validation, and decision shaping in separate units.
- Treat ILMU as optional non-judge-path infrastructure unless explicit approval is documented.

# Runtime Contract

- Prefer typed decision objects with recommendation, explanation, tradeoffs, assumptions, missing inputs, confidence, and economic impact fields.
- Request JSON when downstream code expects structured output.
- Validate model output before business logic or UI rendering consumes it.
- Never treat raw chain-of-thought as a user-facing explanation.

# Reliability And Cost

- Keep model names, token limits, and base URLs configurable.
- Log request IDs, status, latency, and token usage when available.
- Add bounded retries for transient provider failures.
- Reject, chunk, or summarize oversized payloads before submission.
- Keep deterministic KPI calculations in code.