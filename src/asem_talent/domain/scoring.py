from asem_talent.domain.models import CandidateProfile, DeterministicDecisionContext, SuitabilityBreakdown, TrainingTrack


WEIGHTS = {
    "toolchain_alignment": 0.25,
    "foundational_readiness": 0.20,
    "portfolio_relevance": 0.15,
    "communication_readiness": 0.10,
    "accessibility_score": 0.10,
    "completion_likelihood": 0.10,
    "wage_uplift_potential": 0.05,
    "employer_demand_alignment": 0.05,
}


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _normalize_score(score: float | None, maximum: float = 100.0) -> float:
    if score is None:
        return 0.5
    return _clamp(score / maximum)


def _overlap_score(observed: list[str], required: list[str]) -> float:
    if not required:
        return 0.0
    observed_set = {item.strip().lower() for item in observed}
    required_set = {item.strip().lower() for item in required}
    return len(observed_set & required_set) / len(required_set)


def _compute_accessibility_score(candidate: CandidateProfile, track: TrainingTrack) -> float:
    if candidate.state == track.state and candidate.district == track.district:
        return 1.0
    if candidate.state == track.state:
        return 0.75
    if candidate.willing_to_relocate is True:
        return 0.65
    if candidate.willing_to_relocate is False:
        return 0.35
    return 0.45


def _compute_completion_likelihood(candidate: CandidateProfile) -> float:
    score = 0.35
    score += 0.25 * _normalize_score(candidate.communication_score)
    score += 0.20 if candidate.prior_training else 0.0
    score += 0.20 if candidate.effective_portfolio_tags() else 0.0
    return _clamp(score)


def _find_missing_inputs(candidate: CandidateProfile, track: TrainingTrack) -> list[str]:
    missing_inputs: list[str] = []

    if track.minimum_coding_score is not None and candidate.coding_test_score is None:
        missing_inputs.append("candidate.coding_test_score")
    if track.minimum_math_score is not None and candidate.math_foundation_score is None:
        missing_inputs.append("candidate.math_foundation_score")
    if candidate.communication_score is None:
        missing_inputs.append("candidate.communication_score")
    if track.employer_demand_signal is None:
        missing_inputs.append("target_track.employer_demand_signal")
    if track.wage_growth_signal is None:
        missing_inputs.append("target_track.wage_growth_signal")
    if candidate.willing_to_relocate is None and candidate.state != track.state:
        missing_inputs.append("candidate.willing_to_relocate")

    return missing_inputs


def build_decision_context(candidate: CandidateProfile, track: TrainingTrack) -> DeterministicDecisionContext:
    effective_skill_tags = candidate.effective_skill_tags()
    effective_portfolio_tags = candidate.effective_portfolio_tags()

    toolchain_alignment = _overlap_score(effective_skill_tags, track.required_skills)
    foundational_readiness = (
        _normalize_score(candidate.coding_test_score) + _normalize_score(candidate.math_foundation_score)
    ) / 2
    portfolio_relevance = _overlap_score(effective_portfolio_tags + effective_skill_tags, track.required_skills)
    communication_readiness = _normalize_score(candidate.communication_score)
    accessibility_score = _compute_accessibility_score(candidate, track)
    completion_likelihood = _compute_completion_likelihood(candidate)
    wage_uplift_potential = track.wage_growth_signal if track.wage_growth_signal is not None else 0.5
    employer_demand_alignment = track.employer_demand_signal if track.employer_demand_signal is not None else 0.5

    overall_score = sum(
        [
            toolchain_alignment * WEIGHTS["toolchain_alignment"],
            foundational_readiness * WEIGHTS["foundational_readiness"],
            portfolio_relevance * WEIGHTS["portfolio_relevance"],
            communication_readiness * WEIGHTS["communication_readiness"],
            accessibility_score * WEIGHTS["accessibility_score"],
            completion_likelihood * WEIGHTS["completion_likelihood"],
            wage_uplift_potential * WEIGHTS["wage_uplift_potential"],
            employer_demand_alignment * WEIGHTS["employer_demand_alignment"],
        ]
    )

    missing_inputs = _find_missing_inputs(candidate, track)
    candidate_skills = {skill.lower() for skill in effective_skill_tags}
    top_skill_gaps = [skill for skill in track.required_skills if skill.lower() not in candidate_skills][:3]
    confidence_baseline = _clamp(0.90 - (0.08 * len(missing_inputs)), minimum=0.35)

    return DeterministicDecisionContext(
        score_breakdown=SuitabilityBreakdown(
            toolchain_alignment=round(toolchain_alignment, 4),
            foundational_readiness=round(foundational_readiness, 4),
            portfolio_relevance=round(portfolio_relevance, 4),
            communication_readiness=round(communication_readiness, 4),
            accessibility_score=round(accessibility_score, 4),
            completion_likelihood=round(completion_likelihood, 4),
            wage_uplift_potential=round(wage_uplift_potential, 4),
            employer_demand_alignment=round(employer_demand_alignment, 4),
            overall_score=round(overall_score, 4),
        ),
        top_skill_gaps=top_skill_gaps,
        missing_inputs=missing_inputs,
        confidence_baseline=round(confidence_baseline, 4),
    )
