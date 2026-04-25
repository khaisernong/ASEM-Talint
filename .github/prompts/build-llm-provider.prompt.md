---
description: "Use when creating or revising the LLM provider abstraction, ZAI provider implementation, or optional non-judge-path adapters."
name: "Build LLM Provider"
argument-hint: "Describe the provider layer you want to add or change"
agent: "agent"
---

Create or update the provider layer for this repository.

Requirements:

- Keep a narrow `LLMProvider` interface.
- Make `ZAIProvider` the primary implementation.
- If an alternative provider is requested, isolate it clearly as optional and non-judge-path unless compliance is documented.
- Return typed outputs plus usage metadata.
- Validate JSON before returning structured decisions.
- Keep retries, limits, and error handling explicit.

Output:

- Provider interface and implementation changes.
- Notes on config, testing, and any compliance-sensitive tradeoffs.