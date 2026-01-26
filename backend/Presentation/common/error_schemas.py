from pydantic import BaseModel
from typing import List


class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    type: str


class ValidationErrorResponse(BaseModel):
    error: str
    details: List[ValidationErrorDetail]
