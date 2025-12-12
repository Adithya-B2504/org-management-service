# Organization Management Service

Multi-tenant organization management API with MongoDB and JWT authentication.

## Tech Stack

- FastAPI, MongoDB (Motor), JWT, Python 3.10+

## Installation

```bash
# Clone and setup
git clone https://github.com/Adithya-B2504/org-management-service.git
cd org-management-service
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure .env
MONGO_URI=mongodb://localhost:27017
MASTER_DB_NAME=master_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Run
uvicorn app.main:app --reload --port 8000
```

Access: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/org/create` | Create organization | No |
| GET | `/org/get` | Get organization | No |
| PUT | `/org/update` | Update organization | No |
| DELETE | `/org/delete` | Delete organization | JWT |
| POST | `/admin/login` | Get JWT token | No |

## Architecture

**Collection-per-Tenant Model:**
- Master DB stores org metadata and admin credentials
- Each org gets its own MongoDB collection (`org_name`)
- Good isolation, scales to 1000+ organizations

**Trade-offs:**
- ✅ Simple, secure, easy backups
- ⚠️ Limited to ~10k orgs per database

**Alternatives considered:**
- Database-per-tenant: Better isolation but complex
- Shared collection: Simpler but security risks

## Testing

```bash
# Create org
curl -X POST http://localhost:8000/org/create -H "Content-Type: application/json" \
  -d "{\"organization_name\":\"TestCorp\",\"email\":\"admin@test.com\",\"password\":\"pass123\"}"

# Login
curl -X POST http://localhost:8000/admin/login -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@test.com\",\"password\":\"pass123\"}"

# Delete (use token from login)
curl -X DELETE "http://localhost:8000/org/delete?organization_name=TestCorp" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Project Structure

```text
app/
├── main.py           # FastAPI app
├── config.py         # Settings
├── database.py       # MongoDB + dynamic collections
├── models/           # Pydantic models
├── services/         # Business logic + auth
└── routes/           # API endpoints
```

## Author

B Adithya - badithya637@gmail.com
