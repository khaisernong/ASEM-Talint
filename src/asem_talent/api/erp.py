from fastapi import APIRouter, HTTPException

from asem_talent.domain.models import ERPSyncPackage, ERPSyncRequest
from asem_talent.services.erp_sync import build_erp_sync_package

router = APIRouter(prefix="/v1/erp", tags=["erp"])


@router.post("/sync-package", response_model=ERPSyncPackage)
def create_erp_sync_package(request: ERPSyncRequest) -> ERPSyncPackage:
    try:
        return build_erp_sync_package(request)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=f"Unknown selected_role_id: {error.args[0]}") from error