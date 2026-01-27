from fastapi import FastAPI
from presentation.controllers.interview_controller import router as interview_router
from presentation.controllers.question_controller import router as question_router
from presentation.controllers.answer_controller import router as answer_router
from presentation.controllers.summary_controller import router as summary_router


def register_routers(app: FastAPI) -> None:
    app.include_router(interview_router, prefix="/api/v1")
    app.include_router(question_router, prefix="/api/v1")
    app.include_router(answer_router, prefix="/api/v1")
    app.include_router(summary_router, prefix="/api/v1")
