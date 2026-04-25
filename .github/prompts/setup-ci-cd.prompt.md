---
description: "Use when creating or refining CI workflows for build, test, doc export, or submission-package generation in this repository."
name: "Setup CI CD"
argument-hint: "Describe the workflow or checks you want to add"
agent: "agent"
---

Create or refine CI or packaging workflows for this repository.

Requirements:

- Focus on install, build, lint, tests, docs export, or artifact packaging.
- Keep final hackathon submission manual.
- Prefer small, reviewable workflows with explicit artifacts.
- Surface any missing environment variables, secrets, or manual gates.

If the repository is missing enough structure to create a workflow safely, state the blocker and generate the smallest useful scaffold.