# Preliminary Round 10-Minute Dual-Host Screen Demo Script

Script status: Draft  
Recording mode: One continuous screen recording with simultaneous live narration  
Target runtime: 9 minutes 40 seconds to 9 minutes 55 seconds  
Start page: Home  
End page: ERP Bridge

This script is designed for a full-screen application recording, not a slide-first pitch. It assumes the browser opens directly on the ASEM Talint Home page and the team records screen and microphone audio at the same time.

ASSUMPTION: the current local demo environment remains unchanged on recording day. In the present local build, the combined `Run Z.AI / ILMU review` button calls the ILMU-backed Z.AI GLM route and returns provider model `ilmu-glm-5.1`.

UNSPECIFIED: whether the final judging environment will keep this exact endpoint wiring or switch back to a direct Z.AI endpoint. If that changes, keep the spoken emphasis on Z.AI GLM and update only the operator note for the combined review button.

## Delivery Mode

- Keep the tone calm, measured, formal, and understated.
- Use short declarative sentences.
- Let the page settle after every click before speaking over new movement.
- Avoid startup-hype language, jokes, or exaggerated claims.
- Keep one speaker active at a time.
- Keep the cursor still while a key sentence lands.

## Team Split

- Ong Khai Sern: opening, Home page framing, combined review explanation, Candidate Lab, Pathway Planner, final close
- Tan Eng Feng: Malaysia context, market evidence, Market Studio, ERP Bridge, operational handoff explanation
- Default cursor operator: Ong for the full recording

## Recording Setup

- Maximize the browser window before recording starts.
- Keep the app on the Home page, at the top of the hero section.
- Turn notifications off.
- Keep the microphone hot from the first second of screen capture.
- If a backup audio recorder is used, start it at the same time and use one clap for sync before speaking.
- Do not display raw keys, terminals, or `.env` contents.
- Keep the repository and deck off-screen for this app-first recording.

## Timing Overview

| Time | Speaker | Page | Goal |
| --- | --- | --- | --- |
| 0:00-0:45 | Ong | Home | Product thesis and user problem |
| 0:45-1:20 | Tan | Home | Malaysia context and economic logic |
| 1:20-3:05 | Ong then Tan | Home | Show working case and run combined review |
| 3:05-4:10 | Tan | Home | Explain market, GIS, OJT, and wage context |
| 4:10-5:15 | Ong | Candidate Lab | Show evidence organization and repair logic |
| 5:15-6:30 | Tan | Market Studio | Show ranked roles and evidence contribution |
| 6:30-7:40 | Ong | Pathway Planner | Show wage scenario and 30-60-90 plan |
| 7:40-9:00 | Tan | ERP Bridge | Show package builder and machine-readable handoff |
| 9:00-9:55 | Ong then Tan | ERP Bridge | Close with value, feasibility, and submission readiness |

## Minute-by-Minute Script

### 1. Opening on Home

Time: 0:00-0:45  
Speaker: Ong  
Page: Home

Cursor and click script:

1. Start with the cursor parked in empty space near the upper-right of the hero area.
2. After recording starts, wait one beat.
3. Move the cursor slowly under `One place to read the candidate clearly`.
4. Move down to the three runtime cards and pause over `Primary path`.
5. Do not click yet.

Spoken script:

Good afternoon judges. We are Team Novum. I am Ong Khai Sern, and my teammate is Tan Eng Feng. This is ASEM Talint, short for talent intelligence. It is a decision-intelligence workflow for semiconductor pathway review. The point is simple. A reviewer should be able to read one candidate clearly, understand the market context around that candidate, and decide the next step with an auditable Z.AI GLM-based explanation.

### 2. Malaysia Lens and Why the Problem Matters

Time: 0:45-1:20  
Speaker: Tan  
Page: Home

Cursor and click script:

1. Move the cursor down to `Malaysia lens`.
2. Pause over `Local capability, not just placement`.
3. Briefly hover over the `NST source, Feb 5 2026` link.
4. Move the cursor away into whitespace so the line lands cleanly.

Spoken script:

Why does this matter now? Because capability building cannot be treated as a generic placement exercise. Malaysia is pushing harder on local sourcing, vendor development, SME participation, and stronger industry links. So the decision is not only whether a candidate looks promising. It is whether the pathway is economically sensible, geographically realistic, and aligned with a real operating environment. That is why the product is built as decision intelligence, not as a generic chat layer.

### 3. Working Case and Combined Review Call

Time: 1:20-2:20  
Speaker: Ong  
Page: Home

Cursor and click script:

1. Scroll down until `Candidate brief` is fully visible.
2. Pause over the payload box for one second.
3. Move the cursor to the `Run Z.AI / ILMU review` button.
4. Click once.
5. Keep the cursor still while the request runs.

Spoken script:

This is the working case. We start from one shared candidate payload, not from a vague prompt. The candidate, target track, required skills, thresholds, and market signals are already structured. In the current local demo environment, this combined review button is wired to an ILMU-backed Z.AI GLM route. For the reviewer, the important point is that the model is asked to return a structured pathway judgment, not an unbounded paragraph.

### 4. Read the Returned Decision

Time: 2:20-3:05  
Speaker: Tan  
Page: Home

Cursor and click script:

1. When the result loads, move the cursor to `Overall score`.
2. Move right to `Confidence`, then `Provider`, then `Missing inputs`.
3. Move down to `Recommendation`.
4. Pause over `Key factors` and `Next steps`.
5. Move briefly to `Raw JSON` and stop there for two seconds.

Spoken script:

Now we have the decision result. The recommendation is clear. The confidence is explicit. The provider used in this run is visible. Missing inputs are also explicit. That matters because the system is not trying to sound certain when the case is thin. Under the surface, deterministic scoring has already been computed in code: toolchain alignment, readiness, accessibility, demand alignment, and wage direction. The model then turns that bounded context into a readable explanation, factors, tradeoffs, next steps, and a structured JSON contract.

### 5. Market Context on the Same Page

Time: 3:05-4:10  
Speaker: Tan  
Page: Home

Cursor and click script:

1. Scroll down to `Market context`.
2. Pause over the four KPI cards.
3. Move to the `Demand by role` section.
4. Move to the GIS map and trace marker `1`, then `2`, then `3`, then `4`.
5. Move down to the OJT table.
6. Move to `Wage outlook` and pause.

Spoken script:

The decision is immediately grounded in market evidence. We can see the wage baseline, the employer-demand view, the GIS accessibility panel, the OJT match, and the wage outlook without leaving the case. The GIS figure is especially important. It uses numbered hotspot markers and a ranked list underneath, so the spatial evidence stays readable during a live demo. What this gives the reviewer is not just a label such as strong fit. It gives a practical sense of access, role demand, shortlist quality, and directional economic upside.

Handoff line:

Ong, let us move from the broad case view into the evidence view.

### 6. Candidate Lab

Time: 4:10-5:15  
Speaker: Ong  
Page: Candidate Lab

Cursor and click script:

1. Move to the top navigation bar.
2. Click `Candidate Lab`.
3. On load, pause over `Skill coverage` and `Evidence depth`.
4. Move through `Role signals`, `Certifications`, `Project evidence`, and `Toolchain evidence`.
5. Move to `Repair queue`.
6. Pause on `Coach notes`.

Spoken script:

Candidate Lab is where the case is tightened before a reviewer advances it. Instead of leaving resume evidence scattered across text, the page organizes it as proof. Role signals are here. Certifications are here. Project evidence and toolchain evidence are here. On the right, the repair queue translates weak evidence into a short, coachable next action. In this sample case, there is no urgent gap. But the product still recommends converting the strongest project into employer-ready talking points. So the reviewer is supported before the decision, not only after it.

### 7. Market Studio

Time: 5:15-6:30  
Speaker: Tan  
Page: Market Studio

Cursor and click script:

1. Click `Market Studio` in the top navigation.
2. Pause over `Roles`, `Top signal`, and `Wage baseline`.
3. Move down the ranked role cards from `Validation Engineer Trainee` to `Robotics and Test Automation Trainee`.
4. Pause on the first card's demand, resume, and salary line.
5. Move to `Contribution by role` and stop on `Validation Engineer Trainee`.
6. Keep the cursor still while the summary sentence is spoken.

Spoken script:

Market Studio answers a different question. Not only, does the target track fit? Also, what nearby roles become plausible once resume evidence is counted properly? The shortlist keeps demand, evidence, and salary context together. The top role remains Validation Engineer Trainee in Selangor. But we also see adjacency roles in Penang, Kedah, and Johor. This is useful because a reviewer can separate the primary path from the secondary path while keeping the evidence trail visible. It is a shortlist that can be defended.

### 8. Pathway Planner

Time: 6:30-7:40  
Speaker: Ong  
Page: Pathway Planner

Cursor and click script:

1. Click `Pathway Planner` in the navigation.
2. Pause over `Active role`, `Wage change`, `Evidence strength`, and `Blockers`.
3. Move to `Wage view`.
4. Scroll slightly until the `30-60-90 plan` fills the center of the screen.
5. Trace down the `30 days`, `60 days`, and `90 days` columns.
6. Pause on `Watchouts`.

Spoken script:

Pathway Planner turns a shortlist into a plan. The selected role is explicit. The wage direction is explicit. The evidence strength is explicit. Then the system produces a 30-60-90 sequence that a counselor or candidate can actually follow. That point is important. A recommendation without a next-step plan is only a label. Here, the product ties the label to actions, timing, and a salary reference that is clearly presented as directional rather than guaranteed.

### 9. ERP Bridge

Time: 7:40-9:00  
Speaker: Tan  
Page: ERP Bridge

Cursor and click script:

1. Click `ERP Bridge` in the navigation.
2. Pause over `Schema version`, `ERP system`, `Case status`, and `Selected role`.
3. Move to `Build package` and click once.
4. Pause over `Package overview`.
5. Move through `Upsert keys`.
6. Move through `Sync actions`.
7. Move to `Machine-readable package` and rest on the JSON block for two seconds.

Spoken script:

ERP Bridge is the operational handoff. This page packages the same case into a stable sync bundle so an ERP does not need to scrape the screen or rely on manual copying. Here we can see the package overview, the upsert keys, the sync actions, and the raw machine-readable contract. In other words, the workflow does not stop at explanation. It reaches the point where the decision can move downstream into a real institutional process.

### 10. Close on ERP Bridge

Time: 9:00-9:55  
Speaker: Ong, then Tan  
Page: ERP Bridge

Cursor and click script:

1. Keep the cursor still over `Package overview` for Ong's first line.
2. Move gently to `Machine-readable package` for Tan's line.
3. Do not click again.

Spoken script, Ong:

To close, ASEM Talint turns a manual review of scattered evidence into a disciplined semiconductor pathway workflow. The case is tightened. Market context is made readable. The Z.AI GLM-based reasoning output is structured and auditable. And the final handoff is ready for downstream use.

Spoken script, Tan:

Our preliminary submission is designed to be judged as a coherent build. The product logic, the architecture, the tests, and the demonstration all point to the same claim: this is a feasible decision-intelligence prototype for Domain 2. Thank you.

## Filler Lines for Load Delays

Use one line only when needed. Do not stack them.

- While the combined review call is running: `While this call is running, note that we validate a structured response contract rather than accepting free text directly into the workflow.`
- While a page is settling after navigation: `We will hold for one second here so the page settles and the judges can read the layout clearly.`
- While the ERP package is rebuilding: `This packaging step is using the current case state. It is not asking a second model to reinterpret the candidate.`

## Operator Rules During Recording

- Never circle the cursor repeatedly.
- Never drag-select text inside the JSON box.
- If a scroll overshoots, scroll back once, slowly, without apology.
- If the review call fails, stop recording and restart after the environment is corrected.
- If the page already shows the expected state, do not add extra clicks just to create motion.

## Final Reminder Before Recording

- Keep the Home page runtime cards visible long enough for judges to read them.
- Keep the combined review result on screen long enough for judges to see the provider name and recommendation.
- Keep the GIS panel visible long enough for judges to see both the numbered markers and the ranked list.
- End on ERP Bridge so the video closes on operational feasibility, not only explanation.