from Presentation.Controllers.interview_controller import router as interview_router
from Presentation.Controllers.question_controller import router as question_router
from Presentation.Controllers.answer_controller import router as answer_router
from Presentation.Controllers.summary_controller import router as summary_router

__all__ = [
    "interview_router",
    "question_router",
    "answer_router",
    "summary_router",
]