from typing import Protocol

from asem_talent.domain.models import (
    CandidateDecisionRequest,
    DecisionExplanation,
    DeterministicDecisionContext,
    ProviderUsage,
)


class DecisionProviderError(RuntimeError):
    pass


class LLMProvider(Protocol):
    def explain_candidate_track_fit(
        self,
        request: CandidateDecisionRequest,
        context: DeterministicDecisionContext,
    ) -> tuple[DecisionExplanation, ProviderUsage]:
        ...
