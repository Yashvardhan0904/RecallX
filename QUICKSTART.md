# Quick Start Guide - AgentMemory Database Setup

## ✅ Setup Checklist

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
- FastAPI, Uvicorn, SQLAlchemy 2.0, psycopg3, and other packages

### Step 2: Start PostgreSQL
```bash
docker-compose up -d
```
- Starts PostgreSQL 15 container
- Credentials: agentmemory / agentmemory_dev_password
- Database: agentmemory on port 5432

Verify it's running:
```bash
docker-compose ps
```

### Step 3: Initialize Database Schema
```bash
python init_db.py init
```
- Creates all 6 tables from the SRS
- Sets up relationships and constraints
- Enables UUID and JSONB support

Expected output:
```
2026-05-20 10:30:45 - __main__ - INFO - Initializing database...
2026-05-20 10:30:46 - database - INFO - Creating database tables...
2026-05-20 10:30:46 - database - INFO - Database tables created successfully
✓ Database initialization complete
```

### Step 4: Start the API
```bash
python main.py
```

Expected output:
```
2026-05-20 10:30:50 - __main__ - INFO - 🚀 Starting AgentMemory API...
2026-05-20 10:30:50 - database - INFO - ✓ Database initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Verify Everything Works
Test endpoints in another terminal:

```bash
# Health check
curl http://localhost:8000/health

# API status (tests database connection)
curl http://localhost:8000/api/v1/status
```

---

## 📊 Database Tables Created

### 1. **tenants**
- Organizational units for multi-tenancy
- Fields: id, name, created_at

### 2. **api_keys**
- API authentication credentials
- Fields: id, tenant_id, key_hash, scopes, rate_limit_per_min, token_budget, embedding_provider, created_at

### 3. **sessions**
- Agent activity periods
- Fields: id, tenant_id, cwd, started_at, ended_at, summary, top_concepts, key_files

### 4. **observations**
- Raw events from agents
- Fields: id, tenant_id, session_id, ts, type, tool, input, output, files, tags

### 5. **memories**
- LLM-compressed memories
- Fields: id, tenant_id, session_ids, title, content, facts, concepts, files, strength, created_at, decay_at, deleted_at

### 6. **audit_log**
- Complete activity audit trail
- Fields: id, tenant_id, action, target_id, details, created_at

---

## 🔧 Common Commands

| Task | Command |
|------|---------|
| Install packages | `pip install -r requirements.txt` |
| Start database | `docker-compose up -d` |
| Stop database | `docker-compose down` |
| View logs | `docker-compose logs -f postgres` |
| Initialize DB | `python init_db.py init` |
| Reset DB | `python init_db.py reset` |
| Drop tables | `python init_db.py drop` |
| Start API | `python main.py` |
| Connect to DB | `docker exec -it agentmemory_db psql -U agentmemory -d agentmemory` |

---

## 🐛 Troubleshooting

### PostgreSQL won't start
```bash
# Check logs
docker-compose logs postgres

# Reset container
docker-compose down
docker-compose up -d
```

### Database already exists error
```bash
# Drop and recreate
python init_db.py reset
```

### Cannot connect to database
```bash
# Verify PostgreSQL is running
docker-compose ps

# Check if port 5432 is available
netstat -an | grep 5432
```

### SQLAlchemy import error
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📝 Configuration

Edit `.env` to customize:
- `DATABASE_URL` - PostgreSQL connection string
- `SQLALCHEMY_ECHO` - Enable SQL query logging
- `ENVIRONMENT` - development/production
- `API_PORT` - Server port (default: 8000)
- `API_HOST` - Server host (default: 0.0.0.0)

---

## 🎯 Next Steps

After setup is complete:
1. Implement API endpoints in `routers/` directory
2. Add service layer for LLM compression
3. Implement memory search (BM25, vector, graph)
4. Add memory lifecycle/consolidation logic
5. Implement governance endpoints
6. Add comprehensive logging & monitoring

---

## 📚 Resources

- **SRS Document:** Section 7 (Data Model), Section 11 (Build Plan)
- **PostgreSQL:** http://localhost:5432
- **API:** http://localhost:8000
- **Documentation:** See README.md

---

**Status:** ✅ Foundation Phase Complete
