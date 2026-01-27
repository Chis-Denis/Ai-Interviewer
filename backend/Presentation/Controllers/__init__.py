from presentation.controllers.interview_controller import router as interview_router
from presentation.controllers.question_controller import router as question_router
from presentation.controllers.answer_controller import router as answer_router
from presentation.controllers.summary_controller import router as summary_router

__all__ = [
    "interview_router",
    "question_router",
    "answer_router",
    "summary_router",
]