from fastapi import APIRouter
from app.models.organization import AdminLogin, TokenResponse
from app.services.org_service import OrganizationService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login", response_model=TokenResponse)
async def admin_login(credentials: AdminLogin):
    return await OrganizationService.admin_login(
        credentials.email,
        credentials.password
    )
