from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from asem_talent.domain.models import ResumeParseResponse
from asem_talent.services.resume_parser import ResumeParseError, parse_resume_document

router = APIRouter(prefix="/v1/resumes", tags=["resumes"])


@router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume(file: Annotated[UploadFile, File(...)]) -> ResumeParseResponse:
    try:
        content = await file.read()
        return parse_resume_document(file.filename or "resume", file.content_type, content)
    except ResumeParseError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error