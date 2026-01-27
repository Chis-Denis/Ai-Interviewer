from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from application.exceptions import (
    NotFoundException,
    BusinessRuleException,
    ValidationException,
    LlmServiceError,
)
from .error_schemas import ValidationErrorDetail, ValidationErrorResponse
from core.config import settings


def format_validation_error(errors: List[Dict[str, Any]]) -> ValidationErrorResponse:
    formatted_errors = []
    for error in errors:
        field = ".".join(str(loc) for loc in error.get("loc", []))
        message = error.get("msg", "Validation error")
        error_type = error.get("type", "validation_error")
        
        formatted_errors.append(
            ValidationErrorDetail(
                field=field,
                message=message,
                type=error_type
            )
        )
    
    return ValidationErrorResponse(
        error="Validation Error",
        details=formatted_errors
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error_response = format_validation_error(exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Not Found", "message": exc.message}
    )


async def business_rule_exception_handler(request: Request, exc: BusinessRuleException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Business Rule Violation", "message": exc.message}
    )


async def validation_exception_handler_app(request: Request, exc: ValidationException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation Error", "message": exc.message}
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": "An error occurred while processing your request. Please try again later."
        }
    )


async def llm_service_exception_handler(request: Request, exc: LlmServiceError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "LLM Service Error",
            "message": "An error occurred while generating content. Please try again later."
        }
    )
