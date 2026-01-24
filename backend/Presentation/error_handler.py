from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List, Dict, Any
from Application.Exceptions import (
    NotFoundException,
    BusinessRuleException,
)
from Presentation.Validations.error_schemas import ValidationErrorDetail, ValidationErrorResponse


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
