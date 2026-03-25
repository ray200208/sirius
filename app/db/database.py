from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
import logging

# Create async engine optimized for PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,                    # Set to True only for debugging
    pool_pre_ping=True,            # Good for PostgreSQL to detect dead connections
    pool_size=10,                  # Adjust based on your needs
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    """FastAPI dependency for async database sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()