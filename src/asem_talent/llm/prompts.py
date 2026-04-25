import json

from asem_talent.domain.models import CandidateDecisionRequest, CandidateProfile, DeterministicDecisionContext


SYSTEM_PROMPT = """You are the reasoning core for ASEM's semiconductor talent intelligence platform.
Return valid JSON only.
Explain the recommendation using visible evidence from the payload.
Do not fabricate missing values.
Do not output raw chain-of-thought.
Always surface missing_inputs, tradeoffs, confidence, and pathway_steps.
Treat resume_evidence as supporting structured context when it is provided.
"""


def _truncate_text(value: str | None, max_chars: int) -> str | None:
    if value is None or len(value) <= max_chars:
        return value
    return value[: max_chars - 3] + "..."


def _bounded_list(values: list[str], limit: int) -> list[str]:
    return [value for value in values if value][:limit]


def _build_resume_evidence(candidate: CandidateProfile, notes_max_chars: int) -> dict[str, object] | None:
    resume_context = candidate.resume_context
    if resume_context is None:
        return None

    summary_limit = min(notes_max_chars, 400)
    detail_limit = min(notes_max_chars, 180)
    evidence = {
        "summary": _truncate_text(resume_context.summary, summary_limit),
        "skill_tags": _bounded_list(resume_context.skill_tags, 8),
        "tool_tags": _bounded_list(resume_context.tool_tags, 8),
        "certifications": _bounded_list(resume_context.certifications, 5),
        "inferred_role_signals": _bounded_list(resume_context.inferred_role_signals, 5),
        "project_highlights": [
            {
                "title": project.title,
                "skill_tags": _bounded_list(project.skill_tags, 6),
                "summary": _truncate_text(project.summary, detail_limit),
            }
            for project in resume_context.project_highlights[:3]
        ],
        "internship_highlights": [
            {
                "organization": internship.organization,
                "role_title": internship.role_title,
                "skill_tags": _bounded_list(internship.skill_tags, 6),
                "summary": _truncate_text(internship.summary, detail_limit),
            }
            for internship in resume_context.internship_highlights[:2]
        ],
    }
    return {
        key: value
        for key, value in evidence.items()
        if value not in (None, [], "")
    }


def build_candidate_decision_messages(
    request: CandidateDecisionRequest,
    context: DeterministicDecisionContext,
    notes_max_chars: int,
) -> list[dict[str, str]]:
    candidate_payload = request.candidate.model_dump(mode="json", exclude={"resume_context"})
    candidate_payload["notes"] = _truncate_text(candidate_payload.get("notes"), notes_max_chars)

    user_payload = {
        "candidate": candidate_payload,
        "target_track": request.target_track.model_dump(mode="json"),
        "deterministic_context": context.model_dump(mode="json"),
        "required_response_fields": [
            "recommendation",
            "recommendation_type",
            "target_track_or_role",
            "explanation_summary",
            "top_factors",
            "missing_inputs",
            "tradeoffs",
            "confidence",
            "pathway_steps",
            "wage_note",
            "accessibility_note",
            "validation_notes",
        ],
    }
    resume_evidence = _build_resume_evidence(request.candidate, notes_max_chars)
    if resume_evidence is not None:
        user_payload["resume_evidence"] = resume_evidence

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(user_payload)},
    ]
