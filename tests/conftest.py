import pytest

from asem_talent.domain.models import CandidateDecisionRequest, CandidateProfile, TrainingTrack


@pytest.fixture
def sample_request() -> CandidateDecisionRequest:
    return CandidateDecisionRequest(
        candidate=CandidateProfile(
            candidate_id="cand_0001",
            age_band="22-24",
            education_level="bachelor_final_year",
            degree_field="mechatronics",
            district="Sepang",
            state="Selangor",
            latitude=2.9264,
            longitude=101.6964,
            skill_tags=["c++", "debugging", "data_acquisition", "embedded_systems"],
            portfolio_tags=["robot_arm", "debugging", "sensor_integration"],
            coding_test_score=74.0,
            math_foundation_score=69.0,
            communication_score=78.0,
            willing_to_relocate=True,
            prior_training=["basic_iot_bootcamp"],
            notes="Interested in validation and robotics workflows with structured mentoring.",
        ),
        target_track=TrainingTrack(
            track_id="track_validation",
            track_name="Chip Validation and Robotics Basics",
            district="Sepang",
            state="Selangor",
            required_skills=["debugging", "data_acquisition", "python_basics"],
            target_roles=["validation engineer trainee", "robotics trainee"],
            minimum_coding_score=60.0,
            minimum_math_score=60.0,
            employer_demand_signal=0.82,
            wage_growth_signal=0.73,
        ),
    )


@pytest.fixture
def request_with_missing_signals(sample_request: CandidateDecisionRequest) -> CandidateDecisionRequest:
    payload = sample_request.model_copy(deep=True)
    payload.candidate.communication_score = None
    payload.target_track.employer_demand_signal = None
    payload.target_track.wage_growth_signal = None
    payload.candidate.willing_to_relocate = None
    return payload
