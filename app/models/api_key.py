"""
APIKey model
"""
from uuid import uuid4
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, ARRAY, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base import Base


class APIKey(Base):
    """
    API Key entity - represents authentication credentials for a tenant
    FR-9.1: API Key Model with SHA-256 hashing (FR-SEC-02)
    """
    __tablename__ = "api_keys"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    key_hash = Column(String(64), nullable=False, unique=True)
    scopes = Column(ARRAY(String), default=list)
    rate_limit_per_min = Column(Integer, default=60)
    token_budget = Column(Integer, default=2000)
    embedding_provider = Column(String(50), default='openai')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="api_keys")

    def __repr__(self):
        return f"<APIKey(id={self.id}, tenant_id={self.tenant_id})>"
