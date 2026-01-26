from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from Presentation.common import (
    setup_middleware,
    validation_exception_handler,
    not_found_exception_handler,
    business_rule_exception_handler,
    validation_exception_handler_app,
    database_exception_handler,
    llm_service_exception_handler,
)
from Application.Exceptions import NotFoundException, BusinessRuleException, ValidationException, LlmServiceError
from sqlalchemy.exc import SQLAlchemyError
from Infrastructure.Database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="AI Interviewer API",
    description="AI-powered interview system API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

setup_middleware(app)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BusinessRuleException, business_rule_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler_app)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(LlmServiceError, llm_service_exception_handler)


from Presentation.Routers import register_routers
import uvicorn

register_routers(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
