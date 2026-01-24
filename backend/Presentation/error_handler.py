from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import List, Dict, Any
from Application.Exceptions import (
    ApplicationException,
    NotFoundException,
    BusinessRuleException,
)


def format_validation_error(errors: List[Dict[str, Any]]) -> Dict[str, Any]:
    formatted_errors = []
    for error in errors:
        field = ".".join(str(loc) for loc in error.get("loc", []))
        message = error.get("msg", "Validation error")
        error_type = error.get("type", "validation_error")
        
        formatted_errors.append({
            "field": field,
            "message": message,
            "type": error_type
        })
    
    return {
        "error": "Validation Error",
        "details": formatted_errors
    }


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_validation_error(exc.errors())
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
