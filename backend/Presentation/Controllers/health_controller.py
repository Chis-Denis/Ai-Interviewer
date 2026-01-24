from fastapi import APIRouter, status

router = APIRouter(tags=["system"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def root():
    return {
        "message": "AI Interviewer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@router.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    return {"status": "healthy"}
