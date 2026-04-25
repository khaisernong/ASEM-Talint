from fastapi.testclient import TestClient

from asem_talent.app import create_app
from asem_talent.domain.models import ResumeContext, ResumeProject


def test_erp_sync_package_endpoint_returns_operational_bundle(sample_request) -> None:
    client = TestClient(create_app())
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

    response = client.post(
        "/v1/erp/sync-package",
        json={
            "candidate": candidate.model_dump(mode="json"),
            "target_track": sample_request.target_track.model_dump(mode="json"),
            "erp_system": "ERPNext",
            "external_candidate_id": "ERP-CAND-1",
            "current_wage": 3300,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == "erp.sync.v1"
    assert body["candidate_master"]["external_candidate_id"] == "ERP-CAND-1"
    assert body["ranked_market_roles"][0]["role_id"] == "role_validation_001"
    assert body["ojt_shortlist"][0]["role_id"] == "role_validation_001"
    assert body["wage_mobility"]["target_role_id"] == "role_validation_001"
    assert body["status_map"]["market_priority"] in {"high", "medium", "low"}


def test_erp_sync_package_endpoint_rejects_unknown_selected_role(sample_request) -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/erp/sync-package",
        json={
            "candidate": sample_request.candidate.model_dump(mode="json"),
            "target_track": sample_request.target_track.model_dump(mode="json"),
            "selected_role_id": "role_missing_999",
        },
    )

    assert response.status_code == 404
    assert "Unknown selected_role_id" in response.json()["detail"]