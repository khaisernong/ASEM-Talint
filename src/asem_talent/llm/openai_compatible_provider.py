import json
from time import perf_counter

import httpx

from asem_talent.domain.models import (
    CandidateDecisionRequest,
    DecisionExplanation,
    DeterministicDecisionContext,
    ProviderUsage,
)
from asem_talent.llm.prompts import build_candidate_decision_messages
from asem_talent.llm.provider import DecisionProviderError


class OpenAICompatibleProvider:
    def __init__(
        self,
        *,
        provider_name: str,
        api_key_env_name: str,
        model_env_name: str,
        is_optional: bool,
        api_key: str,
        base_url: str,
        model_name: str,
        timeout_seconds: float,
        max_tokens: int,
        temperature: float,
        notes_max_chars: int,
        extra_system_instructions: str | None = None,
        retry_attempts: int = 2,
        client: httpx.Client | None = None,
    ) -> None:
        self.provider_name = provider_name
        self.api_key_env_name = api_key_env_name
        self.model_env_name = model_env_name
        self.is_optional = is_optional
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.notes_max_chars = notes_max_chars
        self.extra_system_instructions = extra_system_instructions
        self.retry_attempts = retry_attempts
        self.client = client or httpx.Client(timeout=self.timeout_seconds)

    def explain_candidate_track_fit(
        self,
        request: CandidateDecisionRequest,
        context: DeterministicDecisionContext,
    ) -> tuple[DecisionExplanation, ProviderUsage]:
        if self.api_key == "UNSPECIFIED":
            provider_label = "optional non-judge-path provider" if self.is_optional else "runtime provider"
            raise DecisionProviderError(
                f"{self.api_key_env_name} is UNSPECIFIED. Configure the environment before calling the {provider_label}."
            )
        if self.model_name == "UNSPECIFIED":
            raise DecisionProviderError(
                f"{self.model_env_name} is UNSPECIFIED. Configure a valid {self.provider_name} model before calling the provider."
            )
        if self.base_url == "UNSPECIFIED":
            raise DecisionProviderError(
                f"{self.provider_name} base URL is UNSPECIFIED. Configure the provider endpoint before calling it."
            )

        messages = build_candidate_decision_messages(request, context, self.notes_max_chars)
        if self.extra_system_instructions:
            messages[0]["content"] = f"{messages[0]['content']}\n{self.extra_system_instructions}"

        payload = {
            "model": self.model_name,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        last_error: Exception | None = None
        for attempt in range(self.retry_attempts + 1):
            started_at = perf_counter()
            try:
                response = self.client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
                latency_ms = int((perf_counter() - started_at) * 1000)
                return self._parse_explanation_response(response.json(), latency_ms)
            except (httpx.HTTPError, ValueError, KeyError, DecisionProviderError) as error:
                last_error = error
                if attempt >= self.retry_attempts:
                    break

        raise DecisionProviderError(f"{self.provider_name} provider call failed after retries: {last_error}")

    def _parse_explanation_response(
        self,
        payload: dict,
        latency_ms: int,
    ) -> tuple[DecisionExplanation, ProviderUsage]:
        usage_payload = payload.get("usage", {})
        try:
            choice = payload["choices"][0]
            message_content = self._extract_message_content(choice.get("message", {}).get("content"))
            if message_content is None:
                raise DecisionProviderError(
                    f"{self.provider_name} returned no assistant content "
                    f"(finish_reason={choice.get('finish_reason', 'UNSPECIFIED')}, "
                    f"completion_tokens={usage_payload.get('completion_tokens', 'UNSPECIFIED')}). "
                    "Increase the token limit or adjust the model configuration so it emits visible JSON output."
                )
            parsed_content = json.loads(self._clean_json_text(message_content))
            explanation = DecisionExplanation.model_validate(parsed_content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as error:
            raise DecisionProviderError(f"Invalid {self.provider_name} response payload: {error}") from error

        usage = ProviderUsage(
            request_id=payload.get("id"),
            model=payload.get("model", self.model_name),
            prompt_tokens=usage_payload.get("prompt_tokens"),
            completion_tokens=usage_payload.get("completion_tokens"),
            total_tokens=usage_payload.get("total_tokens"),
            latency_ms=latency_ms,
        )
        return explanation, usage

    def _extract_message_content(self, content: object) -> str | None:
        if content is None:
            return None
        if isinstance(content, str):
            return content
        if isinstance(content, dict):
            text = content.get("text")
            return text if isinstance(text, str) else json.dumps(content)
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, str):
                    text_parts.append(item)
                    continue
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
            joined = "".join(text_parts).strip()
            return joined or None
        return str(content)

    def _clean_json_text(self, content: str) -> str:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
        return cleaned