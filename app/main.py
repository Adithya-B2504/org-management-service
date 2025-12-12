from fastapi import FastAPI
from app.database import db
from app.routes import org, admin
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect_db()
    yield
    # Shutdown
    await db.close_db()

app = FastAPI(
    title="Organization Management Service",
    description="Multi-tenant organization management API",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(org.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "Organization Management Service API"}
