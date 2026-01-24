from fastapi import FastAPI
from Presentation.Controllers.health_controller import router as health_router
from Presentation.Controllers.interview_controller import router as interview_router
from Presentation.Controllers.question_controller import router as question_router
from Presentation.Controllers.answer_controller import router as answer_router
from Presentation.Controllers.summary_controller import router as summary_router


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(interview_router, prefix="/api/v1")
    app.include_router(question_router, prefix="/api/v1")
    app.include_router(answer_router, prefix="/api/v1")
    app.include_router(summary_router, prefix="/api/v1")
