from fastapi import APIRouter, HTTPException

from asem_talent.data.official_data import load_employer_roles, load_wage_signals
from asem_talent.domain.models import (
    AccessibilityRequest,
    AccessibilityResponse,
    EmployerDemandRequest,
    EmployerDemandResponse,
    EmployerRole,
    OJTMatchRequest,
    OJTMatchResponse,
    WageMobilityRequest,
    WageMobilityResult,
    WageSignal,
)
from asem_talent.services.employer_demand import build_employer_demand_response
from asem_talent.services.accessibility import build_accessibility_response
from asem_talent.services.ojt_matching import build_ojt_match_response
from asem_talent.services.wage_mobility import estimate_wage_mobility

router = APIRouter(prefix="/v1", tags=["market-signals"])


@router.get("/signals/wages", response_model=list[WageSignal])
def list_wage_signals(state: str | None = None, sector: str | None = None) -> list[WageSignal]:
    signals = list(load_wage_signals())
    if state is not None:
        signals = [signal for signal in signals if signal.state.lower() == state.lower()]
    if sector is not None:
        signals = [signal for signal in signals if signal.sector.lower() == sector.lower()]
    return signals


@router.get("/signals/employer-demand", response_model=list[EmployerRole])
def list_employer_demand(state: str | None = None, track_id: str | None = None) -> list[EmployerRole]:
    roles = list(load_employer_roles())
    if state is not None:
        roles = [role for role in roles if role.state.lower() == state.lower()]
    if track_id is not None:
        roles = [role for role in roles if role.track_id == track_id]
    return roles


@router.post("/signals/employer-demand/ranked", response_model=EmployerDemandResponse)
def rank_employer_demand(request: EmployerDemandRequest) -> EmployerDemandResponse:
    return build_employer_demand_response(request)


@router.post("/signals/accessibility", response_model=AccessibilityResponse)
def candidate_accessibility(request: AccessibilityRequest) -> AccessibilityResponse:
    return build_accessibility_response(request)


@router.post("/matching/ojt", response_model=OJTMatchResponse)
def candidate_ojt_matches(request: OJTMatchRequest) -> OJTMatchResponse:
    return build_ojt_match_response(request)


@router.post("/analysis/wage-mobility", response_model=WageMobilityResult)
def candidate_wage_mobility(request: WageMobilityRequest) -> WageMobilityResult:
    try:
        return estimate_wage_mobility(request)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=f"Unknown target_role_id: {error.args[0]}") from error