"""
Memory model
"""
from uuid import uuid4
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, ARRAY, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base import Base


class Memory(Base):
    """
    Memory entity - LLM-compressed, indexed unit derived from observations
    FR-COMP-01: Compress observations via LLM into facts, concepts, narrative
    FR-RET-01: Support hybrid recall combining BM25, vector, and graph results
    """
    __tablename__ = "memories"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    session_ids = Column(ARRAY(PG_UUID(as_uuid=True)), default=list, nullable=False)
    title = Column(String(512))
    content = Column(Text, nullable=False)
    facts = Column(ARRAY(String), default=list)
    concepts = Column(ARRAY(String), default=list)
    files = Column(ARRAY(String), default=list)
    strength = Column(Integer, default=5)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    decay_at = Column(TIMESTAMP(timezone=True))
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    tenant = relationship("Tenant", back_populates="memories")

    def __repr__(self):
        return f"<Memory(id={self.id}, title={self.title})>"
