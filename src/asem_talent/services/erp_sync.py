from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256

from asem_talent.domain.models import (
    ERPDecisionSummary,
    ERPCandidateMaster,
    ERPSyncPackage,
    ERPSyncRequest,
    ERPStatusMap,
    ERPTrainingCase,
    ERPUpsertKey,
    EmployerDemandRequest,
    OJTMatchRequest,
    WageMobilityRequest,
)
from asem_talent.domain.scoring import build_decision_context
from asem_talent.services.employer_demand import build_employer_demand_response
from asem_talent.services.ojt_matching import build_ojt_match_response
from asem_talent.services.wage_mobility import estimate_wage_mobility


ERP_SCHEMA_VERSION = "erp.sync.v1"

FACTOR_LABELS = {
    "toolchain_alignment": "toolchain alignment",
    "foundational_readiness": "foundational readiness",
    "portfolio_relevance": "portfolio relevance",
    "communication_readiness": "communication readiness",
    "accessibility_score": "location accessibility",
    "completion_likelihood": "completion likelihood",
    "wage_uplift_potential": "wage uplift potential",
    "employer_demand_alignment": "employer demand alignment",
}


def _build_case_id(request: ERPSyncRequest) -> str:
    return f"case_{request.candidate.candidate_id}_{request.target_track.track_id}"


def _integration_id(request: ERPSyncRequest) -> str:
    raw = "|".join(
        [
            request.erp_system,
            request.external_candidate_id or request.candidate.candidate_id,
            request.external_case_id or _build_case_id(request),
            request.target_track.track_id,
        ]
    )
    return sha256(raw.encode("utf-8")).hexdigest()[:16]


def _top_strengths(context) -> list[str]:
    score_breakdown = context.score_breakdown.model_dump()
    ranked = sorted(score_breakdown.items(), key=lambda item: item[1], reverse=True)
    return [FACTOR_LABELS[key] for key, _ in ranked[:3] if key in FACTOR_LABELS]


def _readiness_band(overall_score: float) -> tuple[str, str, str]:
    if overall_score >= 0.75:
        return ("ready", "ready_for_track_review", "advance")
    if overall_score >= 0.55:
        return ("bridge", "bridge_required", "prepare_then_review")
    return ("prepare", "foundation_required", "reroute_before_review")


def _market_priority(ranked_market_roles, ojt_shortlist) -> str:
    top_market_score = ranked_market_roles[0].market_signal_score if ranked_market_roles else 0.0
    top_match_score = ojt_shortlist[0].match_score if ojt_shortlist else 0.0
    combined = max(top_market_score, top_match_score)
    if combined >= 0.8:
        return "high"
    if combined >= 0.6:
        return "medium"
    return "low"


def _mobility_band(wage_mobility) -> str:
    if wage_mobility is None or wage_mobility.estimated_uplift_pct is None:
        return "unspecified"
    if wage_mobility.estimated_uplift_pct >= 60:
        return "transformative"
    if wage_mobility.estimated_uplift_pct >= 25:
        return "positive"
    if wage_mobility.estimated_uplift_pct >= 0:
        return "limited"
    return "negative"


def _summary_note(readiness_band: str, request: ERPSyncRequest, top_role_title: str | None) -> str:
    if readiness_band == "ready":
        prefix = f"Candidate is operationally ready for {request.target_track.track_name} review"
    elif readiness_band == "bridge":
        prefix = f"Candidate should complete a bridge before {request.target_track.track_name} allocation"
    else:
        prefix = "Candidate needs further preparation before direct track allocation"
    if top_role_title:
        return f"{prefix}; top ERP-shortlisted role is {top_role_title}."
    return f"{prefix}; no role shortlist was available at packaging time."


def build_erp_sync_package(request: ERPSyncRequest) -> ERPSyncPackage:
    generated_at = datetime.now(timezone.utc).isoformat()
    context = build_decision_context(request.candidate, request.target_track)
    readiness_band, case_status, recommendation_stage = _readiness_band(context.score_breakdown.overall_score)

    ranked_market_roles = build_employer_demand_response(
        EmployerDemandRequest(
            candidate=request.candidate,
            track_id=request.target_track.track_id,
            limit=request.ranked_role_limit,
        )
    ).roles
    ojt_shortlist = build_ojt_match_response(
        OJTMatchRequest(
            candidate=request.candidate,
            target_track_id=request.target_track.track_id,
            limit=request.ranked_role_limit,
        )
    ).matches

    selected_role_id = request.selected_role_id
    if selected_role_id is None and ojt_shortlist:
        selected_role_id = ojt_shortlist[0].role_id
    if selected_role_id is None and ranked_market_roles:
        selected_role_id = ranked_market_roles[0].role_id

    wage_mobility = None
    if selected_role_id is not None:
        wage_mobility = estimate_wage_mobility(
            WageMobilityRequest(
                candidate=request.candidate,
                target_role_id=selected_role_id,
                current_wage=request.current_wage,
                current_sector=request.current_sector,
            )
        )

    candidate_master = ERPCandidateMaster(
        internal_candidate_id=request.candidate.candidate_id,
        external_candidate_id=request.external_candidate_id,
        education_level=request.candidate.education_level,
        degree_field=request.candidate.degree_field,
        district=request.candidate.district,
        state=request.candidate.state,
        willing_to_relocate=request.candidate.willing_to_relocate,
        effective_skill_tags=request.candidate.effective_skill_tags(),
        certifications=(request.candidate.resume_context.certifications if request.candidate.resume_context else []),
        inferred_role_signals=(request.candidate.resume_context.inferred_role_signals if request.candidate.resume_context else []),
        notes=request.candidate.notes,
    )
    training_case = ERPTrainingCase(
        internal_case_id=_build_case_id(request),
        external_case_id=request.external_case_id,
        target_track_id=request.target_track.track_id,
        target_track_name=request.target_track.track_name,
        track_location=f"{request.target_track.district}, {request.target_track.state}",
        required_skills=request.target_track.required_skills,
        target_roles=request.target_track.target_roles,
        top_skill_gaps=context.top_skill_gaps,
        missing_inputs=context.missing_inputs,
    )
    decision_summary = ERPDecisionSummary(
        overall_score=context.score_breakdown.overall_score,
        confidence_baseline=context.confidence_baseline,
        readiness_band=readiness_band,
        case_status=case_status,
        recommendation_stage=recommendation_stage,
        top_strengths=_top_strengths(context),
        top_skill_gaps=context.top_skill_gaps,
        summary_note=_summary_note(
            readiness_band,
            request,
            ojt_shortlist[0].role_title if ojt_shortlist else None,
        ),
    )
    status_map = ERPStatusMap(
        candidate_status=readiness_band,
        case_status=case_status,
        recommendation_stage=recommendation_stage,
        market_priority=_market_priority(ranked_market_roles, ojt_shortlist),
        mobility_band=_mobility_band(wage_mobility),
    )
    integration_id = _integration_id(request)
    upsert_keys = [
        ERPUpsertKey(
            entity="candidate_master",
            external_key=request.external_candidate_id or request.candidate.candidate_id,
        ),
        ERPUpsertKey(
            entity="training_case",
            external_key=request.external_case_id or training_case.internal_case_id,
        ),
        ERPUpsertKey(
            entity="decision_snapshot",
            external_key=f"{integration_id}:decision",
        ),
        ERPUpsertKey(
            entity="role_shortlist",
            external_key=f"{integration_id}:roles",
        ),
    ]
    if wage_mobility is not None:
        upsert_keys.append(
            ERPUpsertKey(
                entity="wage_scenario",
                external_key=f"{integration_id}:{wage_mobility.target_role_id}:wage",
            )
        )

    return ERPSyncPackage(
        schema_version=ERP_SCHEMA_VERSION,
        generated_at=generated_at,
        erp_system=request.erp_system,
        integration_id=integration_id,
        candidate_master=candidate_master,
        training_case=training_case,
        decision_summary=decision_summary,
        ranked_market_roles=ranked_market_roles,
        ojt_shortlist=ojt_shortlist,
        wage_mobility=wage_mobility,
        status_map=status_map,
        upsert_keys=upsert_keys,
        sync_actions=[
            "upsert_candidate_master",
            "upsert_training_case",
            "upsert_decision_snapshot",
            "upsert_role_shortlist",
            "upsert_wage_scenario" if wage_mobility is not None else "skip_wage_scenario",
        ],
    )