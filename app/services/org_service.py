from app.database import db
from app.services.auth import hash_password, verify_password
from app.models.organization import OrganizationCreate, OrganizationUpdate
from datetime import datetime
from fastapi import HTTPException

class OrganizationService:
    
    @staticmethod
    async def create_organization(org_data: OrganizationCreate):
        """Create new organization with admin"""
        try:
            master_db = db.get_master_db()
            orgs_collection = master_db["organizations"]
            
            # Check if organization exists
            existing = await orgs_collection.find_one({"organization_name": org_data.organization_name})
            if existing:
                raise HTTPException(status_code=400, detail="Organization already exists")
            
            # Create organization collection
            collection_name = await db.create_org_collection(org_data.organization_name)
            
            # Create organization record
            org_doc = {
                "organization_name": org_data.organization_name,
                "collection_name": collection_name,
                "admin_email": org_data.email,
                "admin_password": hash_password(org_data.password),
                "created_at": datetime.utcnow()
            }
            
            result = await orgs_collection.insert_one(org_doc)
            org_doc["_id"] = str(result.inserted_id)
            
            return {
                "organization_name": org_doc["organization_name"],
                "collection_name": org_doc["collection_name"],
                "admin_email": org_doc["admin_email"],
                "created_at": org_doc["created_at"]
            }
        except Exception as e:
            print(f"ERROR in create_organization: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    async def get_organization(org_name: str):
        """Get organization by name"""
        master_db = db.get_master_db()
        orgs_collection = master_db["organizations"]
        
        org = await orgs_collection.find_one({"organization_name": org_name})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        return {
            "organization_name": org["organization_name"],
            "collection_name": org["collection_name"],
            "admin_email": org["admin_email"],
            "created_at": org["created_at"]
        }
    
    @staticmethod
    async def update_organization(org_data: OrganizationUpdate):
        """Update organization - create new collection and migrate data"""
        master_db = db.get_master_db()
        orgs_collection = master_db["organizations"]
        
        # Get existing organization
        org = await orgs_collection.find_one({"admin_email": org_data.email})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        # Verify password
        if not verify_password(org_data.password, org["admin_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create new collection
        new_collection_name = await db.create_org_collection(org_data.organization_name)
        old_collection_name = org["collection_name"]
        
        # Migrate data
        old_collection = db.get_org_collection(old_collection_name)
        new_collection = db.get_org_collection(new_collection_name)
        
        documents = await old_collection.find().to_list(length=None)
        if documents:
            await new_collection.insert_many(documents)
        
        # Update organization record
        await orgs_collection.update_one(
            {"_id": org["_id"]},
            {"$set": {
                "organization_name": org_data.organization_name,
                "collection_name": new_collection_name
            }}
        )
        
        return {"message": "Organization updated successfully"}
    
    @staticmethod
    async def delete_organization(org_name: str, admin_email: str):
        """Delete organization and its collection"""
        master_db = db.get_master_db()
        orgs_collection = master_db["organizations"]
        
        # Find organization
        org = await orgs_collection.find_one({
            "organization_name": org_name,
            "admin_email": admin_email
        })
        
        if not org:
            raise HTTPException(status_code=403, detail="Unauthorized or organization not found")
        
        # Drop organization collection
        await master_db.drop_collection(org["collection_name"])
        
        # Delete organization record
        await orgs_collection.delete_one({"_id": org["_id"]})
        
        return {"message": "Organization deleted successfully"}
    
    @staticmethod
    async def admin_login(email: str, password: str):
        """Authenticate admin and return JWT"""
        master_db = db.get_master_db()
        orgs_collection = master_db["organizations"]
        
        org = await orgs_collection.find_one({"admin_email": email})
        if not org or not verify_password(password, org["admin_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        from app.services.auth import create_access_token
        
        token_data = {
            "admin_email": email,
            "organization_id": str(org["_id"]),
            "organization_name": org["organization_name"]
        }
        
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}
