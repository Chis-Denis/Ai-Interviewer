from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from Presentation.middleware import setup_middleware
from Presentation.error_handler import (
    validation_exception_handler,
    not_found_exception_handler,
    business_rule_exception_handler,
    database_exception_handler,
    llm_service_exception_handler,
)
from Application.Exceptions import NotFoundException, BusinessRuleException, LlmServiceError
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    from Infrastructure.Db.database import init_db
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
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(LlmServiceError, llm_service_exception_handler)


from Presentation.Routers import register_routers

register_routers(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
