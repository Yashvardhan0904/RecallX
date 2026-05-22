"""
FastAPI application for AgentMemory
Main entry point for the REST API
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db import init_db, close_db, get_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting AgentMemory API...")
    await init_db()
    logger.info("✓ Database initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AgentMemory API...")
    await close_db()
    logger.info("✓ Cleanup complete")


# Create FastAPI app
app = FastAPI(
    title="AgentMemory API",
    description="Multi-tenant memory service for AI agents",
    version="1.0.0",
    lifespan=lifespan
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "agentmemory-api",
        "version": "1.0.0"
    }


# Example endpoint to test database connection
@app.get("/api/v1/status")
async def status(session: AsyncSession = Depends(get_session)):
    """
    API status endpoint - verifies database connection
    """
    try:
        # Test database connection
        from sqlalchemy import text
        result = await session.execute(text("SELECT 1"))
        result.scalar()
        
        return {
            "status": "operational",
            "database": "connected",
            "api_version": "v1"
        }
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }


# Include routers (to be added later)
# from routers import auth, observations, memory, governance


if __name__ == "__main__":
    import uvicorn
    from app.core.config import API_HOST, API_PORT, ENVIRONMENT
    
    logger.info(f"Starting server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=ENVIRONMENT == "development"
    )
