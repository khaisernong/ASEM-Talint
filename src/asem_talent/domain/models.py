from pydantic import BaseModel, Field


def _dedupe_tags(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        lookup_key = normalized.lower()
        if lookup_key in seen:
            continue
        seen.add(lookup_key)
        deduped.append(normalized)
    return deduped


class ResumeProject(BaseModel):
    title: str
    summary: str | None = None
    skill_tags: list[str] = Field(default_factory=list)
    outcome_tags: list[str] = Field(default_factory=list)


class ResumeInternship(BaseModel):
    organization: str
    role_title: str
    summary: str | None = None
    skill_tags: list[str] = Field(default_factory=list)


class ResumeContext(BaseModel):
    summary: str | None = None
    skill_tags: list[str] = Field(default_factory=list)
    tool_tags: list[str] = Field(default_factory=list)
    project_highlights: list[ResumeProject] = Field(default_factory=list)
    internship_highlights: list[ResumeInternship] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    inferred_role_signals: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    candidate_id: str
    age_band: str | None = None
    education_level: str
    degree_field: str
    district: str
    state: str
    latitude: float | None = None
    longitude: float | None = None
    skill_tags: list[str] = Field(default_factory=list)
    portfolio_tags: list[str] = Field(default_factory=list)
    coding_test_score: float | None = None
    math_foundation_score: float | None = None
    communication_score: float | None = None
    willing_to_relocate: bool | None = None
    prior_training: list[str] = Field(default_factory=list)
    notes: str | None = None
    resume_context: ResumeContext | None = None

    def effective_skill_tags(self) -> list[str]:
        merged_tags = list(self.skill_tags)
        if self.resume_context is not None:
            merged_tags.extend(self.resume_context.skill_tags)
            merged_tags.extend(self.resume_context.tool_tags)
            for project in self.resume_context.project_highlights:
                merged_tags.extend(project.skill_tags)
            for internship in self.resume_context.internship_highlights:
                merged_tags.extend(internship.skill_tags)
        return _dedupe_tags(merged_tags)

    def effective_portfolio_tags(self) -> list[str]:
        merged_tags = list(self.portfolio_tags)
        if self.resume_context is not None:
            merged_tags.extend(self.resume_context.certifications)
            merged_tags.extend(self.resume_context.inferred_role_signals)
            for project in self.resume_context.project_highlights:
                merged_tags.append(project.title)
                merged_tags.extend(project.skill_tags)
                merged_tags.extend(project.outcome_tags)
            for internship in self.resume_context.internship_highlights:
                merged_tags.append(internship.role_title)
                merged_tags.extend(internship.skill_tags)
        return _dedupe_tags(merged_tags)


class TrainingTrack(BaseModel):
    track_id: str
    track_name: str
    district: str
    state: str
    required_skills: list[str] = Field(default_factory=list)
    target_roles: list[str] = Field(default_factory=list)
    minimum_coding_score: float | None = None
    minimum_math_score: float | None = None
    employer_demand_signal: float | None = Field(default=None, ge=0.0, le=1.0)
    wage_growth_signal: float | None = Field(default=None, ge=0.0, le=1.0)


class SuitabilityBreakdown(BaseModel):
    toolchain_alignment: float
    foundational_readiness: float
    portfolio_relevance: float
    communication_readiness: float
    accessibility_score: float
    completion_likelihood: float
    wage_uplift_potential: float
    employer_demand_alignment: float
    overall_score: float


class DeterministicDecisionContext(BaseModel):
    score_breakdown: SuitabilityBreakdown
    top_skill_gaps: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)
    confidence_baseline: float = Field(ge=0.0, le=1.0)


class DecisionExplanation(BaseModel):
    recommendation: str
    recommendation_type: str
    target_track_or_role: str
    explanation_summary: str
    top_factors: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)
    tradeoffs: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    pathway_steps: list[str] = Field(default_factory=list)
    wage_note: str
    accessibility_note: str
    validation_notes: list[str] = Field(default_factory=list)


class ProviderUsage(BaseModel):
    request_id: str | None = None
    model: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None


class CandidateDecisionRequest(BaseModel):
    candidate: CandidateProfile
    target_track: TrainingTrack


class CandidateDecisionResult(BaseModel):
    candidate_id: str
    target_track_id: str
    context: DeterministicDecisionContext
    explanation: DecisionExplanation
    usage: ProviderUsage


class ResumeParseResponse(BaseModel):
    file_name: str
    file_type: str
    file_size_bytes: int
    redacted_preview: str
    redaction_counts: dict[str, int] = Field(default_factory=dict)
    truncated: bool = False
    warnings: list[str] = Field(default_factory=list)
    resume_context: ResumeContext


class WageSignal(BaseModel):
    date: str
    state: str
    district: str | None = None
    sector: str
    metric: str
    value: float
    currency: str = "MYR"
    source: str


class EmployerRole(BaseModel):
    employer_id: str
    employer_name: str
    facility_name: str
    district: str
    state: str
    role_id: str
    role_title: str
    track_id: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_degree_fields: list[str] = Field(default_factory=list)
    openings: int = 0
    onsite_requirement: bool = True
    salary_band_min: float | None = None
    salary_band_max: float | None = None
    demand_score: float = Field(default=0.5, ge=0.0, le=1.0)
    latitude: float | None = None
    longitude: float | None = None
    source: str


class RankedEmployerRole(EmployerRole):
    market_signal_score: float = Field(default=0.0, ge=0.0, le=1.0)
    resume_alignment_score: float = Field(default=0.0, ge=0.0, le=1.0)
    resume_evidence: list[str] = Field(default_factory=list)
    resume_evidence_summary: str = ""


class EmployerDemandRequest(BaseModel):
    candidate: CandidateProfile
    state: str | None = None
    track_id: str | None = None
    limit: int = Field(default=5, ge=1, le=20)


class EmployerDemandResponse(BaseModel):
    candidate_id: str
    roles: list[RankedEmployerRole] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)


class SemiconHotspot(BaseModel):
    hotspot_id: str
    hotspot_name: str
    hotspot_type: str
    district: str
    state: str
    latitude: float | None = None
    longitude: float | None = None
    evidence_tag: str
    source: str


class AccessibilityDestination(BaseModel):
    destination_id: str
    destination_name: str
    destination_type: str
    district: str
    state: str
    latitude: float | None = None
    longitude: float | None = None
    accessibility_score: float = Field(ge=0.0, le=1.0)
    distance_km: float | None = None
    note: str


class AccessibilityRequest(BaseModel):
    candidate: CandidateProfile
    limit: int = Field(default=3, ge=1, le=10)


class AccessibilityResponse(BaseModel):
    candidate_id: str
    destinations: list[AccessibilityDestination] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)


class OJTMatchRequest(BaseModel):
    candidate: CandidateProfile
    target_track_id: str | None = None
    limit: int = Field(default=5, ge=1, le=10)


class OJTMatch(BaseModel):
    role_id: str
    employer_name: str
    role_title: str
    track_id: str
    match_score: float = Field(ge=0.0, le=1.0)
    skill_fit: float = Field(ge=0.0, le=1.0)
    track_fit: float = Field(ge=0.0, le=1.0)
    accessibility_score: float = Field(ge=0.0, le=1.0)
    wage_fit: float = Field(ge=0.0, le=1.0)
    demand_score: float = Field(ge=0.0, le=1.0)
    blockers: list[str] = Field(default_factory=list)
    justification: str
    commute_note: str
    distance_km: float | None = None
    salary_band_min: float | None = None
    salary_band_max: float | None = None


class OJTMatchResponse(BaseModel):
    candidate_id: str
    matches: list[OJTMatch] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)


class WageMobilityRequest(BaseModel):
    candidate: CandidateProfile
    target_role_id: str
    current_wage: float | None = None
    current_sector: str | None = None


class WageMobilityResult(BaseModel):
    candidate_id: str
    target_role_id: str
    target_role_title: str
    current_estimated_wage: float | None = None
    target_estimated_wage: float | None = None
    estimated_uplift_abs: float | None = None
    estimated_uplift_pct: float | None = None
    current_source: str
    target_source: str
    evidence_strength: str
    resume_alignment_score: float = Field(default=0.0, ge=0.0, le=1.0)
    resume_evidence: list[str] = Field(default_factory=list)
    confidence_rationale: str = ""
    caution_note: str
    data_sources: list[str] = Field(default_factory=list)


class ERPSyncRequest(BaseModel):
    candidate: CandidateProfile
    target_track: TrainingTrack
    erp_system: str = "UNSPECIFIED"
    external_candidate_id: str | None = None
    external_case_id: str | None = None
    current_wage: float | None = None
    current_sector: str | None = None
    selected_role_id: str | None = None
    ranked_role_limit: int = Field(default=3, ge=1, le=10)


class ERPCandidateMaster(BaseModel):
    internal_candidate_id: str
    external_candidate_id: str | None = None
    education_level: str
    degree_field: str
    district: str
    state: str
    willing_to_relocate: bool | None = None
    effective_skill_tags: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    inferred_role_signals: list[str] = Field(default_factory=list)
    notes: str | None = None


class ERPTrainingCase(BaseModel):
    internal_case_id: str
    external_case_id: str | None = None
    target_track_id: str
    target_track_name: str
    track_location: str
    required_skills: list[str] = Field(default_factory=list)
    target_roles: list[str] = Field(default_factory=list)
    top_skill_gaps: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)


class ERPDecisionSummary(BaseModel):
    overall_score: float = Field(ge=0.0, le=1.0)
    confidence_baseline: float = Field(ge=0.0, le=1.0)
    readiness_band: str
    case_status: str
    recommendation_stage: str
    top_strengths: list[str] = Field(default_factory=list)
    top_skill_gaps: list[str] = Field(default_factory=list)
    summary_note: str


class ERPStatusMap(BaseModel):
    candidate_status: str
    case_status: str
    recommendation_stage: str
    market_priority: str
    mobility_band: str


class ERPUpsertKey(BaseModel):
    entity: str
    external_key: str


class ERPSyncPackage(BaseModel):
    schema_version: str
    generated_at: str
    erp_system: str
    integration_id: str
    candidate_master: ERPCandidateMaster
    training_case: ERPTrainingCase
    decision_summary: ERPDecisionSummary
    ranked_market_roles: list[RankedEmployerRole] = Field(default_factory=list)
    ojt_shortlist: list[OJTMatch] = Field(default_factory=list)
    wage_mobility: WageMobilityResult | None = None
    status_map: ERPStatusMap
    upsert_keys: list[ERPUpsertKey] = Field(default_factory=list)
    sync_actions: list[str] = Field(default_factory=list)
