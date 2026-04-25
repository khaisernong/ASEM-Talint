from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ASEM Talint API"
    app_env: str = Field(default="local", alias="APP_ENV")
    zai_api_key: str = Field(default="UNSPECIFIED", alias="ZAI_API_KEY")
    zai_base_url: str = Field(default="https://api.z.ai/api/paas/v4", alias="ZAI_BASE_URL")
    glm_model: str = Field(default="UNSPECIFIED", alias="GLM_MODEL")
    ilmu_api_key: str = Field(default="UNSPECIFIED", alias="ILMU_API_KEY")
    ilmu_base_url: str = Field(default="UNSPECIFIED", alias="ILMU_BASE_URL")
    ilmu_model: str = Field(default="UNSPECIFIED", alias="ILMU_MODEL")
    ilmu_max_tokens: int = Field(default=1800, alias="ILMU_MAX_TOKENS")
    ilmu_notes_max_chars: int = Field(default=120, alias="ILMU_NOTES_MAX_CHARS")
    zai_timeout_seconds: float = Field(default=30.0, alias="ZAI_TIMEOUT_SECONDS")
    zai_max_tokens: int = Field(default=1200, alias="ZAI_MAX_TOKENS")
    zai_temperature: float = Field(default=0.1, alias="ZAI_TEMPERATURE")
    prompt_notes_max_chars: int = Field(default=1500, alias="PROMPT_NOTES_MAX_CHARS")
    opendosm_wages_source: str = Field(default="UNSPECIFIED", alias="OPENDOSM_WAGES_SOURCE")
    employer_demand_source: str = Field(default="UNSPECIFIED", alias="EMPLOYER_DEMAND_SOURCE")
    hotspot_registry_source: str = Field(default="UNSPECIFIED", alias="HOTSPOT_REGISTRY_SOURCE")
    opendosm_source_manifest: str = Field(default="UNSPECIFIED", alias="OPENDOSM_SOURCE_MANIFEST")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    def missing_zai_config(self) -> list[str]:
        missing = []
        if self.zai_api_key == "UNSPECIFIED":
            missing.append("ZAI_API_KEY")
        if self.glm_model == "UNSPECIFIED":
            missing.append("GLM_MODEL")
        return missing

    def missing_ilmu_config(self) -> list[str]:
        missing = []
        if self.ilmu_api_key == "UNSPECIFIED":
            missing.append("ILMU_API_KEY")
        if self.ilmu_base_url == "UNSPECIFIED":
            missing.append("ILMU_BASE_URL")
        if self.ilmu_model == "UNSPECIFIED":
            missing.append("ILMU_MODEL")
        return missing


@lru_cache
def get_settings() -> Settings:
    return Settings()
