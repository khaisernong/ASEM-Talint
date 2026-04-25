import httpx

from asem_talent.llm.openai_compatible_provider import OpenAICompatibleProvider


ILMU_COMPACT_JSON_INSTRUCTIONS = (
    "Keep the JSON terse. Use at most 2 items in each list. "
    "Keep each list item under 12 words. Keep explanation_summary under 40 words. "
    "Keep wage_note and accessibility_note under 16 words. Do not wrap JSON in markdown fences. "
    "The fields top_factors, missing_inputs, tradeoffs, pathway_steps, and validation_notes must remain JSON arrays even when they contain one item."
)


class ILMUProvider(OpenAICompatibleProvider):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        timeout_seconds: float,
        max_tokens: int,
        temperature: float,
        notes_max_chars: int,
        retry_attempts: int = 3,
        retry_backoff_seconds: float = 1.0,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            provider_name="ILMU.ai",
            api_key_env_name="ILMU_API_KEY",
            model_env_name="ILMU_MODEL",
            is_optional=True,
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            timeout_seconds=timeout_seconds,
            max_tokens=max_tokens,
            temperature=temperature,
            notes_max_chars=notes_max_chars,
            extra_system_instructions=ILMU_COMPACT_JSON_INSTRUCTIONS,
            retry_attempts=retry_attempts,
            retry_backoff_seconds=retry_backoff_seconds,
            client=client,
        )