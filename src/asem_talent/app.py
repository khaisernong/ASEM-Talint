from fastapi import FastAPI

from asem_talent.api.dashboard import router as dashboard_router
from asem_talent.api.erp import router as erp_router
from asem_talent.api.market import router as market_router
from asem_talent.api.resumes import router as resume_router
from asem_talent.api.routes import router as decision_router
from asem_talent.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)

    @application.get("/health", tags=["health"])
    def healthcheck() -> dict[str, object]:
        missing_review_config = settings.missing_ilmu_config()

        review_provider_ready = len(missing_review_config) == 0
        review_provider_message = (
            "Z.AI / ILMU review ready."
            if review_provider_ready
            else f"Configure {', '.join(missing_review_config)} to enable the Z.AI / ILMU review."
        )

        return {
            "status": "ok",
            "environment": settings.app_env,
            "live_provider_ready": review_provider_ready,
            "live_provider_message": review_provider_message,
            "zai_provider_ready": review_provider_ready,
            "zai_provider_message": review_provider_message,
            "ilmu_provider_ready": review_provider_ready,
            "ilmu_provider_message": review_provider_message,
            "review_provider_ready": review_provider_ready,
            "review_provider_message": review_provider_message,
        }

    application.include_router(dashboard_router)
    application.include_router(decision_router)
    application.include_router(resume_router)
    application.include_router(market_router)
    application.include_router(erp_router)
    return application


app = create_app()
