from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from Core.config import settings

def get_async_database_url() -> str:
    if settings.DATABASE_URL.startswith("sqlite:///"):
        return settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
    return settings.DATABASE_URL

engine = create_async_engine(
    get_async_database_url(),
    echo=settings.DATABASE_ECHO,
    future=True,
)

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
    db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
    db_dir = db_path.parent
    if db_dir and not db_dir.exists():
        db_dir.mkdir(parents=True, exist_ok=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
