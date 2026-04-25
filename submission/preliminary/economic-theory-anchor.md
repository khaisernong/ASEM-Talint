# ASEM Talint Economic Theory Anchor

Document status: Draft  
Purpose: Judge-facing economic framing for the current prototype

## 1. Core Economic Logic

ASEM Talint is not a generic AI assistant. Economically, it is a decision-support system for reducing labor-market frictions in semiconductor talent development.

The current prototype is anchored in five linked ideas:

- Human capital allocation: training seats and OJT slots are scarce investments. The fit score, gap detection, and pathway steps are designed to allocate scarce training capacity toward candidates who appear most ready for the target pathway with the least additional remediation.
- Information asymmetry and signaling: resumes, certifications, projects, and internship history are imperfect signals of candidate capability. Resume parsing and structured evidence extraction reduce reviewer uncertainty by standardizing those signals instead of leaving them buried in unstructured CV text.
- Matching and search frictions: the goal is not only to identify a strong candidate, but to identify a strong candidate-role-track match. Candidate-track fit, resume-aware employer-demand ranking, and OJT matching all treat outcome quality as a matching problem rather than a raw ranking problem.
- Spatial frictions and agglomeration: semiconductor opportunities cluster geographically. Accessibility scoring and hotspot analysis reflect the idea that location, commuting distance, and relocation willingness affect whether a candidate can realistically access a pathway even when the role itself is attractive.
- Wage mobility and job ladders: the wage-mobility layer treats pathway choice as a step on a labor-market ladder. It gives reviewers a directional estimate of whether the proposed pathway plausibly improves earnings, while staying explicit that the estimate is a scenario, not a guaranteed realized wage.

## 2. How The Current Product Maps To Theory

| Current feature | Economic concept | Why it matters |
| --- | --- | --- |
| Candidate Lab | human capital allocation; signaling | helps reviewers inspect which observed signals justify investment in a candidate and which gaps still need remediation |
| Dashboard decision flow | screening under uncertainty | combines deterministic readiness proxies with Z.AI GLM structured explanation so screening is evidence-backed rather than ad hoc |
| Market Studio | matching; search frictions | ranks employer roles using both demand and candidate-specific evidence, which is closer to a matching problem than a vacancy-count problem |
| GIS accessibility | spatial frictions; agglomeration | makes cluster access visible so recommendation quality is not overstated for geographically weak matches |
| OJT matching | two-sided matching intuition | surfaces roles where candidate evidence, employer demand, wages, and access all align |
| Wage mobility | job ladders; expected returns to training | frames pathway choice in terms of directional earnings movement rather than only acceptance into a training seat |
| ERP Bridge | transaction-cost economics; coordination efficiency | reduces handoff costs between reviewers, employer-partnership teams, and enterprise systems by packaging one consistent sync contract |

## 3. Working Economic Interpretation Of The Prototype

In economic terms, the prototype currently behaves like this:

1. Candidate capability is only partially observed.
2. Resume evidence, tests, prior training, projects, and certifications reveal part of that capability through noisy signals.
3. The system uses deterministic scoring to estimate readiness for a specific training track under bounded information.
4. Market and OJT layers then ask whether the candidate is not only trainable, but also matchable to real employer demand under location and wage constraints.
5. The ERP layer makes those outputs operational by reducing coordination costs in institutional decision workflows.

This framing is important because it explains why ASEM Talint contains multiple layers instead of only one recommendation endpoint. The product is trying to reduce several frictions at once: screening friction, information friction, matching friction, spatial friction, and coordination friction.

## 4. Boundary Conditions And Honest Limits

The current prototype is not a causal inference engine and should not be described as one.

- It does not estimate the causal effect of training on long-run wages.
- It does not model equilibrium labor demand or employer behavior.
- It does not prove productivity; it organizes available signals into a more structured screening and matching workflow.
- It does not guarantee mobility outcomes; wage panels remain directional scenario support using bounded official data and employer salary bands.

ASSUMPTION: if a training operator integrates the workflow into real review operations, lower review friction and more structured evidence handling should improve decision consistency. That outcome is theoretically plausible, but not yet measured in the current prototype.

## 5. Why Z.AI GLM Still Fits The Economic Framing

Z.AI GLM is not replacing the economic logic. The economic structure remains in code:

- readiness weights and thresholds are deterministic
- missing-input penalties are deterministic
- employer-demand and wage signals are deterministic data slices
- OJT and wage-mobility calculations remain code-driven

Z.AI GLM adds structured interpretation on top of those bounded signals. Economically, that means the model is used to explain and summarize a structured decision problem, not to invent the economic logic itself.

## References

- Becker, Gary S. 1964. Human Capital.
- Akerlof, George A. 1970. The Market for "Lemons": Quality Uncertainty and the Market Mechanism.
- Spence, Michael. 1973. Job Market Signaling.
- Mortensen, Dale T., and Christopher A. Pissarides. 1994. Job Creation and Job Destruction in the Theory of Unemployment.
- Marshall, Alfred. 1890. Principles of Economics.
- Williamson, Oliver E. 1981. The Economics of Organization: The Transaction Cost Approach.