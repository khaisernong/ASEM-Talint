---
description: "Use when generating focused tests for decision-engine logic, provider integrations, schema validation, or UI flows in this hackathon repo."
name: "Generate Tests"
argument-hint: "Describe the code or files that need tests"
agent: "agent"
---

Generate or extend the narrowest useful tests for the selected slice.

Priorities:

- one happy path
- one invalid-input or missing-data path
- one provider or integration failure path when relevant
- one schema-validation or output-contract check when relevant
- one non-functional check if the slice has measurable constraints

Follow existing test conventions and keep assertions concrete.