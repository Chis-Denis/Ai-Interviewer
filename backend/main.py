from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Core.config import settings
from Infrastructure.Db import init_db

app = FastAPI(
    title="AI Interviewer API",
    description="AI-powered interview system API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized successfully")


# Router registration
from Presentation.Controllers.health_controller import router as health_router
from Presentation.Controllers.interview_controller import router as interview_router

app.include_router(health_router)
app.include_router(interview_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
