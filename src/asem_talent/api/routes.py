from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from asem_talent.api.dependencies import get_decision_engine, get_ilmu_decision_engine
from asem_talent.domain.models import CandidateDecisionRequest, CandidateDecisionResult
from asem_talent.llm.provider import DecisionProviderError
from asem_talent.services.demo_decision import build_demo_decision_result
from asem_talent.services.decision_engine import DecisionEngine

router = APIRouter(prefix="/v1/decisions", tags=["decisions"])


@router.post("/candidate-track-fit", response_model=CandidateDecisionResult)
def candidate_track_fit(
    request: CandidateDecisionRequest,
    engine: Annotated[DecisionEngine, Depends(get_decision_engine)],
) -> CandidateDecisionResult:
    try:
        return engine.evaluate_candidate(request)
    except DecisionProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@router.post("/candidate-track-fit/ilmu", response_model=CandidateDecisionResult)
def candidate_track_fit_ilmu(
    request: CandidateDecisionRequest,
    engine: Annotated[DecisionEngine, Depends(get_ilmu_decision_engine)],
) -> CandidateDecisionResult:
    try:
        return engine.evaluate_candidate(request)
    except DecisionProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@router.post("/candidate-track-fit/demo", response_model=CandidateDecisionResult)
def candidate_track_fit_demo(request: CandidateDecisionRequest) -> CandidateDecisionResult:
    return build_demo_decision_result(request)
