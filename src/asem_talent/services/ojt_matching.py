from asem_talent.data.official_data import load_employer_roles
from asem_talent.domain.models import EmployerRole, OJTMatch, OJTMatchRequest, OJTMatchResponse
from asem_talent.services.accessibility import score_destination_access


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _overlap_score(observed: list[str], required: list[str]) -> float:
    if not required:
        return 0.0
    observed_set = {item.strip().lower() for item in observed}
    required_set = {item.strip().lower() for item in required}
    return len(observed_set & required_set) / len(required_set)


def _salary_fit(role: EmployerRole) -> float:
    if role.salary_band_min is None and role.salary_band_max is None:
        return 0.5
    salary_floor = role.salary_band_min or role.salary_band_max or 0.0
    salary_ceiling = role.salary_band_max or role.salary_band_min or salary_floor
    midpoint = (salary_floor + salary_ceiling) / 2
    return _clamp((midpoint - 3500.0) / 3500.0)


def build_ojt_match_response(request: OJTMatchRequest) -> OJTMatchResponse:
    roles = load_employer_roles()
    filtered_roles = [
        role for role in roles if request.target_track_id is None or role.track_id == request.target_track_id
    ]
    candidate_skill_tags = request.candidate.effective_skill_tags()
    candidate_skill_lookup = {item.lower() for item in candidate_skill_tags}

    matches = []
    for role in filtered_roles:
        skill_fit = _overlap_score(candidate_skill_tags, role.required_skills)
        track_fit = 1.0 if request.target_track_id is None or role.track_id == request.target_track_id else 0.35
        accessibility_score, distance_km, commute_note = score_destination_access(
            request.candidate,
            role.district,
            role.state,
            role.latitude,
            role.longitude,
        )
        wage_fit = _salary_fit(role)
        match_score = round(
            (0.35 * skill_fit)
            + (0.20 * track_fit)
            + (0.15 * accessibility_score)
            + (0.15 * wage_fit)
            + (0.15 * role.demand_score),
            4,
        )
        blockers = [
            skill for skill in role.required_skills if skill.lower() not in candidate_skill_lookup
        ][:3]
        justification = (
            f"Skill fit {skill_fit:.2f}, track fit {track_fit:.2f}, and accessibility {accessibility_score:.2f}"
            f" make {role.role_title} a credible OJT option."
        )

        matches.append(
            OJTMatch(
                role_id=role.role_id,
                employer_name=role.employer_name,
                role_title=role.role_title,
                track_id=role.track_id,
                match_score=match_score,
                skill_fit=round(skill_fit, 4),
                track_fit=round(track_fit, 4),
                accessibility_score=round(accessibility_score, 4),
                wage_fit=round(wage_fit, 4),
                demand_score=role.demand_score,
                blockers=blockers,
                justification=justification,
                commute_note=commute_note,
                distance_km=distance_km,
                salary_band_min=role.salary_band_min,
                salary_band_max=role.salary_band_max,
            )
        )

    ranked_matches = sorted(matches, key=lambda item: (-item.match_score, len(item.blockers), item.role_title))
    return OJTMatchResponse(
        candidate_id=request.candidate.candidate_id,
        matches=ranked_matches[: request.limit],
        data_sources=sorted({role.source for role in filtered_roles}),
    )