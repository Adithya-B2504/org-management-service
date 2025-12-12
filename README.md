# Organization Management Service

A multi-tenant organization management API built with FastAPI and MongoDB (Motor).

## Structure

- `app/`: Application source code
  - `main.py`: FastAPI entry point
  - `models/`: Pydantic models
  - `routes/`: API endpoints
  - `services/`: Business logic
  - `database.py`: Database connection
- `.env`: Environment variables
- `requirements.txt`: Project dependencies

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Visit API Docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
