import json

import pytest

from asem_talent.domain.models import DecisionExplanation, ProviderUsage, ResumeContext, ResumeInternship, ResumeProject
from asem_talent.domain.scoring import build_decision_context
from asem_talent.llm.ilmu_provider import ILMUProvider, ILMU_COMPACT_JSON_INSTRUCTIONS
from asem_talent.llm.prompts import build_candidate_decision_messages
from asem_talent.llm.provider import DecisionProviderError
from asem_talent.llm.zai_provider import ZAIProvider


class FakeHTTPResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


class RecordingClient:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.last_url: str | None = None
        self.last_json: dict | None = None
        self.last_headers: dict | None = None

    def post(self, url: str, json: dict, headers: dict) -> FakeHTTPResponse:
        self.last_url = url
        self.last_json = json
        self.last_headers = headers
        return FakeHTTPResponse(self.payload)


class SequencedClient:
    def __init__(self, payloads: list[dict]) -> None:
        self.payloads = payloads
        self.calls = 0

    def post(self, url: str, json: dict, headers: dict) -> FakeHTTPResponse:
        payload = self.payloads[min(self.calls, len(self.payloads) - 1)]
        self.calls += 1
        return FakeHTTPResponse(payload)


def test_build_candidate_decision_messages_truncates_notes(sample_request) -> None:
    sample_request.candidate.notes = "x" * 80
    context = build_decision_context(sample_request.candidate, sample_request.target_track)

    messages = build_candidate_decision_messages(sample_request, context, notes_max_chars=20)
    user_payload = json.loads(messages[1]["content"])

    assert user_payload["candidate"]["notes"].endswith("...")
    assert len(user_payload["candidate"]["notes"]) == 20


def test_build_candidate_decision_messages_compacts_resume_evidence(sample_request) -> None:
    sample_request.candidate.resume_context = ResumeContext(
        summary="r" * 80,
        skill_tags=["python_basics", "debugging"],
        tool_tags=["oscilloscope"],
        project_highlights=[
            ResumeProject(
                title="Wafer inspection prototype",
                summary="p" * 70,
                skill_tags=["python_basics", "sensor_integration"],
            )
        ],
        internship_highlights=[
            ResumeInternship(
                organization="ASEM Partner Lab",
                role_title="Automation Intern",
                summary="i" * 70,
                skill_tags=["data_acquisition", "debugging"],
            )
        ],
        certifications=["ipc_basics"],
        inferred_role_signals=["validation engineer trainee"],
    )
    context = build_decision_context(sample_request.candidate, sample_request.target_track)

    messages = build_candidate_decision_messages(sample_request, context, notes_max_chars=20)
    user_payload = json.loads(messages[1]["content"])

    assert "resume_context" not in user_payload["candidate"]
    assert user_payload["resume_evidence"]["summary"].endswith("...")
    assert len(user_payload["resume_evidence"]["summary"]) == 20
    assert user_payload["resume_evidence"]["project_highlights"][0]["summary"].endswith("...")


def test_parse_explanation_response_returns_usage(sample_request) -> None:
    context = build_decision_context(sample_request.candidate, sample_request.target_track)
    provider = ZAIProvider(
        api_key="test-key",
        base_url="https://example.com/v4",
        model_name="glm-test",
        timeout_seconds=10,
        max_tokens=1200,
        temperature=0.1,
        notes_max_chars=200,
    )
    response_payload = {
        "id": "req_123",
        "model": "glm-test",
        "usage": {"prompt_tokens": 110, "completion_tokens": 90, "total_tokens": 200},
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "recommendation": "Advance to the validation cohort.",
                            "recommendation_type": "track_fit",
                            "target_track_or_role": sample_request.target_track.track_name,
                            "explanation_summary": "Deterministic signals indicate a strong fit.",
                            "top_factors": ["debugging overlap", "same-district access"],
                            "missing_inputs": context.missing_inputs,
                            "tradeoffs": ["Python skill remains partial"],
                            "confidence": context.confidence_baseline,
                            "pathway_steps": ["Complete Python basics", "Enter cohort"],
                            "wage_note": "Wage signal depends on future official integration.",
                            "accessibility_note": "Candidate already sits in the same district.",
                            "validation_notes": ["Schema validated."],
                        }
                    )
                }
            }
        ],
    }

    explanation, usage = provider._parse_explanation_response(response_payload, latency_ms=37)

    assert isinstance(explanation, DecisionExplanation)
    assert isinstance(usage, ProviderUsage)
    assert usage.total_tokens == 200
    assert usage.latency_ms == 37


def test_explain_candidate_track_fit_supports_openbigmodel_compatible_base_url(sample_request) -> None:
    context = build_decision_context(sample_request.candidate, sample_request.target_track)
    response_payload = {
        "id": "req_compat",
        "model": "glm-4",
        "usage": {"prompt_tokens": 64, "completion_tokens": 32, "total_tokens": 96},
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "recommendation": "Advance to the validation cohort.",
                            "recommendation_type": "track_fit",
                            "target_track_or_role": sample_request.target_track.track_name,
                            "explanation_summary": "Deterministic readiness and resume-aligned evidence support the track.",
                            "top_factors": ["skill overlap", "same-district access"],
                            "missing_inputs": context.missing_inputs,
                            "tradeoffs": ["Python depth still needs reinforcement"],
                            "confidence": context.confidence_baseline,
                            "pathway_steps": ["Complete Python basics", "Proceed to cohort"],
                            "wage_note": "Wage estimate uses official baseline data.",
                            "accessibility_note": "Candidate remains locally accessible to the cohort.",
                            "validation_notes": ["Compatibility test fixture"],
                        }
                    )
                }
            }
        ],
    }
    client = RecordingClient(response_payload)
    provider = ZAIProvider(
        api_key="test-key",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        model_name="glm-4",
        timeout_seconds=10,
        max_tokens=1200,
        temperature=0.1,
        notes_max_chars=200,
        client=client,
    )

    explanation, usage = provider.explain_candidate_track_fit(sample_request, context)

    assert explanation.recommendation_type == "track_fit"
    assert usage.model == "glm-4"
    assert client.last_url == "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    assert client.last_json is not None
    assert client.last_json["model"] == "glm-4"
    assert client.last_headers == {
        "Authorization": "Bearer test-key",
        "Content-Type": "application/json",
    }


def test_parse_explanation_response_rejects_invalid_contract() -> None:
    provider = ZAIProvider(
        api_key="test-key",
        base_url="https://example.com/v4",
        model_name="glm-test",
        timeout_seconds=10,
        max_tokens=1200,
        temperature=0.1,
        notes_max_chars=200,
    )
    invalid_payload = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "recommendation": "Advance to the validation cohort."
                        }
                    )
                }
            }
        ]
    }

    with pytest.raises(DecisionProviderError):
        provider._parse_explanation_response(invalid_payload, latency_ms=20)


def test_ilmu_provider_supports_configured_openai_compatible_base_url(sample_request) -> None:
    context = build_decision_context(sample_request.candidate, sample_request.target_track)
    response_payload = {
        "id": "req_ilmu",
        "model": "ilmu-test",
        "usage": {"prompt_tokens": 52, "completion_tokens": 28, "total_tokens": 80},
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "recommendation": "Advance to the validation cohort.",
                            "recommendation_type": "track_fit",
                            "target_track_or_role": sample_request.target_track.track_name,
                            "explanation_summary": "Configured ILMU compatibility path returns the same structured contract.",
                            "top_factors": ["skill overlap", "same-district access"],
                            "missing_inputs": context.missing_inputs,
                            "tradeoffs": ["Python depth still needs reinforcement"],
                            "confidence": context.confidence_baseline,
                            "pathway_steps": ["Complete Python basics", "Proceed to cohort"],
                            "wage_note": "Wage estimate uses official baseline data.",
                            "accessibility_note": "Candidate remains locally accessible to the cohort.",
                            "validation_notes": ["ILMU compatibility test fixture"],
                        }
                    )
                }
            }
        ],
    }
    client = RecordingClient(response_payload)
    provider = ILMUProvider(
        api_key="test-key",
        base_url="https://api.ilmu.example/v1/",
        model_name="ilmu-test",
        timeout_seconds=10,
        max_tokens=1200,
        temperature=0.1,
        notes_max_chars=200,
        client=client,
    )

    explanation, usage = provider.explain_candidate_track_fit(sample_request, context)

    assert explanation.recommendation_type == "track_fit"
    assert usage.model == "ilmu-test"
    assert client.last_url == "https://api.ilmu.example/v1/chat/completions"
    assert client.last_json is not None
    assert ILMU_COMPACT_JSON_INSTRUCTIONS in client.last_json["messages"][0]["content"]
    assert client.last_headers == {
        "Authorization": "Bearer test-key",
        "Content-Type": "application/json",
    }


def test_parse_explanation_response_accepts_fenced_json() -> None:
    provider = ILMUProvider(
        api_key="test-key",
        base_url="https://api.ilmu.example/v1/",
        model_name="ilmu-test",
        timeout_seconds=10,
        max_tokens=1800,
        temperature=0.1,
        notes_max_chars=200,
    )
    fenced_payload = {
        "id": "req_fenced",
        "model": "ilmu-test",
        "choices": [
            {
                "message": {
                    "content": "```json\n{\"recommendation\":\"Proceed\",\"recommendation_type\":\"track_fit\",\"target_track_or_role\":\"Track\",\"explanation_summary\":\"Short summary\",\"top_factors\":[\"factor\"],\"missing_inputs\":[],\"tradeoffs\":[\"tradeoff\"],\"confidence\":0.9,\"pathway_steps\":[\"step\"],\"wage_note\":\"wage\",\"accessibility_note\":\"access\",\"validation_notes\":[\"ok\"]}\n```"
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
    }

    explanation, usage = provider._parse_explanation_response(fenced_payload, latency_ms=20)

    assert explanation.recommendation == "Proceed"
    assert usage.total_tokens == 30


def test_ilmu_provider_raises_clear_error_when_response_has_no_visible_content() -> None:
    provider = ILMUProvider(
        api_key="test-key",
        base_url="https://api.ilmu.example/v1/",
        model_name="ilmu-test",
        timeout_seconds=10,
        max_tokens=1200,
        temperature=0.1,
        notes_max_chars=200,
    )
    invalid_payload = {
        "id": "req_ilmu",
        "model": "ilmu-test",
        "choices": [
            {
                "message": {"role": "assistant", "content": None, "tool_calls": None},
                "finish_reason": "length",
            }
        ],
        "usage": {"prompt_tokens": 389, "completion_tokens": 1200, "total_tokens": 1589},
    }

    with pytest.raises(DecisionProviderError, match="returned no assistant content") as error:
        provider._parse_explanation_response(invalid_payload, latency_ms=20)

    assert "finish_reason=length" in str(error.value)


def test_ilmu_provider_retries_after_invalid_response_payload(sample_request) -> None:
    context = build_decision_context(sample_request.candidate, sample_request.target_track)
    invalid_payload = {
        "id": "req_bad",
        "model": "ilmu-test",
        "choices": [{"message": {"content": "{"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
    }
    valid_payload = {
        "id": "req_good",
        "model": "ilmu-test",
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "recommendation": "Proceed",
                            "recommendation_type": "track_fit",
                            "target_track_or_role": sample_request.target_track.track_name,
                            "explanation_summary": "Compact valid response.",
                            "top_factors": ["factor"],
                            "missing_inputs": [],
                            "tradeoffs": ["tradeoff"],
                            "confidence": context.confidence_baseline,
                            "pathway_steps": ["step"],
                            "wage_note": "wage",
                            "accessibility_note": "access",
                            "validation_notes": ["ok"],
                        }
                    )
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
    }
    provider = ILMUProvider(
        api_key="test-key",
        base_url="https://api.ilmu.example/v1/",
        model_name="ilmu-test",
        timeout_seconds=10,
        max_tokens=1800,
        temperature=0.1,
        notes_max_chars=120,
        retry_attempts=1,
        client=SequencedClient([invalid_payload, valid_payload]),
    )

    explanation, usage = provider.explain_candidate_track_fit(sample_request, context)

    assert explanation.recommendation == "Proceed"
    assert usage.request_id == "req_good"
