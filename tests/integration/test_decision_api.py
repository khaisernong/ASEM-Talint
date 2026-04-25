from fastapi.testclient import TestClient

from asem_talent.api.dependencies import get_decision_engine, get_ilmu_decision_engine
from asem_talent.app import create_app
from asem_talent.config import get_settings
from asem_talent.domain.models import DecisionExplanation, ProviderUsage, ResumeContext
from asem_talent.services.decision_engine import DecisionEngine


class FakeProvider:
    def explain_candidate_track_fit(self, request, context):
        return (
            DecisionExplanation(
                recommendation="Advance the candidate to the validation track.",
                recommendation_type="track_fit",
                target_track_or_role=request.target_track.track_name,
                explanation_summary="The candidate aligns with the requested track based on deterministic readiness signals.",
                top_factors=["skill overlap", "communication score", "local access"],
                missing_inputs=context.missing_inputs,
                tradeoffs=["Python fundamentals still need reinforcement"],
                confidence=context.confidence_baseline,
                pathway_steps=["Finish Python basics", "Proceed to cohort review"],
                wage_note="Wage output remains a scenario estimate pending official data integration.",
                accessibility_note="Candidate and cohort are in the same district.",
                validation_notes=["Integration test fixture"],
            ),
            ProviderUsage(model="test-double", total_tokens=123, latency_ms=3),
        )


def test_candidate_track_fit_endpoint_returns_structured_response(sample_request) -> None:
    app = create_app()
    app.dependency_overrides[get_decision_engine] = lambda: DecisionEngine(provider=FakeProvider())
    client = TestClient(app)

    response = client.post(
        "/v1/decisions/candidate-track-fit",
        json=sample_request.model_dump(mode="json"),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_id"] == "cand_0001"
    assert body["explanation"]["recommendation_type"] == "track_fit"
    assert body["usage"]["total_tokens"] == 123


def test_candidate_track_fit_ilmu_endpoint_returns_structured_response(sample_request) -> None:
    app = create_app()
    app.dependency_overrides[get_ilmu_decision_engine] = lambda: DecisionEngine(provider=FakeProvider())
    client = TestClient(app)

    response = client.post(
        "/v1/decisions/candidate-track-fit/ilmu",
        json=sample_request.model_dump(mode="json"),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_id"] == "cand_0001"
    assert body["explanation"]["recommendation_type"] == "track_fit"
    assert body["usage"]["total_tokens"] == 123


def test_dashboard_root_returns_html() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "ASEM Talint Dashboard" in response.text
    assert 'aria-label="ASEM Talint logo"' in response.text
    assert "Local capability, not just placement" in response.text
    assert "Run ILMU route" in response.text
    assert "Run local preview" in response.text
    assert "Parse resume" in response.text
    assert "Candidate Lab" in response.text
    assert "Market Studio" in response.text
    assert "Pathway Planner" in response.text
    assert "ERP Bridge" in response.text


def test_candidate_lab_page_returns_html() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/candidate-lab")

    assert response.status_code == 200
    assert "ASEM Talint Candidate Lab" in response.text
    assert 'aria-label="ASEM Talint logo"' in response.text
    assert "Repair queue" in response.text
    assert "Coach notes" in response.text


def test_market_studio_page_returns_html() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/market-studio")

    assert response.status_code == 200
    assert "ASEM Talint Market Studio" in response.text
    assert "Contribution by role" in response.text
    assert "Refresh roles" in response.text


def test_pathway_planner_page_returns_html() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/pathway-planner")

    assert response.status_code == 200
    assert "ASEM Talint Pathway Planner" in response.text
    assert "30-60-90 plan" in response.text
    assert "Rebuild plan" in response.text


def test_erp_bridge_page_returns_html() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/erp-bridge")

    assert response.status_code == 200
    assert "ASEM Talint ERP Bridge" in response.text
    assert "Package builder" in response.text
    assert "Copy package JSON" in response.text


def test_health_endpoint_reports_provider_readiness_when_optional_routes_are_unconfigured(monkeypatch) -> None:
    monkeypatch.setenv("ZAI_API_KEY", "UNSPECIFIED")
    monkeypatch.setenv("GLM_MODEL", "UNSPECIFIED")
    monkeypatch.setenv("ILMU_API_KEY", "UNSPECIFIED")
    monkeypatch.setenv("ILMU_BASE_URL", "UNSPECIFIED")
    monkeypatch.setenv("ILMU_MODEL", "UNSPECIFIED")
    get_settings.cache_clear()

    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["live_provider_ready"] is False
    assert body["zai_provider_ready"] is False
    assert body["ilmu_provider_ready"] is False
    assert "ZAI_API_KEY" in body["live_provider_message"]
    assert "ILMU_API_KEY" in body["ilmu_provider_message"]

    get_settings.cache_clear()


def test_candidate_track_fit_demo_returns_degraded_response(sample_request) -> None:
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/v1/decisions/candidate-track-fit/demo",
        json=sample_request.model_dump(mode="json"),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["usage"]["model"] == "demo-heuristic"
    assert body["explanation"]["recommendation_type"] == "track_fit_demo"
    assert "DEGRADED" in body["explanation"]["validation_notes"][0]


def test_candidate_track_fit_endpoint_accepts_resume_context(sample_request) -> None:
    app = create_app()
    app.dependency_overrides[get_decision_engine] = lambda: DecisionEngine(provider=FakeProvider())
    client = TestClient(app)
    request = sample_request.model_copy(deep=True)
    request.candidate.skill_tags = ["debugging", "data_acquisition"]
    request.candidate.resume_context = ResumeContext(
        summary="Built validation scripts during a lab placement.",
        skill_tags=["python_basics"],
    )

    response = client.post(
        "/v1/decisions/candidate-track-fit",
        json=request.model_dump(mode="json"),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["context"]["score_breakdown"]["toolchain_alignment"] == 1.0
    assert "python_basics" not in body["context"]["top_skill_gaps"]


def test_candidate_track_fit_endpoint_rejects_invalid_payload() -> None:
    app = create_app()
    app.dependency_overrides[get_decision_engine] = lambda: DecisionEngine(provider=FakeProvider())
    client = TestClient(app)

    response = client.post(
        "/v1/decisions/candidate-track-fit",
        json={"candidate": {"candidate_id": "cand_0001"}, "target_track": {"track_id": "track_validation"}},
    )

    assert response.status_code == 422