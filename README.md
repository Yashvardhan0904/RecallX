# AgentMemory - Multi-Tenant Memory API

A centralized, multi-tenant memory service for AI agents with persistent, structured, and searchable memory across sessions. Built with FastAPI, PostgreSQL, SQLAlchemy, and psycopg3.

## Project Structure

```
agentmemo/
├── models.py              # SQLAlchemy ORM models (database schema)
├── database.py            # Database configuration and session management
├── main.py                # FastAPI application entry point
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # PostgreSQL container setup
├── .env                   # Environment configuration
└── README.md              # This file
```

## Prerequisites

- Python 3.12+
- Docker & Docker Compose (for PostgreSQL)
- pip (Python package manager)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL Database

```bash
docker-compose up -d
```

This will start a PostgreSQL 15 container with the following credentials:
- **User:** agentmemory
- **Password:** agentmemory_dev_password
- **Database:** agentmemory
- **Port:** 5432

Verify the database is running:
```bash
docker-compose ps
```

### 3. Initialize Database Schema

```bash
python init_db.py init
```

This creates all tables defined in the SRS:
- `tenants` - Organizational units
- `api_keys` - Authentication credentials
- `sessions` - Agent activity periods
- `observations` - Raw agent events
- `memories` - LLM-compressed structured units
- `audit_log` - Activity logging

### 4. Start the API Server

```bash
python main.py
```

The API will be available at: **http://localhost:8000**

### 5. Check API Health

```bash
curl http://localhost:8000/health
```

```bash
curl http://localhost:8000/api/v1/status
```

## Database Schema (from SRS v1.0)

### Tables Overview

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `tenants` | Organizational units | id, name, created_at |
| `api_keys` | API authentication | id, tenant_id, key_hash, scopes, rate_limit_per_min, token_budget |
| `sessions` | Agent activity periods | id, tenant_id, started_at, ended_at, summary, top_concepts |
| `observations` | Raw agent events | id, tenant_id, session_id, type, tool, input, output, files, tags |
| `memories` | Compressed memories | id, tenant_id, title, content, facts, concepts, strength, decay_at, deleted_at |
| `audit_log` | Activity audit trail | id, tenant_id, action, target_id, details, created_at |

### Key Features

**Multi-Tenancy (NFR-SEC-03):**
- Every query filtered by `tenant_id` at the database layer
- Architecturally impossible to access cross-tenant data

**Memory Lifecycle (Section 10):**
- `strength` field (1-10) tracks memory salience
- `decay_at` for consolidation tier transitions
- `deleted_at` for soft-delete support

**Audit & Governance (FR-GOV-01):**
- All mutations logged to `audit_log`
- Support for soft-delete and hard-delete
- Comprehensive activity tracking

## Configuration

Edit `.env` to customize:

```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/database
SQLALCHEMY_ECHO=True              # SQL query logging
ENVIRONMENT=development            # development | production
API_PORT=8000
API_HOST=0.0.0.0
```

## Database Commands

### Initialize Database
```bash
python init_db.py init
```

### Reset Database (WARNING: Deletes all data)
```bash
python init_db.py reset
```

### Drop All Tables (WARNING: Destructive)
```bash
python init_db.py drop
```

## Database Management

### Connect to PostgreSQL directly

```bash
# Using Docker
docker exec -it agentmemory_db psql -U agentmemory -d agentmemory

# Using psql (if installed locally)
psql -h localhost -U agentmemory -d agentmemory
```

### Stop PostgreSQL Container

```bash
docker-compose down
```

### View PostgreSQL Logs

```bash
docker-compose logs -f postgres
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| API Framework | FastAPI | 0.104.1 |
| ASGI Server | Uvicorn | 0.24.0 |
| ORM | SQLAlchemy | 2.0.23 |
| Database Driver | psycopg | 3.17.0 |
| Database | PostgreSQL | 15 |
| Validation | Pydantic | 2.5.0 |
| Containerization | Docker Compose | 3.8 |

## Performance Targets (from SRS)

- **Ingestion:** < 200ms p99 latency (FR-PERF-01)
- **Recall:** < 500ms p99 latency for ≤20 memories (FR-PERF-02)
- **Scalability:** ≥100 concurrent tenants (FR-SCAL-01)
- **Availability:** 99.5% uptime (FR-REL-01)

## Security Features

- **TLS 1.2+** for all external traffic
- **SHA-256** hashing for API keys (FR-SEC-02)
- **Tenant isolation** at DB layer (FR-SEC-03)
- **Privacy scrubbing** of secrets from observations
- **Audit logging** of all mutations

## Development

### Run in Debug Mode
```bash
ENVIRONMENT=development python main.py
```

### Enable SQL Query Logging
```bash
SQLALCHEMY_ECHO=True python main.py
```

### Interactive Python Session
```bash
python
>>> import asyncio
>>> from database import get_db_session
>>> from models import Tenant
>>> 
>>> async def test():
...     async with get_db_session() as session:
...         result = await session.execute(text("SELECT count(*) FROM tenants"))
...         print(result.scalar())
>>> 
>>> asyncio.run(test())
```

## API Endpoints (Coming Soon)

### Authentication
- `POST /auth/keys` - Create API key
- `GET /auth/keys` - List keys
- `DELETE /auth/keys/:id` - Revoke key

### Ingestion
- `POST /v1/observations` - Ingest observation
- `POST /v1/sessions/start` - Start session
- `POST /v1/sessions/end` - End session

### Memory & Retrieval
- `POST /v1/memory/recall` - Hybrid recall
- `POST /v1/memory/smart-search` - Smart search
- `GET /v1/memory/profile` - Get profile
- `GET /v1/memory/timeline` - Get timeline

### Governance
- `POST /v1/memory/delete` - Delete memory
- `GET /v1/memory/audit` - Query audit log
- `POST /v1/memory/export` - Export memories
- `POST /v1/memory/snapshot` - Create snapshot

## Troubleshooting

### Database Connection Issues

**Error: `FATAL: role "agentmemory" does not exist`**
```bash
# Restart the container
docker-compose restart postgres
docker-compose logs postgres
```

**Error: `could not translate host name "postgres" to address`**
```bash
# Ensure Docker network is up
docker network ls
docker-compose down
docker-compose up -d
```

### SQLAlchemy Issues

**Import Error: `ModuleNotFoundError: No module named 'sqlalchemy'`**
```bash
pip install -r requirements.txt
```

**Async Error: `RuntimeError: Event loop is closed`**
- Use the provided `get_db_session()` context manager
- Don't manually create/close event loops

## References

- [AgentMemory SRS v1.0](./agentmemory_srs.pdf) - Complete specification
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/20/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg 3 Documentation](https://www.psycopg.org/psycopg3/)

## License

Confidential - Internal Project Document (as per SRS)

## Next Steps

1. ✅ PostgreSQL setup with Docker Compose
2. ✅ SQLAlchemy models from SRS schema
3. ✅ Database initialization scripts
4. ⬜ Implement API endpoints (auth, ingestion, retrieval)
5. ⬜ Add service layer (LLM compression, indexing)
6. ⬜ Implement hybrid search (BM25, vector, graph)
7. ⬜ Add memory lifecycle/consolidation
8. ⬜ Add governance endpoints
9. ⬜ Add comprehensive logging & metrics

---

**Created:** May 20, 2026 | **Status:** Foundation Phase ✓
