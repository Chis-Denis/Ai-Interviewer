from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from Core.config import settings

BACKEND_DIR = Path(__file__).parent.parent.parent.resolve()
DEFAULT_DB_PATH = BACKEND_DIR / "Infrastructure" / "Database" / "ai_interviewer.db"

def get_async_database_url() -> str:
    db_url = settings.DATABASE_URL
    if not db_url or db_url.strip() == "":
        db_url = f"sqlite:///{DEFAULT_DB_PATH}"
    elif "Infrastructure/Db" in db_url or "Infrastructure\\Db" in db_url:
        db_url = f"sqlite:///{DEFAULT_DB_PATH}"
    elif db_url.startswith("sqlite:///./"):
        relative_path = db_url.replace("sqlite:///./", "")
        absolute_path = BACKEND_DIR / relative_path
        db_url = f"sqlite:///{absolute_path}"
    elif db_url.startswith("sqlite:///"):
        path_part = db_url.replace("sqlite:///", "")
        if not Path(path_part).is_absolute():
            absolute_path = BACKEND_DIR / path_part
            db_url = f"sqlite:///{absolute_path}"
    
    if db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    return db_url

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
    db_url = get_async_database_url()
    if db_url.startswith("sqlite+aiosqlite:///"):
        db_path_str = db_url.replace("sqlite+aiosqlite:///", "")
        db_path = Path(db_path_str)
    else:
        db_path = DEFAULT_DB_PATH
    
    db_dir = db_path.parent
    if db_dir and not db_dir.exists():
        db_dir.mkdir(parents=True, exist_ok=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
