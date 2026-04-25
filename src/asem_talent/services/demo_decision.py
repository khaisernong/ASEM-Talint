from asem_talent.domain.models import (
    CandidateDecisionRequest,
    CandidateDecisionResult,
    DecisionExplanation,
    ProviderUsage,
)
from asem_talent.domain.scoring import build_decision_context


FACTOR_LABELS = {
    "toolchain_alignment": "toolchain alignment with the target track",
    "foundational_readiness": "foundational coding and math readiness",
    "portfolio_relevance": "portfolio relevance to the requested pathway",
    "communication_readiness": "communication readiness",
    "accessibility_score": "accessibility to the training location",
    "completion_likelihood": "completion likelihood based on prior signals",
    "wage_uplift_potential": "estimated wage uplift potential",
    "employer_demand_alignment": "employer demand alignment",
}


def _sorted_top_factors(score_breakdown: dict[str, float]) -> list[str]:
    ranked_pairs = sorted(score_breakdown.items(), key=lambda item: item[1], reverse=True)
    top_factor_names = [FACTOR_LABELS[key] for key, _ in ranked_pairs[:3] if key in FACTOR_LABELS]
    return top_factor_names


def build_demo_decision_result(request: CandidateDecisionRequest) -> CandidateDecisionResult:
    context = build_decision_context(request.candidate, request.target_track)
    overall_score = context.score_breakdown.overall_score
    track_name = request.target_track.track_name

    if overall_score >= 0.75:
        recommendation = f"Advance the candidate into {track_name}."
        explanation_summary = "The deterministic baseline indicates that this candidate is already close to track readiness and can move into the target pathway with focused reinforcement on remaining gaps."
        tradeoffs = ["Advancing immediately may still require targeted reinforcement for the remaining gap areas."]
    elif overall_score >= 0.55:
        recommendation = f"Route the candidate to a preparatory bridge before {track_name}."
        explanation_summary = "The candidate shows enough promise for the target pathway, but the current readiness level suggests a short bridge module will reduce seat-allocation risk."
        tradeoffs = ["A bridge module delays placement, but lowers the chance of poor cohort fit."]
    else:
        recommendation = "Route the candidate to an embedded, robotics, or fundamentals feeder track first."
        explanation_summary = "The current baseline does not support direct placement into the requested track without additional preparation on core technical foundations."
        tradeoffs = ["Feeder routing improves readiness, but delays access to the target track."]

    top_factors = _sorted_top_factors(context.score_breakdown.model_dump())
    pathway_steps = []
    for gap in context.top_skill_gaps:
        pathway_steps.append(f"Close the skill gap in {gap} through a targeted module or project.")
    if not pathway_steps:
        pathway_steps.append("Move to cohort review and employer-fit discussion.")
    if context.missing_inputs:
        pathway_steps.append("Capture the missing inputs before a live Z.AI decision is used for judge-path evaluation.")

    explanation = DecisionExplanation(
        recommendation=recommendation,
        recommendation_type="track_fit_demo",
        target_track_or_role=track_name,
        explanation_summary=explanation_summary,
        top_factors=top_factors,
        missing_inputs=context.missing_inputs,
        tradeoffs=tradeoffs,
        confidence=min(context.confidence_baseline, 0.78),
        pathway_steps=pathway_steps,
        wage_note="This dashboard demo does not compute a live wage estimate yet. Treat any mobility interpretation as UNSPECIFIED until official wage data is integrated.",
        accessibility_note=f"The baseline accessibility score is {context.score_breakdown.accessibility_score:.2f}. This is a deterministic proxy, not a GIS travel-time result.",
        validation_notes=[
            "DEGRADED: local dashboard demo generated without Z.AI GLM.",
            "Use this mode for UI validation only, not for judge-path reasoning.",
        ],
    )
    usage = ProviderUsage(model="demo-heuristic", latency_ms=0, total_tokens=0)

    return CandidateDecisionResult(
        candidate_id=request.candidate.candidate_id,
        target_track_id=request.target_track.track_id,
        context=context,
        explanation=explanation,
        usage=usage,
    )