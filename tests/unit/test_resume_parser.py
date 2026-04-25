from io import BytesIO

import pytest
from docx import Document

from asem_talent.services.resume_parser import MAX_UPLOAD_BYTES, ResumeParseError, parse_resume_document


def _build_docx_bytes(lines: list[str]) -> bytes:
    document = Document()
    for line in lines:
        document.add_paragraph(line)
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_parse_resume_document_extracts_structured_context_from_docx() -> None:
    content = _build_docx_bytes(
        [
            "alex applicant",
            "alex@example.com",
            "+60 12-345 6789",
            "Projects",
            "Vision-guided wafer inspection prototype - Python automation for defect debugging",
            "Internship",
            "Automation Intern at Penang E&E SME",
            "Certifications",
            "IPC-A-610 awareness",
        ]
    )

    result = parse_resume_document("resume.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", content)

    assert result.file_type == "docx"
    assert "[REDACTED_EMAIL]" in result.redacted_preview
    assert "[REDACTED_PHONE]" in result.redacted_preview
    assert "python_basics" in result.resume_context.skill_tags
    assert result.resume_context.project_highlights[0].title.startswith("Vision-guided")
    assert result.resume_context.internship_highlights[0].organization == "Penang E&E SME"


def test_parse_resume_document_rejects_oversized_upload() -> None:
    with pytest.raises(ResumeParseError) as error:
        parse_resume_document("resume.pdf", "application/pdf", b"x" * (MAX_UPLOAD_BYTES + 1))

    assert error.value.status_code == 413


def test_parse_resume_document_supports_pdf_path_via_extractor(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "asem_talent.services.resume_parser._extract_pdf_text",
        lambda content: "Projects\nWafer validation project\nInternship\nValidation Intern at ASEM Lab\npython debugging",
    )

    result = parse_resume_document("resume.pdf", "application/pdf", b"%PDF-1.4")

    assert result.file_type == "pdf"
    assert "validation engineer trainee" in result.resume_context.inferred_role_signals


def test_parse_resume_document_uses_ocr_for_image_only_pdf(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "asem_talent.services.resume_parser._extract_pdf_text",
        lambda content: "",
    )
    monkeypatch.setattr(
        "asem_talent.services.resume_parser._extract_pdf_text_with_ocr",
        lambda content: "Projects\nPython automation and debugging project\nInternship\nAutomation Intern at Penang E&E SME",
    )

    result = parse_resume_document("resume.pdf", "application/pdf", b"%PDF-1.4")

    assert "python_basics" in result.resume_context.skill_tags
    assert any("OCR fallback" in warning for warning in result.warnings)