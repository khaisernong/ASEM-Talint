---
description: "Use when implementing or refactoring a server-side Z.AI GLM endpoint for Domain 2 decision intelligence."
name: "Implement ZAI Endpoint"
argument-hint: "Describe the endpoint, service, or selected files"
agent: "agent"
---

Implement or refactor a server-side Z.AI GLM integration for this repository.

Requirements:

- Keep Z.AI GLM as the primary reasoning provider.
- Preserve or introduce a provider abstraction instead of scattering direct API calls.
- Separate prompt building, provider transport, response parsing, schema validation, and decision shaping.
- Use environment variables for secrets, model IDs, base URLs, and limits.
- Request structured JSON when downstream code expects machine-readable output.
- Log latency and token usage where the provider exposes them.
- Add or update the narrowest useful validation for the touched slice.

Output:

- Implemented code changes.
- Any config or environment-variable additions.
- A brief note on how the endpoint satisfies Domain 2 compliance.