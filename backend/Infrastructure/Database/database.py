from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

BACKEND_DIR = Path(__file__).parent.parent.parent.resolve()
DEFAULT_DB_PATH = BACKEND_DIR / "infrastructure" / "database" / "ai_interviewer.db"


def get_database_url() -> str:
    return f"sqlite+aiosqlite:///{DEFAULT_DB_PATH}"


engine = create_async_engine(get_database_url(), future=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    db_path = DEFAULT_DB_PATH
    db_dir = db_path.parent
    if not db_dir.exists():
        db_dir.mkdir(parents=True, exist_ok=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
