# AgentMemory - Multi-Tenant Memory API

A persistent, structured memory service for AI agents with multi-tenant support.

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL
```bash
docker-compose up -d
```

### 3. Initialize Database
```bash
# Create a simple init script or use app/db
python -c "import asyncio; from app.db import init_db; asyncio.run(init_db())"
```

### 4. Run API Server
```bash
python main.py
```

Server: `http://localhost:8000`

---

## Check Health
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/status
```

---

## Database
- **Type:** PostgreSQL 15
- **Host:** localhost:5432
- **User:** agentmemory
- **Password:** agentmemory_dev_password (dev only)
- **Database:** agentmemory

Connect:
```bash
docker exec -it agentmemory_db psql -U agentmemory -d agentmemory
```

---

## Stop Services
```bash
docker-compose down
```

---

## Documentation
- [Quick Start Guide](./QUICKSTART.md)
- [Cleanup Summary](./CLEANUP_SUMMARY.md)

