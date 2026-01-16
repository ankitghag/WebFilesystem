from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import setting

# Create a standard synchronous engine with psycopg2
print(setting.SQLALCHEMY_DATABASE_URI)
engine = create_async_engine(
    setting.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=False,
        connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,  # IMPORTANT
    }
)

# Create asynchronous session factory
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()