import httpx
from asem_talent.llm.openai_compatible_provider import OpenAICompatibleProvider


class ZAIProvider(OpenAICompatibleProvider):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        timeout_seconds: float,
        max_tokens: int,
        temperature: float,
        notes_max_chars: int,
        retry_attempts: int = 2,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            provider_name="Z.AI",
            api_key_env_name="ZAI_API_KEY",
            model_env_name="GLM_MODEL",
            is_optional=False,
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            timeout_seconds=timeout_seconds,
            max_tokens=max_tokens,
            temperature=temperature,
            notes_max_chars=notes_max_chars,
            retry_attempts=retry_attempts,
            client=client,
        )
