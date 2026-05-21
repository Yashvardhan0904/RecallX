"""
SQLAlchemy ORM models for AgentMemory SRS
Based on database schema defined in section 7.2 of the SRS
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import (
    Column, String, Integer, DateTime, ARRAY, Text, ForeignKey,
    TIMESTAMP, JSONB, Boolean, func
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

Base = declarative_base()


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


class APIKey(Base):
    """
    API Key entity - represents authentication credentials for a tenant
    FR-9.1: API Key Model with SHA-256 hashing (FR-SEC-02)
    """
    __tablename__ = "api_keys"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    key_hash = Column(String(64), nullable=False, unique=True)  # SHA-256 hash
    scopes = Column(ARRAY(String), default=list)  # ['read', 'write', 'admin']
    rate_limit_per_min = Column(Integer, default=60)
    token_budget = Column(Integer, default=2000)
    embedding_provider = Column(String(50), default='openai')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="api_keys")

    def __repr__(self):
        return f"<APIKey(id={self.id}, tenant_id={self.tenant_id})>"


class Session(Base):
    """
    Session entity - represents a bounded period of agent activity
    FR-ING-06: Support session start and end hook endpoints
    """
    __tablename__ = "sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    cwd = Column(String(512))  # Current working directory
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
    type = Column(String(50), nullable=False)  # prompt | tool_use | output | file
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
    content = Column(Text, nullable=False)  # narrative
    facts = Column(ARRAY(String), default=list)
    concepts = Column(ARRAY(String), default=list)
    files = Column(ARRAY(String), default=list)
    strength = Column(Integer, default=5)  # 1-10; decays over time
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    decay_at = Column(TIMESTAMP(timezone=True))  # When decay should occur
    deleted_at = Column(TIMESTAMP(timezone=True))  # Soft delete timestamp

    # Relationships
    tenant = relationship("Tenant", back_populates="memories")

    def __repr__(self):
        return f"<Memory(id={self.id}, title={self.title})>"


class AuditLog(Base):
    """
    Audit Log entity - comprehensive activity logging
    FR-GOV-01: Log every memory mutation to audit_log
    NFR-OBS-01: Emit structured JSON logs with traceId
    """
    __tablename__ = "audit_log"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)  # save | recall | delete | export | snapshot
    target_id = Column(PG_UUID(as_uuid=True))  # ID of the affected resource
    details = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action})>"
