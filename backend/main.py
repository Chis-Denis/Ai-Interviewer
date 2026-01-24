from fastapi import FastAPI
from Infrastructure.Db import init_db
from Presentation.middleware import setup_middleware

app = FastAPI(
    title="AI Interviewer API",
    description="AI-powered interview system API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

setup_middleware(app)


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
