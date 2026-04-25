import csv
from functools import lru_cache
from pathlib import Path

from asem_talent.domain.models import EmployerRole, SemiconHotspot, WageSignal

DATA_ROOT = Path(__file__).resolve().parents[3] / "data" / "official"


def _split_pipe_list(raw_value: str) -> list[str]:
    return [item.strip() for item in raw_value.split("|") if item.strip()]


def _optional_float(raw_value: str) -> float | None:
    return float(raw_value) if raw_value else None


def _parse_bool(raw_value: str) -> bool:
    return raw_value.strip().lower() in {"1", "true", "yes"}


def _read_rows(file_name: str) -> list[dict[str, str]]:
    file_path = DATA_ROOT / file_name
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@lru_cache
def load_wage_signals() -> tuple[WageSignal, ...]:
    rows = _read_rows("wages_formal_mfg.csv")
    return tuple(
        WageSignal(
            date=row["date"],
            state=row["state"],
            district=row["district"] or None,
            sector=row["sector"],
            metric=row["metric"],
            value=float(row["value"]),
            currency=row["currency"],
            source=row["source"],
        )
        for row in rows
    )


@lru_cache
def load_employer_roles() -> tuple[EmployerRole, ...]:
    rows = _read_rows("employer_demand_semicon.csv")
    return tuple(
        EmployerRole(
            employer_id=row["employer_id"],
            employer_name=row["employer_name"],
            facility_name=row["facility_name"],
            district=row["district"],
            state=row["state"],
            role_id=row["role_id"],
            role_title=row["role_title"],
            track_id=row["track_id"],
            required_skills=_split_pipe_list(row["required_skills"]),
            preferred_degree_fields=_split_pipe_list(row["preferred_degree_fields"]),
            openings=int(row["openings"]),
            onsite_requirement=_parse_bool(row["onsite_requirement"]),
            salary_band_min=_optional_float(row["salary_band_min"]),
            salary_band_max=_optional_float(row["salary_band_max"]),
            demand_score=float(row["demand_score"]),
            latitude=_optional_float(row["latitude"]),
            longitude=_optional_float(row["longitude"]),
            source=row["source"],
        )
        for row in rows
    )


@lru_cache
def load_semicon_hotspots() -> tuple[SemiconHotspot, ...]:
    rows = _read_rows("semicon_hotspots.csv")
    return tuple(
        SemiconHotspot(
            hotspot_id=row["hotspot_id"],
            hotspot_name=row["hotspot_name"],
            hotspot_type=row["hotspot_type"],
            district=row["district"],
            state=row["state"],
            latitude=_optional_float(row["latitude"]),
            longitude=_optional_float(row["longitude"]),
            evidence_tag=row["evidence_tag"],
            source=row["source"],
        )
        for row in rows
    )