from fastapi.testclient import TestClient

from asem_talent.app import create_app


def test_wage_signals_endpoint_filters_by_state() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/signals/wages", params={"state": "Selangor"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["state"] == "Selangor"


def test_employer_demand_endpoint_filters_by_track() -> None:
    client = TestClient(create_app())

    response = client.get("/v1/signals/employer-demand", params={"track_id": "track_validation"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["role_id"] == "role_validation_001"


def test_ranked_employer_demand_endpoint_uses_resume_evidence() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/signals/employer-demand/ranked",
        json={
            "candidate": {
                "candidate_id": "cand_0002",
                "education_level": "bachelor_final_year",
                "degree_field": "computer_engineering",
                "district": "Johor Bahru",
                "state": "Johor",
                "skill_tags": ["c++"],
                "portfolio_tags": [],
                "resume_context": {
                    "inferred_role_signals": ["embedded systems ojt"],
                    "certifications": ["embedded_c_lab_badge"],
                    "project_highlights": [
                        {
                            "title": "Embedded sensor controller",
                            "skill_tags": ["embedded_systems", "c++", "sensor_integration"],
                            "outcome_tags": ["firmware_validation"]
                        }
                    ]
                }
            },
            "limit": 4
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["roles"][0]["role_id"] == "role_embedded_004"
    assert body["roles"][0]["resume_alignment_score"] > 0.7


def test_accessibility_endpoint_returns_hotspot_rankings(sample_request) -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/signals/accessibility",
        json={"candidate": sample_request.candidate.model_dump(mode="json"), "limit": 2},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_id"] == "cand_0001"
    assert len(body["destinations"]) == 2


def test_ojt_matching_endpoint_returns_ranked_matches(sample_request) -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/matching/ojt",
        json={"candidate": sample_request.candidate.model_dump(mode="json"), "target_track_id": "track_validation", "limit": 2},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["matches"][0]["role_id"] == "role_validation_001"


def test_wage_mobility_endpoint_returns_estimate(sample_request) -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/analysis/wage-mobility",
        json={"candidate": sample_request.candidate.model_dump(mode="json"), "target_role_id": "role_validation_001"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["target_role_id"] == "role_validation_001"
    assert body["current_estimated_wage"] == 3127
    assert body["estimated_uplift_abs"] == 2623
    assert body["resume_alignment_score"] == 0.0