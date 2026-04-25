from math import asin, cos, radians, sin, sqrt

from asem_talent.data.official_data import load_semicon_hotspots
from asem_talent.domain.models import AccessibilityDestination, AccessibilityRequest, AccessibilityResponse, CandidateProfile


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius_km = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return earth_radius_km * c


def score_destination_access(
    candidate: CandidateProfile,
    destination_district: str,
    destination_state: str,
    destination_latitude: float | None,
    destination_longitude: float | None,
) -> tuple[float, float | None, str]:
    if (
        candidate.latitude is not None
        and candidate.longitude is not None
        and destination_latitude is not None
        and destination_longitude is not None
    ):
        distance_km = _haversine_km(candidate.latitude, candidate.longitude, destination_latitude, destination_longitude)
        if distance_km <= 10:
            score = 1.0
        elif distance_km <= 25:
            score = 0.88
        elif distance_km <= 50:
            score = 0.72
        elif distance_km <= 100:
            score = 0.58
        else:
            score = 0.42

        if candidate.willing_to_relocate is False and candidate.state != destination_state:
            score = min(score, 0.35)
            note = f"Approximate straight-line distance is {distance_km:.1f} km and relocation is currently constrained."
        else:
            note = f"Approximate straight-line distance is {distance_km:.1f} km."
        return _clamp(score), round(distance_km, 1), note

    if candidate.state == destination_state and candidate.district == destination_district:
        return 1.0, None, "District-level match used because coordinates are not fully available."
    if candidate.state == destination_state:
        return 0.75, None, "State-level proximity used because coordinates are not fully available."
    if candidate.willing_to_relocate is True:
        return 0.6, None, "Cross-state destination accepted because the candidate is willing to relocate."
    if candidate.willing_to_relocate is False:
        return 0.3, None, "Cross-state destination is constrained because relocation is not preferred."
    return 0.45, None, "Cross-state destination estimated with limited travel data."


def build_accessibility_response(request: AccessibilityRequest) -> AccessibilityResponse:
    hotspots = load_semicon_hotspots()
    destinations = []

    for hotspot in hotspots:
        accessibility_score, distance_km, note = score_destination_access(
            request.candidate,
            hotspot.district,
            hotspot.state,
            hotspot.latitude,
            hotspot.longitude,
        )
        destinations.append(
            AccessibilityDestination(
                destination_id=hotspot.hotspot_id,
                destination_name=hotspot.hotspot_name,
                destination_type=hotspot.hotspot_type,
                district=hotspot.district,
                state=hotspot.state,
                latitude=hotspot.latitude,
                longitude=hotspot.longitude,
                accessibility_score=round(accessibility_score, 4),
                distance_km=distance_km,
                note=note,
            )
        )

    ranked_destinations = sorted(
        destinations,
        key=lambda item: (-item.accessibility_score, item.distance_km if item.distance_km is not None else 99999, item.destination_name),
    )

    return AccessibilityResponse(
        candidate_id=request.candidate.candidate_id,
        destinations=ranked_destinations[: request.limit],
        data_sources=sorted({hotspot.source for hotspot in hotspots}),
    )