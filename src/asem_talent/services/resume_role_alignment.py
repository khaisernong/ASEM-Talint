from dataclasses import dataclass
import re

from asem_talent.domain.models import CandidateProfile, EmployerRole


ROLE_STOPWORDS = {
    "and",
    "associate",
    "engineer",
    "engineering",
    "for",
    "intern",
    "junior",
    "ojt",
    "role",
    "senior",
    "systems",
    "technician",
    "test",
    "trainee",
    "with",
}
TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class ResumeRoleEvidence:
    alignment_score: float
    evidence: list[str]
    summary: str


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _tokenize(value: str) -> set[str]:
    return {match.group(0) for match in TOKEN_RE.finditer(value.lower())}


def _meaningful_tokens(value: str) -> set[str]:
    return _tokenize(value) - ROLE_STOPWORDS


def _overlap_score(observed: list[str], required: list[str]) -> float:
    if not observed or not required:
        return 0.0
    observed_set = {item.strip().lower() for item in observed if item.strip()}
    required_set = {item.strip().lower() for item in required if item.strip()}
    if not required_set:
        return 0.0
    return len(observed_set & required_set) / len(required_set)


def assess_resume_role_evidence(candidate: CandidateProfile, role: EmployerRole) -> ResumeRoleEvidence:
    resume_context = candidate.resume_context
    if resume_context is None:
        return ResumeRoleEvidence(
            alignment_score=0.0,
            evidence=[],
            summary="No structured resume evidence was supplied for role-specific personalization.",
        )

    role_tokens = set(role.required_skills)
    role_tokens.update(_meaningful_tokens(role.role_title))
    role_tokens.update(_meaningful_tokens(" ".join(role.preferred_degree_fields)))

    role_signal_hits: list[str] = []
    for signal in resume_context.inferred_role_signals:
        if _meaningful_tokens(signal) & role_tokens:
            role_signal_hits.append(signal)
    for internship in resume_context.internship_highlights:
        if _meaningful_tokens(internship.role_title) & role_tokens:
            role_signal_hits.append(internship.role_title)
    role_signal_hits = list(dict.fromkeys(role_signal_hits))
    role_signal_score = 1.0 if role_signal_hits else 0.0

    project_hits: list[str] = []
    project_score = 0.0
    for project in resume_context.project_highlights:
        project_skill_score = _overlap_score(project.skill_tags + project.outcome_tags, role.required_skills)
        title_overlap = 1.0 if _meaningful_tokens(project.title) & role_tokens else 0.0
        current_score = max(project_skill_score, 0.55 if title_overlap else 0.0)
        if current_score > 0.0:
            project_hits.append(project.title)
            project_score = max(project_score, current_score)
    project_hits = list(dict.fromkeys(project_hits))

    certification_hits: list[str] = []
    for certification in resume_context.certifications:
        certification_tokens = _meaningful_tokens(certification)
        if certification_tokens & role_tokens:
            certification_hits.append(certification)
    if certification_hits:
        certification_score = min(1.0, 0.65 + (0.15 * max(0, len(certification_hits) - 1)))
    elif resume_context.certifications:
        certification_hits = resume_context.certifications[:2]
        certification_score = min(0.5, 0.25 * len(certification_hits))
    else:
        certification_score = 0.0

    alignment_score = round(
        _clamp((0.5 * role_signal_score) + (0.2 * certification_score) + (0.3 * project_score)),
        4,
    )

    evidence: list[str] = []
    evidence.extend(f"Role signal: {value}" for value in role_signal_hits[:2])
    evidence.extend(f"Certification: {value}" for value in certification_hits[:2])
    evidence.extend(f"Project: {value}" for value in project_hits[:2])

    summary_parts: list[str] = []
    if role_signal_hits:
        summary_parts.append(f"role signals matched {', '.join(role_signal_hits[:2])}")
    if certification_hits:
        summary_parts.append(f"certifications considered {', '.join(certification_hits[:2])}")
    if project_hits:
        summary_parts.append(f"project evidence from {', '.join(project_hits[:2])}")

    if summary_parts:
        summary = f"Resume evidence used: {'; '.join(summary_parts)}."
    else:
        summary = "Resume context exists, but no strong role-specific signals, certifications, or project evidence matched this role."

    return ResumeRoleEvidence(
        alignment_score=alignment_score,
        evidence=evidence,
        summary=summary,
    )