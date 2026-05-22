"""
AuditLog model
"""
from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from app.db.base import Base


class AuditLog(Base):
    """
    Audit Log entity - comprehensive activity logging
    FR-GOV-01: Log every memory mutation to audit_log
    NFR-OBS-01: Emit structured JSON logs with traceId
    """
    __tablename__ = "audit_log"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)
    target_id = Column(PG_UUID(as_uuid=True))
    details = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action})>"
