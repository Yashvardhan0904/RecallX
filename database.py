"""
Database configuration and session management
Uses SQLAlchemy 2.0 with asyncpg (psycopg3) for async support
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event, pool
from contextlib import asynccontextmanager
import logging
from os import getenv

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = getenv(
    "DATABASE_URL",
    "postgresql+psycopg://agentmemory:agentmemory_dev_password@localhost:5432/agentmemory"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=getenv("SQLALCHEMY_ECHO", "False").lower() == "true",
    future=True,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=20,  # Connection pool size
    max_overflow=10,  # Overflow connections
    connect_args={
        "timeout": 10,
        "server_settings": {"application_name": "agentmemory"},
    },
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncSession:
    """
    Dependency for FastAPI to inject database sessions
    Usage: async def endpoint(session: AsyncSession = Depends(get_session))
    """
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_session():
    """Context manager for manual session management"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database schema
    Creates all tables defined in models
    """
    from models import Base
    
    async with engine.begin() as conn:
        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")


async def drop_db():
    """
    Drop all tables (use with caution!)
    Useful for testing and development
    """
    from models import Base
    
    async with engine.begin() as conn:
        logger.warning("Dropping all database tables...")
        await conn.run_sync(Base.metadata.drop_all)
        logger.warning("All database tables dropped")


async def close_db():
    """Close database connection pool"""
    await engine.dispose()
    logger.info("Database connections closed")
