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

## Architecture Review

### Is this Scalable?
**Yes, but with limits.** The current **Collection-per-Tenant** strategy (separate collection for each org) is excellent for Data Isolation and Security but hits a ceiling.
*   **Scalability**: Good for **100s to ~10,000 tenants**. Beyond this, MongoDB namespace limits and overhead effectively slow down the cluster.
*   **Performance**: Extremely fast for single-tenant queries as data is physically separated.

### Trade-offs & Analysis
| Strategy | Pros | Cons |
| :--- | :--- | :--- |
| **Current (Collection/Tenant)** | ✅ Zero data leaks (hard isolation)<br>✅ Easy per-tenant backup/restore | ⚠️ **Schema Migrations**: Must iterate 1000s of collections to update fields.<br>⚠️ **Resource Overhead**: High memory usage per collection at scale. |

### Recommendation for Massive Scale
If building for **100k+ organizations** (SaaS scale), a **Pooled/Shared Collection** design is "better":
1.  **Shared Collection**: All data lives in one collection with an indexed `org_id` field.
2.  **Why?**: Infinite scalability, instant schema changes, efficient indexing.
3.  **Risk**: Requires strict code-level filtering to prevent data cross-contamination.

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
