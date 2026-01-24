from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from Infrastructure.Db import init_db
from Presentation.middleware import setup_middleware
from Presentation.error_handler import (
    validation_exception_handler,
    not_found_exception_handler,
    business_rule_exception_handler,
)
from Application.Exceptions import NotFoundException, BusinessRuleException

app = FastAPI(
    title="AI Interviewer API",
    description="AI-powered interview system API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

setup_middleware(app)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BusinessRuleException, business_rule_exception_handler)


@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized successfully")


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
