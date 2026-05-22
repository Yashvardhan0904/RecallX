"""
Session model
"""
from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, ARRAY, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base import Base


class Session(Base):
    """
    Session entity - represents a bounded period of agent activity
    FR-ING-06: Support session start and end hook endpoints
    """
    __tablename__ = "sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    cwd = Column(String(512))
    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(TIMESTAMP(timezone=True))
    summary = Column(Text)
    top_concepts = Column(ARRAY(String), default=list)
    key_files = Column(ARRAY(String), default=list)

    # Relationships
    tenant = relationship("Tenant", back_populates="sessions")
    observations = relationship("Observation", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id={self.id}, tenant_id={self.tenant_id})>"
