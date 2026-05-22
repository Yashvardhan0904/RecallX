"""
Application Configuration
"""
from os import getenv

# Environment
ENVIRONMENT = getenv("ENVIRONMENT", "development")

# API
API_PORT = int(getenv("API_PORT", "8000"))
API_HOST = getenv("API_HOST", "0.0.0.0")

# Database
DATABASE_URL = getenv(
    "DATABASE_URL",
    "postgresql+psycopg://agentmemory:agentmemory_dev_password@localhost:5432/agentmemory"
)
SQLALCHEMY_ECHO = getenv("SQLALCHEMY_ECHO", "False").lower() == "true"

# Logging
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
