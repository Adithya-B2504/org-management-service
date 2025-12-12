from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.org_service import OrganizationService
from app.services.auth import verify_token

router = APIRouter(prefix="/org", tags=["Organization"])

@router.post("/create", response_model=OrganizationResponse)
async def create_organization(org: OrganizationCreate):
    return await OrganizationService.create_organization(org)

@router.get("/get")
async def get_organization(organization_name: str):
    return await OrganizationService.get_organization(organization_name)

@router.put("/update")
async def update_organization(org: OrganizationUpdate):
    return await OrganizationService.update_organization(org)

@router.delete("/delete")
async def delete_organization(
    organization_name: str,
    authorization: str = Header(...)
):
    # Verify JWT token
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return await OrganizationService.delete_organization(
        organization_name,
        payload.get("admin_email")
    )
