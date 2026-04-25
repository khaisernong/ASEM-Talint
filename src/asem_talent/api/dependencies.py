from functools import lru_cache

from asem_talent.config import get_settings
from asem_talent.llm.ilmu_provider import ILMUProvider
from asem_talent.services.decision_engine import DecisionEngine


def _build_engine(provider) -> DecisionEngine:
    return DecisionEngine(provider=provider)


def _build_primary_review_engine() -> DecisionEngine:
    settings = get_settings()
    provider = ILMUProvider(
        api_key=settings.ilmu_api_key,
        base_url=settings.ilmu_base_url,
        model_name=settings.ilmu_model,
        timeout_seconds=settings.zai_timeout_seconds,
        max_tokens=settings.ilmu_max_tokens,
        temperature=settings.zai_temperature,
        notes_max_chars=settings.ilmu_notes_max_chars,
    )
    return _build_engine(provider)


@lru_cache
def get_decision_engine() -> DecisionEngine:
    return _build_primary_review_engine()


@lru_cache
def get_ilmu_decision_engine() -> DecisionEngine:
    return _build_primary_review_engine()
