<div align="center">
  <img src="assets/logo.png" alt="RecallX Logo" width="200" height="200">
  
  # RecallX
  **Persistent Memory Service for AI Agents**
  
  [![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
  [![PostgreSQL](https://img.shields.io/badge/postgresql-15-336791.svg)](https://www.postgresql.org/)
  
</div>

---

## What is RecallX?

RecallX is a centralized memory service that enables AI agents to store, retrieve, and search memories across sessions. It provides multi-tenant data isolation, audit logging, and high-performance memory recall with sub-second latency.

---

## Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose

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
python init_db.py init
```

### 4. Run the Server

```bash
python main.py
```

The API is available at **http://localhost:8000**

---

## Configuration

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://agentmemory:agentmemory_dev_password@localhost:5432/agentmemory
API_PORT=8000
API_HOST=0.0.0.0
ENVIRONMENT=development
SQLALCHEMY_ECHO=False
```

---

## Database Management

```bash
# Initialize
python init_db.py init

# Reset (deletes all data)
python init_db.py reset

# Connect to PostgreSQL
docker exec -it agentmemory_db psql -U agentmemory -d agentmemory

# Stop
docker-compose down
```

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0
- **Driver:** psycopg 3.17

---

## License

Confidential - Internal Project

---

<div align="center">
  Last Updated: May 21, 2026
</div>
