from asem_talent.data.official_data import load_employer_roles, load_wage_signals
from asem_talent.domain.models import EmployerRole, WageMobilityRequest, WageMobilityResult, WageSignal
from asem_talent.services.resume_role_alignment import assess_resume_role_evidence


DEFAULT_WAGE_SECTOR_PRIORITY = ("formal_sector", "manufacturing")


def _lookup_wage_signal(state: str, sector: str | None = None) -> WageSignal | None:
    signals = load_wage_signals()
    preferred_sectors = []
    if sector:
        preferred_sectors.append(sector)
    for fallback_sector in DEFAULT_WAGE_SECTOR_PRIORITY:
        if fallback_sector not in preferred_sectors:
            preferred_sectors.append(fallback_sector)

    for preferred_sector in preferred_sectors:
        for signal in signals:
            if signal.state == state and signal.sector == preferred_sector and signal.metric == "median_formal_wage":
                return signal

    for signal in signals:
        if signal.state == state and signal.metric == "median_formal_wage":
            return signal
    return None


def _lookup_role(role_id: str) -> EmployerRole:
    for role in load_employer_roles():
        if role.role_id == role_id:
            return role
    raise KeyError(role_id)


def estimate_wage_mobility(request: WageMobilityRequest) -> WageMobilityResult:
    role = _lookup_role(request.target_role_id)
    current_sector = request.current_sector
    resume_evidence = assess_resume_role_evidence(request.candidate, role)

    if request.current_wage is not None:
        current_estimated_wage = request.current_wage
        current_source = "request.current_wage"
    else:
        current_signal = _lookup_wage_signal(request.candidate.state, current_sector)
        current_estimated_wage = current_signal.value if current_signal is not None else None
        current_sector_label = current_sector or DEFAULT_WAGE_SECTOR_PRIORITY[0]
        current_source = current_signal.source if current_signal is not None else f"UNSPECIFIED proxy for {request.candidate.state}/{current_sector_label}"

    if role.salary_band_min is not None or role.salary_band_max is not None:
        salary_floor = role.salary_band_min or role.salary_band_max or 0.0
        salary_ceiling = role.salary_band_max or role.salary_band_min or salary_floor
        target_estimated_wage = round((salary_floor + salary_ceiling) / 2, 2)
        target_source = role.source
    else:
        target_signal = _lookup_wage_signal(role.state)
        target_estimated_wage = target_signal.value if target_signal is not None else None
        target_source = target_signal.source if target_signal is not None else f"UNSPECIFIED proxy for {role.state}/{DEFAULT_WAGE_SECTOR_PRIORITY[0]}"

    if current_estimated_wage is not None and target_estimated_wage is not None:
        estimated_uplift_abs = round(target_estimated_wage - current_estimated_wage, 2)
        estimated_uplift_pct = round((estimated_uplift_abs / current_estimated_wage) * 100, 2) if current_estimated_wage else None
    else:
        estimated_uplift_abs = None
        estimated_uplift_pct = None

    if (
        request.current_wage is not None
        and role.salary_band_min is not None
        and role.salary_band_max is not None
        and resume_evidence.alignment_score >= 0.55
    ):
        evidence_strength = "high"
    elif current_estimated_wage is not None and target_estimated_wage is not None and request.candidate.resume_context is None:
        evidence_strength = "medium"
    elif current_estimated_wage is not None and target_estimated_wage is not None and resume_evidence.alignment_score >= 0.25:
        evidence_strength = "medium"
    else:
        evidence_strength = "low"

    base_caution_note = (
        "Current wage uses a user-provided value and target wage uses employer-demand salary band data."
        if request.current_wage is not None
        else "Current wage is estimated from the best available official wage baseline unless a direct wage is supplied."
    )
    caution_note = base_caution_note

    return WageMobilityResult(
        candidate_id=request.candidate.candidate_id,
        target_role_id=role.role_id,
        target_role_title=role.role_title,
        current_estimated_wage=current_estimated_wage,
        target_estimated_wage=target_estimated_wage,
        estimated_uplift_abs=estimated_uplift_abs,
        estimated_uplift_pct=estimated_uplift_pct,
        current_source=current_source,
        target_source=target_source,
        evidence_strength=evidence_strength,
        resume_alignment_score=resume_evidence.alignment_score,
        resume_evidence=resume_evidence.evidence,
        confidence_rationale=resume_evidence.summary,
        caution_note=caution_note,
        data_sources=sorted({current_source, target_source}),
    )