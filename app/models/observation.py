"""
Observation model
"""
from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, ARRAY, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from app.db.base import Base


class Observation(Base):
    """
    Observation entity - raw events emitted by an agent
    FR-ING-01: Accept observations via POST /v1/observations
    FR-ING-04: Persist raw observations to observations table
    """
    __tablename__ = "observations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="SET NULL"))
    ts = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    type = Column(String(50), nullable=False)
    tool = Column(String(255))
    input = Column(JSONB)
    output = Column(JSONB)
    files = Column(ARRAY(String), default=list)
    tags = Column(ARRAY(String), default=list)

    # Relationships
    tenant = relationship("Tenant", back_populates="observations")
    session = relationship("Session", back_populates="observations")

    def __repr__(self):
        return f"<Observation(id={self.id}, type={self.type})>"
