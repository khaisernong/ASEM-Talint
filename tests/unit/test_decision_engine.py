import pytest

from asem_talent.domain.models import CandidateDecisionRequest, DecisionExplanation, ProviderUsage, ResumeContext
from asem_talent.llm.provider import DecisionProviderError
from asem_talent.services.decision_engine import DecisionEngine


class FakeProvider:
    def explain_candidate_track_fit(self, request, context):
        return (
            DecisionExplanation(
                recommendation="Advance the candidate to the validation and robotics cohort.",
                recommendation_type="track_fit",
                target_track_or_role=request.target_track.track_name,
                explanation_summary="The candidate already demonstrates debugging and data acquisition signals aligned with the target track.",
                top_factors=["debugging overlap", "same-district accessibility", "strong communication score"],
                missing_inputs=context.missing_inputs,
                tradeoffs=["Python fundamentals still need reinforcement"],
                confidence=context.confidence_baseline,
                pathway_steps=["Complete Python basics module", "Proceed to ASEM validation cohort"],
                wage_note="Wage uplift is an estimate until official wage integration is connected.",
                accessibility_note="Candidate and track are both in Sepang, which improves accessibility.",
                validation_notes=["Synthetic fixture used for automated validation."],
            ),
            ProviderUsage(model="test-double", total_tokens=128, latency_ms=4),
        )


class FailingProvider:
    def explain_candidate_track_fit(self, request, context):
        raise DecisionProviderError("provider failure")


def test_evaluate_candidate_happy_path(sample_request: CandidateDecisionRequest) -> None:
    engine = DecisionEngine(provider=FakeProvider())

    result = engine.evaluate_candidate(sample_request)

    assert result.candidate_id == "cand_0001"
    assert result.explanation.recommendation_type == "track_fit"
    assert result.context.score_breakdown.overall_score > 0.7
    assert result.usage.total_tokens == 128


def test_evaluate_candidate_surfaces_missing_inputs(request_with_missing_signals: CandidateDecisionRequest) -> None:
    engine = DecisionEngine(provider=FakeProvider())

    result = engine.evaluate_candidate(request_with_missing_signals)

    assert "candidate.communication_score" in result.context.missing_inputs
    assert "target_track.employer_demand_signal" in result.context.missing_inputs
    assert result.explanation.missing_inputs == result.context.missing_inputs
    assert result.explanation.confidence < 0.9


def test_evaluate_candidate_raises_on_provider_failure(sample_request: CandidateDecisionRequest) -> None:
    engine = DecisionEngine(provider=FailingProvider())

    with pytest.raises(DecisionProviderError):
        engine.evaluate_candidate(sample_request)


def test_evaluate_candidate_uses_resume_context_to_close_skill_gap(sample_request: CandidateDecisionRequest) -> None:
    engine = DecisionEngine(provider=FakeProvider())
    request = sample_request.model_copy(deep=True)
    request.candidate.skill_tags = ["debugging", "data_acquisition"]
    request.candidate.resume_context = ResumeContext(
        summary="Completed validation scripting and lab debugging work during a short internship.",
        skill_tags=["python_basics"],
        tool_tags=["oscilloscope"],
    )

    result = engine.evaluate_candidate(request)

    assert result.context.score_breakdown.toolchain_alignment == 1.0
    assert "python_basics" not in result.context.top_skill_gaps
