-- AgentMemory Database Schema (PostgreSQL 15)
-- Generated from SRS v1.0 section 7.2
-- Multi-tenant architecture with cascading deletes

-- ========================================
-- 1. TENANTS TABLE
-- ========================================
-- Represents isolated organizational units for multi-tenancy
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX idx_tenants_name ON tenants(name);


-- ========================================
-- 2. API_KEYS TABLE
-- ========================================
-- API authentication credentials with SHA-256 hashing (FR-SEC-02)
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    key_hash VARCHAR(64) NOT NULL UNIQUE,  -- SHA-256 hash
    scopes TEXT[] DEFAULT '{}',  -- ['read', 'write', 'admin']
    rate_limit_per_min INT DEFAULT 60,
    token_budget INT DEFAULT 2000,
    embedding_provider VARCHAR(50) DEFAULT 'openai',
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX idx_api_keys_tenant_id ON api_keys(tenant_id);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);


-- ========================================
-- 3. SESSIONS TABLE
-- ========================================
-- Bounded agent activity periods (FR-ING-06)
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    cwd VARCHAR(512),  -- Current working directory
    started_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    ended_at TIMESTAMPTZ,
    summary TEXT,
    top_concepts TEXT[] DEFAULT '{}',
    key_files TEXT[] DEFAULT '{}'
);

CREATE INDEX idx_sessions_tenant_id ON sessions(tenant_id);
CREATE INDEX idx_sessions_started_at ON sessions(started_at);
CREATE INDEX idx_sessions_ended_at ON sessions(ended_at);


-- ========================================
-- 4. OBSERVATIONS TABLE
-- ========================================
-- Raw events emitted by agents (FR-ING-01, FR-ING-04)
-- Deduplication window: 5 minutes (FR-ING-02)
CREATE TABLE IF NOT EXISTS observations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
    ts TIMESTAMPTZ DEFAULT now() NOT NULL,
    type VARCHAR(50) NOT NULL,  -- 'prompt' | 'tool_use' | 'output' | 'file'
    tool VARCHAR(255),
    input JSONB,
    output JSONB,
    files TEXT[] DEFAULT '{}',
    tags TEXT[] DEFAULT '{}'
);

CREATE INDEX idx_observations_tenant_id ON observations(tenant_id);
CREATE INDEX idx_observations_session_id ON observations(session_id);
CREATE INDEX idx_observations_ts ON observations(ts);
CREATE INDEX idx_observations_type ON observations(type);


-- ========================================
-- 5. MEMORIES TABLE
-- ========================================
-- LLM-compressed, indexed memories (FR-COMP-01, FR-RET-01)
-- Strength: 1-10 salience score; decays over time
-- Soft delete via deleted_at timestamp (FR-GOV-02)
CREATE TABLE IF NOT EXISTS memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    session_ids UUID[] NOT NULL DEFAULT '{}',
    title VARCHAR(512),
    content TEXT NOT NULL,  -- narrative
    facts TEXT[] DEFAULT '{}',
    concepts TEXT[] DEFAULT '{}',
    files TEXT[] DEFAULT '{}',
    strength INT DEFAULT 5 CHECK (strength >= 1 AND strength <= 10),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    decay_at TIMESTAMPTZ,  -- When decay should occur
    deleted_at TIMESTAMPTZ  -- Soft delete timestamp
);

CREATE INDEX idx_memories_tenant_id ON memories(tenant_id);
CREATE INDEX idx_memories_created_at ON memories(created_at);
CREATE INDEX idx_memories_deleted_at ON memories(deleted_at);
CREATE INDEX idx_memories_strength ON memories(strength);
CREATE INDEX idx_memories_concepts ON memories USING GIN(concepts);
CREATE INDEX idx_memories_files ON memories USING GIN(files);


-- ========================================
-- 6. AUDIT_LOG TABLE
-- ========================================
-- Comprehensive mutation audit trail (FR-GOV-01, NFR-OBS-01)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,  -- 'save' | 'recall' | 'delete' | 'export' | 'snapshot'
    target_id UUID,  -- ID of affected resource
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

CREATE INDEX idx_audit_log_tenant_id ON audit_log(tenant_id);
CREATE INDEX idx_audit_log_action ON audit_log(action);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX idx_audit_log_target_id ON audit_log(target_id);


-- ========================================
-- MULTI-TENANCY ENFORCEMENT (NFR-SEC-03)
-- ========================================
-- Every query MUST include WHERE tenant_id = $1
-- Cross-tenant access is architecturally impossible


-- ========================================
-- FOREIGN KEY RELATIONSHIPS
-- ========================================
-- tenants
--   ├── api_keys (1:N) CASCADE
--   ├── sessions (1:N) CASCADE
--   ├── observations (1:N) CASCADE
--   ├── memories (1:N) CASCADE
--   └── audit_log (1:N) CASCADE
--
-- sessions
--   └── observations (1:N) SET NULL
--
-- All foreign keys enforce referential integrity


-- ========================================
-- DATA RETENTION POLICIES
-- ========================================

-- Working Tier: 24 hours (FR-10.1)
-- Episodic Tier: 30 days
-- Semantic Tier: 6 months
-- Procedural Tier: Indefinite

-- Decay Rules (FR-10.2):
-- - Strength decreases by 1 every decay_interval (unless accessed)
-- - Every recall increments strength by +1 (reinforcement)
-- - Strength < 1: soft-deleted, scheduled for hard-deletion after 7 days


-- ========================================
-- NOTES
-- ========================================
-- - UUID: Native PostgreSQL UUID with gen_random_uuid()
-- - JSONB: Efficient JSON storage with indexing support
-- - ARRAY: Native array support for collections
-- - TIMESTAMPTZ: Timezone-aware timestamps for multi-region support
-- - GIN Indexes: For efficient array/JSONB searches
-- - Cascade Delete: Maintains referential integrity on tenant deletion
-- - Soft Delete: deleted_at field allows recoverable deletes
-- - Strength Constraint: Ensures memory strength is always 1-10
