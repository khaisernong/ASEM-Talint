from asem_talent.data.official_data import load_employer_roles, load_semicon_hotspots, load_wage_signals
from asem_talent.domain.models import AccessibilityRequest, EmployerDemandRequest, OJTMatchRequest, ResumeContext, ResumeProject, WageMobilityRequest
from asem_talent.services.accessibility import build_accessibility_response
from asem_talent.services.employer_demand import build_employer_demand_response
from asem_talent.services.ojt_matching import build_ojt_match_response
from asem_talent.services.wage_mobility import estimate_wage_mobility


def test_official_data_loaders_return_fixture_slices() -> None:
    wages = load_wage_signals()
    roles = load_employer_roles()
    hotspots = load_semicon_hotspots()

    assert wages
    assert roles
    assert hotspots
    assert any(wage.state == "Selangor" and wage.metric == "median_formal_wage" for wage in wages)
    assert all(wage.source for wage in wages)


def test_accessibility_service_returns_ranked_destinations(sample_request) -> None:
    response = build_accessibility_response(AccessibilityRequest(candidate=sample_request.candidate, limit=2))

    assert response.candidate_id == "cand_0001"
    assert len(response.destinations) == 2
    assert response.destinations[0].destination_name == "IC Park 2 and ASEM"
    assert response.destinations[0].accessibility_score >= response.destinations[1].accessibility_score


def test_ojt_matching_returns_top_role_for_validation_track(sample_request) -> None:
    response = build_ojt_match_response(
        OJTMatchRequest(candidate=sample_request.candidate, target_track_id="track_validation", limit=3)
    )

    assert response.candidate_id == "cand_0001"
    assert response.matches[0].role_id == "role_validation_001"
    assert response.matches[0].match_score > 0.7


def test_ojt_matching_uses_resume_skill_evidence(sample_request) -> None:
    candidate = sample_request.candidate.model_copy(deep=True)
    candidate.skill_tags = ["debugging", "data_acquisition"]
    candidate.resume_context = ResumeContext(skill_tags=["python_basics"])

    response = build_ojt_match_response(
        OJTMatchRequest(candidate=candidate, target_track_id="track_validation", limit=1)
    )

    assert response.matches[0].skill_fit == 1.0
    assert "python_basics" not in response.matches[0].blockers


def test_wage_mobility_uses_role_salary_band_and_proxy_current_wage(sample_request) -> None:
    result = estimate_wage_mobility(
        WageMobilityRequest(candidate=sample_request.candidate, target_role_id="role_validation_001")
    )

    assert result.current_estimated_wage == 3127
    assert result.target_estimated_wage == 5750
    assert result.estimated_uplift_abs == 2623
    assert result.evidence_strength == "medium"
    assert result.current_source == "OpenDOSM formal sector wages dashboard"


def test_employer_demand_ranking_uses_resume_role_signals_and_projects(sample_request) -> None:
    candidate = sample_request.candidate.model_copy(deep=True)
    candidate.state = "Johor"
    candidate.resume_context = ResumeContext(
        inferred_role_signals=["embedded systems ojt"],
        certifications=["embedded_c_lab_badge"],
        project_highlights=[
            ResumeProject(
                title="Embedded sensor controller",
                skill_tags=["embedded_systems", "c++", "sensor_integration"],
                outcome_tags=["firmware_validation"],
            )
        ],
    )

    response = build_employer_demand_response(EmployerDemandRequest(candidate=candidate, state=None, limit=4))

    assert response.roles[0].role_id == "role_embedded_004"
    assert response.roles[0].market_signal_score > response.roles[1].market_signal_score
    assert response.roles[0].resume_alignment_score > 0.7
    assert any(item.startswith("Role signal:") for item in response.roles[0].resume_evidence)
    assert any(item.startswith("Project:") for item in response.roles[0].resume_evidence)


def test_wage_mobility_confidence_uses_resume_evidence(sample_request) -> None:
    candidate = sample_request.candidate.model_copy(deep=True)
    candidate.resume_context = ResumeContext(
        inferred_role_signals=["validation engineer trainee"],
        certifications=["ipc_basics"],
        project_highlights=[
            ResumeProject(
                title="Wafer validation bench",
                skill_tags=["python_basics", "debugging", "data_acquisition"],
                outcome_tags=["defect_detection"],
            )
        ],
    )

    result = estimate_wage_mobility(
        WageMobilityRequest(candidate=candidate, target_role_id="role_validation_001", current_wage=3200)
    )

    assert result.evidence_strength == "high"
    assert result.resume_alignment_score > 0.7
    assert any(item.startswith("Certification:") for item in result.resume_evidence)
    assert "Resume evidence used:" in result.confidence_rationale