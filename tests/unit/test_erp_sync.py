from asem_talent.domain.models import ERPSyncRequest, ResumeContext, ResumeProject
from asem_talent.services.erp_sync import ERP_SCHEMA_VERSION, build_erp_sync_package


def test_build_erp_sync_package_returns_erp_friendly_bundle(sample_request) -> None:
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

    package = build_erp_sync_package(
        ERPSyncRequest(
            candidate=candidate,
            target_track=sample_request.target_track,
            erp_system="SAP_S4HANA",
            external_candidate_id="ERP-CAND-42",
            external_case_id="ERP-CASE-99",
            current_wage=3200,
        )
    )

    assert package.schema_version == ERP_SCHEMA_VERSION
    assert package.erp_system == "SAP_S4HANA"
    assert package.candidate_master.external_candidate_id == "ERP-CAND-42"
    assert package.training_case.external_case_id == "ERP-CASE-99"
    assert "python_basics" in package.candidate_master.effective_skill_tags
    assert package.ranked_market_roles[0].role_id == "role_validation_001"
    assert package.ojt_shortlist[0].role_id == "role_validation_001"
    assert package.wage_mobility is not None
    assert package.wage_mobility.target_role_id == "role_validation_001"
    assert package.decision_summary.recommendation_stage in {"advance", "prepare_then_review", "reroute_before_review"}
    assert package.status_map.market_priority in {"high", "medium", "low"}
    assert any(key.entity == "wage_scenario" for key in package.upsert_keys)