import argparse
import csv
import io
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "official"
DEFAULT_HOTSPOT_REGISTRY = PROJECT_ROOT / "data" / "source_registry" / "semicon_hotspots.registry.json"
DEFAULT_OPENDOSM_SOURCE_MANIFEST = PROJECT_ROOT / "data" / "source_registry" / "opendosm.registry.json"

FORMAL_WAGES_DASHBOARD_URL = "https://open.dosm.gov.my/dashboard/formal-sector-wages"

STATE_CODE_MAP = {
    "jhr": "Johor",
    "kdh": "Kedah",
    "ktn": "Kelantan",
    "kul": "Kuala Lumpur",
    "lbn": "Labuan",
    "mlk": "Melaka",
    "mys": "Malaysia",
    "nsn": "Negeri Sembilan",
    "phg": "Pahang",
    "pjy": "Putrajaya",
    "pls": "Perlis",
    "png": "Penang",
    "prk": "Perak",
    "sbh": "Sabah",
    "sgr": "Selangor",
    "swk": "Sarawak",
    "trg": "Terengganu",
}


class IngestionJobError(RuntimeError):
    pass


def _is_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme in {"http", "https"}


def _read_text(source: str) -> str:
    if _is_url(source):
        response = httpx.get(source, timeout=30.0)
        response.raise_for_status()
        return response.text
    return Path(source).read_text(encoding="utf-8")


def _read_csv_rows(source: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(_read_text(source))))


def _read_json_rows(source: str) -> list[dict]:
    payload = json.loads(_read_text(source))
    if not isinstance(payload, list):
        raise IngestionJobError(f"Expected a JSON list in hotspot registry source: {source}")
    return payload


def _pick(mapping: dict, keys: list[str], default: str = "") -> str:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return str(value)
    return default


def _extract_next_data_payload(html_text: str) -> dict:
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.DOTALL)
    if not match:
        raise IngestionJobError("Could not locate __NEXT_DATA__ payload in the OpenDOSM dashboard HTML.")
    return json.loads(match.group(1))


def normalize_wage_rows(rows: list[dict[str, str]], source_label: str) -> list[dict[str, str]]:
    normalized_rows = []
    for row in rows:
        value = _pick(row, ["value", "median_formal_wage", "median_wage"])
        if not value:
            continue
        normalized_rows.append(
            {
                "date": _pick(row, ["date", "quarter", "period", "year_quarter"], default="UNSPECIFIED"),
                "state": _pick(row, ["state", "state_name"], default="UNSPECIFIED"),
                "district": _pick(row, ["district", "district_name"], default=""),
                "sector": _pick(row, ["sector", "economic_activity"], default="manufacturing"),
                "metric": _pick(row, ["metric"], default="median_formal_wage"),
                "value": value,
                "currency": _pick(row, ["currency"], default="MYR"),
                "source": _pick(row, ["source"], default=source_label),
            }
        )
    if not normalized_rows:
        raise IngestionJobError("No wage rows were normalized from the provided source.")
    return normalized_rows


def normalize_formal_wage_dashboard_html(html_text: str, source_label: str) -> list[dict[str, str]]:
    payload = _extract_next_data_payload(html_text)
    page_props = payload.get("props", {}).get("pageProps", {})
    callout = page_props.get("timeseries_callout", {})
    quarter = callout.get("data_as_of", "UNSPECIFIED")
    data = callout.get("data", {})

    normalized_rows = []
    for state_code, values in data.items():
        state_name = STATE_CODE_MAP.get(state_code)
        salary = values.get("salary") if isinstance(values, dict) else None
        if state_name is None or salary in (None, ""):
            continue
        normalized_rows.append(
            {
                "date": quarter,
                "state": state_name,
                "district": "",
                "sector": "formal_sector",
                "metric": "median_formal_wage",
                "value": str(salary),
                "currency": "MYR",
                "source": source_label,
            }
        )

    if not normalized_rows:
        raise IngestionJobError("No wage rows were extracted from the OpenDOSM formal wages dashboard payload.")
    return normalized_rows


def load_normalized_wage_rows(source: str) -> list[dict[str, str]]:
    text = _read_text(source)
    if "__NEXT_DATA__" in text and "dashboard-formal-sector-wages" in text:
        return normalize_formal_wage_dashboard_html(text, source_label="OpenDOSM formal sector wages dashboard")
    return normalize_wage_rows(list(csv.DictReader(io.StringIO(text))), source_label="OpenDOSM wages ingestion job")


def resolve_wages_source(wages_source: str, source_manifest: str) -> str:
    if wages_source != FORMAL_WAGES_DASHBOARD_URL or source_manifest == "UNSPECIFIED":
        return wages_source

    try:
        payload = json.loads(_read_text(source_manifest))
    except (OSError, json.JSONDecodeError, httpx.HTTPError):
        return wages_source

    if not isinstance(payload, dict):
        return wages_source
    manifest_source = payload.get("formal_wages_dashboard", {}).get("page_url")
    return str(manifest_source) if manifest_source else wages_source


def normalize_employer_rows(rows: list[dict[str, str]], source_label: str) -> list[dict[str, str]]:
    normalized_rows = []
    for row in rows:
        role_id = _pick(row, ["role_id", "job_id", "id"])
        if not role_id:
            continue
        normalized_rows.append(
            {
                "employer_id": _pick(row, ["employer_id", "company_id"], default=f"emp_{role_id}"),
                "employer_name": _pick(row, ["employer_name", "company_name"], default="UNSPECIFIED"),
                "facility_name": _pick(row, ["facility_name", "site_name"], default="UNSPECIFIED"),
                "district": _pick(row, ["district", "district_name"], default="UNSPECIFIED"),
                "state": _pick(row, ["state", "state_name"], default="UNSPECIFIED"),
                "role_id": role_id,
                "role_title": _pick(row, ["role_title", "job_title"], default="UNSPECIFIED"),
                "track_id": _pick(row, ["track_id", "talent_track"], default="track_validation"),
                "required_skills": _pick(row, ["required_skills", "skills"], default=""),
                "preferred_degree_fields": _pick(row, ["preferred_degree_fields", "preferred_fields"], default=""),
                "openings": _pick(row, ["openings", "vacancies"], default="0"),
                "onsite_requirement": _pick(row, ["onsite_requirement", "onsite"], default="true"),
                "salary_band_min": _pick(row, ["salary_band_min", "salary_min"], default=""),
                "salary_band_max": _pick(row, ["salary_band_max", "salary_max"], default=""),
                "demand_score": _pick(row, ["demand_score", "market_score"], default="0.5"),
                "latitude": _pick(row, ["latitude", "lat"], default=""),
                "longitude": _pick(row, ["longitude", "lon", "lng"], default=""),
                "source": _pick(row, ["source"], default=source_label),
            }
        )
    if not normalized_rows:
        raise IngestionJobError("No employer-demand rows were normalized from the provided source.")
    return normalized_rows


def normalize_hotspot_rows(rows: list[dict], source_label: str) -> list[dict[str, str]]:
    normalized_rows = []
    for row in rows:
        hotspot_id = _pick(row, ["hotspot_id", "id"])
        if not hotspot_id:
            continue
        normalized_rows.append(
            {
                "hotspot_id": hotspot_id,
                "hotspot_name": _pick(row, ["hotspot_name", "name"], default="UNSPECIFIED"),
                "hotspot_type": _pick(row, ["hotspot_type", "type"], default="UNSPECIFIED"),
                "district": _pick(row, ["district", "district_name"], default="UNSPECIFIED"),
                "state": _pick(row, ["state", "state_name"], default="UNSPECIFIED"),
                "latitude": _pick(row, ["latitude", "lat"], default=""),
                "longitude": _pick(row, ["longitude", "lon", "lng"], default=""),
                "evidence_tag": _pick(row, ["evidence_tag"], default="official_sector_doc"),
                "source": _pick(row, ["source"], default=source_label),
            }
        )
    if not normalized_rows:
        raise IngestionJobError("No hotspot rows were normalized from the provided source.")
    return normalized_rows


def _write_csv(file_path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_ingestion_jobs(
    wages_source: str,
    employer_source: str,
    hotspot_source: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    wage_rows = load_normalized_wage_rows(wages_source)
    employer_rows = normalize_employer_rows(_read_csv_rows(employer_source), source_label="Employer demand ingestion job")
    hotspot_rows = normalize_hotspot_rows(_read_json_rows(hotspot_source), source_label="Hotspot registry ingestion job")

    wage_path = output_dir / "wages_formal_mfg.csv"
    employer_path = output_dir / "employer_demand_semicon.csv"
    hotspot_path = output_dir / "semicon_hotspots.csv"

    _write_csv(
        wage_path,
        ["date", "state", "district", "sector", "metric", "value", "currency", "source"],
        wage_rows,
    )
    _write_csv(
        employer_path,
        [
            "employer_id",
            "employer_name",
            "facility_name",
            "district",
            "state",
            "role_id",
            "role_title",
            "track_id",
            "required_skills",
            "preferred_degree_fields",
            "openings",
            "onsite_requirement",
            "salary_band_min",
            "salary_band_max",
            "demand_score",
            "latitude",
            "longitude",
            "source",
        ],
        employer_rows,
    )
    _write_csv(
        hotspot_path,
        ["hotspot_id", "hotspot_name", "hotspot_type", "district", "state", "latitude", "longitude", "evidence_tag", "source"],
        hotspot_rows,
    )
    return {"wages": wage_path, "employer": employer_path, "hotspots": hotspot_path}


def _default_source(env_name: str, fallback: str) -> str:
    value = os.getenv(env_name)
    return value if value and value != "UNSPECIFIED" else fallback


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize official exports into the app's market CSV outputs.")
    parser.add_argument("--wages-source", default=_default_source("OPENDOSM_WAGES_SOURCE", FORMAL_WAGES_DASHBOARD_URL))
    parser.add_argument("--employer-source", default=_default_source("EMPLOYER_DEMAND_SOURCE", "UNSPECIFIED"))
    parser.add_argument("--hotspot-source", default=_default_source("HOTSPOT_REGISTRY_SOURCE", str(DEFAULT_HOTSPOT_REGISTRY)))
    parser.add_argument("--source-manifest", default=_default_source("OPENDOSM_SOURCE_MANIFEST", str(DEFAULT_OPENDOSM_SOURCE_MANIFEST)))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    if args.wages_source == "UNSPECIFIED" or args.employer_source == "UNSPECIFIED":
        raise IngestionJobError("Provide --wages-source and --employer-source, or set OPENDOSM_WAGES_SOURCE and EMPLOYER_DEMAND_SOURCE.")

    outputs = run_ingestion_jobs(
        wages_source=resolve_wages_source(args.wages_source, args.source_manifest),
        employer_source=args.employer_source,
        hotspot_source=args.hotspot_source,
        output_dir=Path(args.output_dir),
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())