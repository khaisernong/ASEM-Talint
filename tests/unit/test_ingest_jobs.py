import csv
import json

from asem_talent.data.ingest_jobs import (
    main,
    normalize_employer_rows,
    normalize_formal_wage_dashboard_html,
    normalize_hotspot_rows,
    normalize_wage_rows,
    resolve_wages_source,
    run_ingestion_jobs,
)


def test_normalize_wage_rows_accepts_alias_columns() -> None:
    rows = normalize_wage_rows(
        [
            {
                "quarter": "2025-Q4",
                "state_name": "Selangor",
                "district_name": "Sepang",
                "economic_activity": "manufacturing",
                "median_formal_wage": "4200",
            }
        ],
        source_label="test-source",
    )

    assert rows[0]["date"] == "2025-Q4"
    assert rows[0]["state"] == "Selangor"
    assert rows[0]["value"] == "4200"


def test_normalize_employer_rows_accepts_alias_columns() -> None:
    rows = normalize_employer_rows(
        [
            {
                "job_id": "role_001",
                "company_name": "ASEM Partner",
                "site_name": "Cyberjaya Lab",
                "district_name": "Sepang",
                "state_name": "Selangor",
                "job_title": "Validation Engineer Trainee",
                "talent_track": "track_validation",
                "skills": "debugging|data_acquisition",
                "preferred_fields": "mechatronics|electrical",
                "vacancies": "5",
                "salary_min": "5000",
                "salary_max": "6500",
            }
        ],
        source_label="test-source",
    )

    assert rows[0]["role_id"] == "role_001"
    assert rows[0]["employer_name"] == "ASEM Partner"
    assert rows[0]["track_id"] == "track_validation"


def test_normalize_formal_wage_dashboard_html_extracts_state_salaries() -> None:
    html_text = """
    <html><head></head><body>
    <script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{"meta":{"id":"dashboard-formal-sector-wages"},"timeseries_callout":{"data_as_of":"2025-Q3","data":{"sgr":{"salary":3127},"mys":{"salary":2864}}}}}}</script>
    </body></html>
    """

    rows = normalize_formal_wage_dashboard_html(html_text, source_label="dashboard-test")

    assert rows[0]["date"] == "2025-Q3"
    assert rows[0]["state"] == "Selangor"
    assert rows[0]["sector"] == "formal_sector"
    assert rows[0]["value"] == "3127"


def test_run_ingestion_jobs_writes_normalized_outputs(tmp_path) -> None:
    wages_source = tmp_path / "wages.csv"
    wages_source.write_text(
        "quarter,state_name,district_name,economic_activity,median_formal_wage\n2025-Q4,Selangor,Sepang,manufacturing,4200\n",
        encoding="utf-8",
    )
    employer_source = tmp_path / "employer.csv"
    employer_source.write_text(
        "job_id,company_name,site_name,district_name,state_name,job_title,talent_track,skills,preferred_fields,vacancies,salary_min,salary_max\nrole_001,ASEM Partner,Cyberjaya Lab,Sepang,Selangor,Validation Engineer Trainee,track_validation,debugging|data_acquisition,mechatronics|electrical,5,5000,6500\n",
        encoding="utf-8",
    )
    hotspot_source = tmp_path / "hotspots.json"
    hotspot_source.write_text(
        json.dumps([
            {
                "id": "hs_001",
                "name": "IC Park 2 and ASEM",
                "type": "training_validation_robotics",
                "district_name": "Sepang",
                "state_name": "Selangor",
                "lat": 2.9210,
                "lng": 101.6540,
            }
        ]),
        encoding="utf-8",
    )

    outputs = run_ingestion_jobs(str(wages_source), str(employer_source), str(hotspot_source), tmp_path / "official")

    assert outputs["wages"].exists()
    assert outputs["employer"].exists()
    assert outputs["hotspots"].exists()

    with outputs["wages"].open("r", encoding="utf-8", newline="") as handle:
        wage_rows = list(csv.DictReader(handle))
    assert wage_rows[0]["state"] == "Selangor"


def test_run_ingestion_jobs_accepts_dashboard_html_for_wages(tmp_path) -> None:
    wages_source = tmp_path / "formal_wages.html"
    wages_source.write_text(
        "<script id=\"__NEXT_DATA__\" type=\"application/json\">{\"props\":{\"pageProps\":{\"meta\":{\"id\":\"dashboard-formal-sector-wages\"},\"timeseries_callout\":{\"data_as_of\":\"2025-Q3\",\"data\":{\"sgr\":{\"salary\":3127}}}}}}</script>",
        encoding="utf-8",
    )
    employer_source = tmp_path / "employer.csv"
    employer_source.write_text(
        "job_id,company_name,site_name,district_name,state_name,job_title,talent_track,skills,preferred_fields,vacancies,salary_min,salary_max\nrole_001,ASEM Partner,Cyberjaya Lab,Sepang,Selangor,Validation Engineer Trainee,track_validation,debugging|data_acquisition,mechatronics|electrical,5,5000,6500\n",
        encoding="utf-8",
    )
    hotspot_source = tmp_path / "hotspots.json"
    hotspot_source.write_text(
        json.dumps(
            [
                {
                    "id": "hs_001",
                    "name": "IC Park 2 and ASEM",
                    "type": "training_validation_robotics",
                    "district_name": "Sepang",
                    "state_name": "Selangor",
                }
            ]
        ),
        encoding="utf-8",
    )

    outputs = run_ingestion_jobs(str(wages_source), str(employer_source), str(hotspot_source), tmp_path / "official")

    with outputs["wages"].open("r", encoding="utf-8", newline="") as handle:
        wage_rows = list(csv.DictReader(handle))
    assert wage_rows[0]["sector"] == "formal_sector"


def test_resolve_wages_source_uses_manifest_when_default_is_selected(tmp_path) -> None:
    manifest_path = tmp_path / "opendosm.registry.json"
    manifest_path.write_text(
        json.dumps(
            {
                "formal_wages_dashboard": {
                    "page_url": "https://open.dosm.gov.my/dashboard/formal-sector-wages"
                }
            }
        ),
        encoding="utf-8",
    )

    resolved = resolve_wages_source(
        "https://open.dosm.gov.my/dashboard/formal-sector-wages",
        str(manifest_path),
    )

    assert resolved == "https://open.dosm.gov.my/dashboard/formal-sector-wages"


def test_cli_main_uses_explicit_sources(tmp_path) -> None:
    wages_source = tmp_path / "wages.csv"
    wages_source.write_text(
        "date,state,district,sector,metric,value,currency\n2025-Q4,Selangor,Sepang,manufacturing,median_formal_wage,4200,MYR\n",
        encoding="utf-8",
    )
    employer_source = tmp_path / "employer.csv"
    employer_source.write_text(
        "role_id,employer_name,facility_name,district,state,role_title,track_id,required_skills,preferred_degree_fields,openings,salary_band_min,salary_band_max\nrole_001,ASEM Partner,Cyberjaya Lab,Sepang,Selangor,Validation Engineer Trainee,track_validation,debugging|data_acquisition,mechatronics|electrical,5,5000,6500\n",
        encoding="utf-8",
    )
    hotspot_source = tmp_path / "hotspots.json"
    hotspot_source.write_text(
        json.dumps([
            {
                "hotspot_id": "hs_001",
                "hotspot_name": "IC Park 2 and ASEM",
                "hotspot_type": "training_validation_robotics",
                "district": "Sepang",
                "state": "Selangor",
            }
        ]),
        encoding="utf-8",
    )
    output_dir = tmp_path / "official"

    exit_code = main([
        "--wages-source",
        str(wages_source),
        "--employer-source",
        str(employer_source),
        "--hotspot-source",
        str(hotspot_source),
        "--output-dir",
        str(output_dir),
    ])

    assert exit_code == 0
    assert (output_dir / "wages_formal_mfg.csv").exists()