from asem_talent.domain.models import CandidateDecisionRequest, CandidateDecisionResult
from asem_talent.domain.scoring import build_decision_context
from asem_talent.llm.provider import LLMProvider


class DecisionEngine:
    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def evaluate_candidate(self, request: CandidateDecisionRequest) -> CandidateDecisionResult:
        context = build_decision_context(request.candidate, request.target_track)
        explanation, usage = self.provider.explain_candidate_track_fit(request, context)
        return CandidateDecisionResult(
            candidate_id=request.candidate.candidate_id,
            target_track_id=request.target_track.track_id,
            context=context,
            explanation=explanation,
            usage=usage,
        )
