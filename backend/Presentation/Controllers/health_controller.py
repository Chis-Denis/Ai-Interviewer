from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/")
async def root():
    return {
        "message": "AI Interviewer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
