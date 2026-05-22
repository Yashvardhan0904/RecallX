"""
Tenant model
"""
from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base import Base


class Tenant(Base):
    """
    Tenant entity - represents an isolated organizational unit
    FR-9.2: Multi-tenant isolation at storage layer
    """
    __tablename__ = "tenants"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    api_keys = relationship("APIKey", back_populates="tenant", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="tenant", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="tenant", cascade="all, delete-orphan")
    memories = relationship("Memory", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.name})>"
