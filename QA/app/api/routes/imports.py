"""Import API: DOCX upload + pasted text, both funneled through the same parser/
validator/import-service pipeline (spec section 5.2, 6, 7)."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, import_service
from app.core.config import get_settings
from app.core.exceptions import FileTooLargeError, UnsupportedFileTypeError, ValidationFailedError
from app.db.models.enums import DuplicateStrategy, QuestionFormat, QuestionType
from app.importers.docx_extractor import DocxTextExtractor, PlainTextExtractor
from app.importers.dto import ImportOptions, ImportResult
from app.importers.text_parser import QuestionTextParser
from app.importers.validator import ImportValidationService
from app.schemas.import_job import (
    ImportJobResponse,
    ImportPreviewItem,
    ImportResultResponse,
    ImportSummary,
    TextImportRequest,
)
from app.services.import_service import QuestionImportService

router = APIRouter(tags=["imports"])

_extractor_docx = DocxTextExtractor()
_extractor_text = PlainTextExtractor()
_parser = QuestionTextParser()
_validator = ImportValidationService()


def _service(db: Session = Depends(get_db)) -> QuestionImportService:
    return import_service(db)


def _to_response(result: ImportResult) -> ImportResultResponse:
    return ImportResultResponse(
        dry_run=result.dry_run,
        job_id=result.job_id,
        summary=ImportSummary(**result.summary.__dict__),
        items=[
            ImportPreviewItem(
                source_order=i.source_order,
                category=i.category,
                question_type=i.question_type,
                question=i.question,
                answer=i.answer,
                status=i.status,
                warnings=i.warnings,
                errors=i.errors,
                question_id=i.question_id,
            )
            for i in result.items
        ],
        unparsed_segments=result.unparsed_segments,
    )


@router.post("/api/admin/import/docx", response_model=ImportResultResponse)
async def import_docx(
    file: UploadFile = File(...),
    dry_run: bool = Form(False),
    duplicate_strategy: DuplicateStrategy = Form(DuplicateStrategy.SKIP),
    generate_concepts: bool = Form(False),
    default_category: str | None = Form(None),
    default_question_type: QuestionType = Form(QuestionType.TEXT),
    default_language_scope: str | None = Form(None),
    question_format: QuestionFormat = Form(QuestionFormat.MULTIPLE_CHOICE),
    service: QuestionImportService = Depends(_service),
) -> ImportResultResponse:
    settings = get_settings()

    if not file.filename or not file.filename.lower().endswith(".docx"):
        raise UnsupportedFileTypeError("Chỉ chấp nhận file .docx")

    content_bytes = await file.read()
    if len(content_bytes) > settings.max_docx_upload_size_bytes:
        raise FileTooLargeError(f"File vượt quá giới hạn {settings.max_docx_upload_size_mb}MB")

    text = _extractor_docx.extract(content_bytes)
    document = _parser.parse(text)
    validated = _validator.validate(document)

    options = ImportOptions(
        dry_run=dry_run,
        duplicate_strategy=duplicate_strategy.value,
        generate_concepts=generate_concepts,
        default_category=default_category,
        default_question_type=default_question_type.value,
        default_language_scope=default_language_scope,
        default_question_format=question_format.value,
        source_type="DOCX",
        source_name=file.filename,
    )
    result = service.import_document(validated, options)
    return _to_response(result)


@router.post("/api/admin/import/text", response_model=ImportResultResponse)
def import_text(
    request: TextImportRequest, service: QuestionImportService = Depends(_service)
) -> ImportResultResponse:
    settings = get_settings()

    if not request.content.strip():
        raise ValidationFailedError("Nội dung dán vào không được để trống")
    if len(request.content.encode("utf-8")) > settings.max_text_import_size_bytes:
        raise ValidationFailedError(
            f"Nội dung vượt quá giới hạn {settings.max_text_import_size_kb}KB"
        )

    text = _extractor_text.extract(request.content)
    document = _parser.parse(text)
    validated = _validator.validate(document)

    options = ImportOptions(
        dry_run=request.dry_run,
        duplicate_strategy=request.duplicate_strategy.value,
        generate_concepts=request.generate_concepts,
        default_category=request.default_category,
        default_question_type=request.default_question_type.value,
        default_language_scope=request.default_language_scope,
        default_question_format=request.question_format.value,
        source_type="PASTED_TEXT",
        source_name=None,
    )
    result = service.import_document(validated, options)
    return _to_response(result)


@router.get("/api/admin/import/jobs", response_model=list[ImportJobResponse])
def list_import_jobs(
    page: int = 1, page_size: int = 20, service: QuestionImportService = Depends(_service)
) -> list[ImportJobResponse]:
    jobs, _ = service.list_jobs(page, page_size)
    return [_job_to_response(j) for j in jobs]


@router.get("/api/admin/import/jobs/{job_id}", response_model=ImportJobResponse)
def get_import_job(
    job_id: int, service: QuestionImportService = Depends(_service)
) -> ImportJobResponse:
    job = service.get_job(job_id)
    if job is None:
        raise ValidationFailedError(f"Import job {job_id} not found")
    return _job_to_response(job)


def _job_to_response(job) -> ImportJobResponse:
    summary = ImportSummary(**json.loads(job.summary_json)) if job.summary_json else None
    return ImportJobResponse(
        id=job.id,
        source_type=job.source_type,
        source_name=job.source_name,
        status=job.status,
        dry_run=job.dry_run,
        duplicate_strategy=job.duplicate_strategy,
        summary=summary,
        created_at=job.created_at,
        completed_at=job.completed_at,
    )
