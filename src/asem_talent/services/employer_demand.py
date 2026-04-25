from asem_talent.data.official_data import load_employer_roles
from asem_talent.domain.models import EmployerDemandRequest, EmployerDemandResponse, RankedEmployerRole
from asem_talent.services.resume_role_alignment import assess_resume_role_evidence


def build_employer_demand_response(request: EmployerDemandRequest) -> EmployerDemandResponse:
    roles = list(load_employer_roles())
    if request.state is not None:
        roles = [role for role in roles if role.state.lower() == request.state.lower()]
    if request.track_id is not None:
        roles = [role for role in roles if role.track_id == request.track_id]

    ranked_roles: list[RankedEmployerRole] = []
    for role in roles:
        resume_evidence = assess_resume_role_evidence(request.candidate, role)
        market_signal_score = round((0.6 * role.demand_score) + (0.4 * resume_evidence.alignment_score), 4)
        ranked_roles.append(
            RankedEmployerRole(
                **role.model_dump(),
                market_signal_score=market_signal_score,
                resume_alignment_score=resume_evidence.alignment_score,
                resume_evidence=resume_evidence.evidence,
                resume_evidence_summary=resume_evidence.summary,
            )
        )

    ranked_roles.sort(
        key=lambda role: (
            -role.market_signal_score,
            -role.resume_alignment_score,
            -role.demand_score,
            role.role_title,
        )
    )
    return EmployerDemandResponse(
        candidate_id=request.candidate.candidate_id,
        roles=ranked_roles[: request.limit],
        data_sources=sorted({role.source for role in roles}),
    )