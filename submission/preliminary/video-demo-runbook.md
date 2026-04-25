# Preliminary Round 10-Minute Pitching Video Runbook

Video status: Draft  
Target format: MP4 or MOV  
Target duration: 10 minutes maximum

Deck currently paired with this runbook: [ASEM-Talint-10-minute-presentation.pptx](./ASEM-Talint-10-minute-presentation.pptx)

## Pre-Recording Technical Checklist

- confirm the exact environment to be recorded is the same one used for the final pitch
- confirm the generated deck file [ASEM-Talint-10-minute-presentation.pptx](./ASEM-Talint-10-minute-presentation.pptx) matches the repository snapshot being recorded
- confirm `/health` reports the live Z.AI route as ready
- confirm a live call to `POST /v1/decisions/candidate-track-fit` succeeds before recording
- remove secrets, raw API keys, and private links from the visible screen
- verify citations are present in the deck and any on-screen external claims
- verify the repository branch or folder shown in the recording matches the final submission pack

ASSUMPTION: the final recording environment will have a valid and authorized Z.AI key. The current repository should not be represented as using a different reasoning model in the judged path.

## Recommended 10-Minute Structure

| Time | Segment | Goal |
| --- | --- | --- |
| 0:00-0:45 | Opening | Introduce the problem, users, and one-sentence thesis |
| 0:45-2:00 | Domain fit and economic logic | Explain the semiconductor talent-allocation problem, the "Made by Malaysia" context, and the main labor-market frictions the product addresses |
| 2:00-3:30 | Product overview | Show the dashboard, scope, and why Z.AI is central |
| 3:30-7:00 | Prototype demonstration | Walk through resume parsing, market panels, and live decision flow |
| 7:00-8:30 | Architecture and QA | Show system logic, provider boundary, and test evidence |
| 8:30-9:30 | Feasibility and next steps | Explain what is working now and what remains `UNSPECIFIED` |
| 9:30-10:00 | Closing | Restate value, submission readiness, and repository availability |

## Demo Script by Segment

## 1. Opening

- introduce the product name and team: Novum, with Ong Khai Sern as team leader and Tan Eng Feng as team member; expand Talint once as "talent intelligence"
- state that the system helps training operators make auditable semiconductor pathway decisions
- state explicitly that Z.AI GLM is the judged reasoning engine in the shipped product path

## 2. Problem and Domain Fit

- explain the difficulty of manual candidate-track screening
- explain why missing inputs, wage context, and employer demand matter
- cite the national industrial context when referencing the "Made by Malaysia" framing
- state the economic logic explicitly: screening friction, signaling friction, matching friction, spatial friction, and wage-mobility uncertainty
- explain that the product layers exist because each one reduces a different decision friction rather than because the team wanted more dashboard panels

## 3. Product Overview

- show the dashboard hero section
- point out that the product is not a generic chatbot
- highlight that deterministic scoring and official-data slices are combined with Z.AI-generated structured explanation
- mention that Candidate Lab, Market Studio, Pathway Planner, and ERP Bridge correspond to screening, matching, mobility, and coordination functions

## 4. Prototype Demonstration

Recommended click path:

1. Load the dashboard and show runtime readiness.
2. Show the sample candidate payload.
3. Parse and apply a resume so the audience sees structured evidence ingestion.
4. Refresh market panels and explain wage, employer-demand, accessibility, and OJT context.
5. Pause on the GIS accessibility panel and point out that the hotspot figure now uses compact numbered markers with a separate ranked list, so the spatial evidence stays readable during the demo.
6. Run the live Z.AI decision route.
7. Inspect the recommendation, top factors, tradeoffs, missing inputs, and pathway steps.
8. Show the raw structured response briefly to prove contract discipline.

## 5. Architecture and QA Evidence

- show one simplified architecture diagram or repository structure view
- explain that scoring weights, missing-input handling, and confidence baseline are coded deterministically
- mention that tests cover happy path, invalid payloads, malformed model output, fenced JSON, and OCR fallback

## 6. Feasibility and Honest Boundaries

- call out that the prototype currently supports one decision workflow
- state that production persistence, reviewer workflow management, and public deployment remain `UNSPECIFIED`
- explain that optional ILMU support exists only as non-judge-path compatibility infrastructure
- avoid claiming causal impact on wages or placement outcomes; describe the current wage view as a directional scenario support layer

## 7. Closing

- restate the product value in one sentence
- remind judges that the submission includes PRD, SAD, QATD, repository, deck, and video
- show or mention the public repository link once finalized

## Recording Rules

- do not present the degraded demo route as the main judged flow
- do not present the optional ILMU route as equivalent to the judged Z.AI path
- if the live Z.AI call fails during recording, stop and re-record after fixing the environment rather than hiding the failure behind another model path
- keep the runtime labels and route names visible when practical

## On-Screen Assets to Prepare in Advance

- pitch deck in presenter-friendly order
- local app running on the final recording port
- one clean sample resume file ready for upload
- [dashboard-gis-accessibility-panel.png](./assets/dashboard-gis-accessibility-panel.png) as a fallback still image for the accessibility panel
- repository window with tests or architecture files visible
- final citations slide or footer

## References

- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [UMHackathon2026 Judging Criteria](../../UMHackathon2026%20Judging%20Criteria.pdf)
- [Pitch deck outline](./pitch-deck-outline.md)
- [Economic theory anchor](./economic-theory-anchor.md)
- [PRD draft](./PRD.md)
- [SAD draft](./SAD.md)
- [QATD draft](./QATD.md)
