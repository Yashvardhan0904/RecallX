<div align="center">
  <br />
  <img src="assets/logo.png" alt="RecallX Logo" width="120" height="120" style="margin-bottom: 20px;">
  
  <h1 style="margin: 10px 0; font-size: 2.5em; font-weight: 700;">RecallX</h1>
  <p style="margin: 5px 0 20px 0; font-size: 1.1em; color: #666;">Persistent Memory Service for AI Agents</p>
  
  <div style="margin: 20px 0;">
    <a href="https://www.python.org/" style="text-decoration: none; margin: 0 8px;">
      <img src="https://img.shields.io/badge/Python-3.12%2B-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </a>
    <a href="https://fastapi.tiangolo.com/" style="text-decoration: none; margin: 0 8px;">
      <img src="https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    </a>
    <a href="https://www.postgresql.org/" style="text-decoration: none; margin: 0 8px;">
      <img src="https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    </a>
  </div>
  
  <hr style="margin: 30px 0; border: none; border-top: 2px solid #e0e0e0;">
  
  <p style="font-size: 0.95em; margin: 15px 0;">
    <strong>⚡ High-Performance</strong> • <strong>🔐 Secure & Isolated</strong> • <strong>📊 Audited</strong>
  </p>
  
  <hr style="margin: 30px 0; border: none; border-top: 1px solid #e0e0e0;">
  
</div>

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