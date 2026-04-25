from io import BytesIO

import pytest
from docx import Document
from fastapi.testclient import TestClient

from asem_talent.app import create_app
from asem_talent.services.resume_parser import MAX_UPLOAD_BYTES


def _build_docx_bytes(lines: list[str]) -> bytes:
    document = Document()
    for line in lines:
        document.add_paragraph(line)
    buffer = BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_resume_parse_endpoint_returns_resume_context() -> None:
    client = TestClient(create_app())
    document_bytes = _build_docx_bytes(
        [
            "alex applicant",
            "alex@example.com",
            "+60 12-345 6789",
            "Projects",
            "Vision-guided wafer inspection prototype - Python automation for defect debugging",
            "Internship",
            "Automation Intern at Penang E&E SME",
        ]
    )

    response = client.post(
        "/v1/resumes/parse",
        files={
            "file": (
                "resume.docx",
                document_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["file_type"] == "docx"
    assert body["redaction_counts"]["emails"] == 1
    assert "python_basics" in body["resume_context"]["skill_tags"]


def test_resume_parse_endpoint_rejects_unsupported_file_type() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/resumes/parse",
        files={"file": ("resume.txt", b"plain text", "text/plain")},
    )

    assert response.status_code == 415


def test_resume_parse_endpoint_enforces_size_limit() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/resumes/parse",
        files={"file": ("resume.pdf", b"x" * (MAX_UPLOAD_BYTES + 1), "application/pdf")},
    )

    assert response.status_code == 413


def test_resume_parse_endpoint_supports_ocr_fallback_for_image_only_pdf(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "asem_talent.services.resume_parser._extract_pdf_text",
        lambda content: "",
    )
    monkeypatch.setattr(
        "asem_talent.services.resume_parser._extract_pdf_text_with_ocr",
        lambda content: "Projects\nPython automation and debugging project\nInternship\nAutomation Intern at Penang E&E SME",
    )

    client = TestClient(create_app())
    response = client.post(
        "/v1/resumes/parse",
        files={"file": ("resume.pdf", b"%PDF-1.4", "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert "python_basics" in body["resume_context"]["skill_tags"]
    assert any("OCR fallback" in warning for warning in body["warnings"])