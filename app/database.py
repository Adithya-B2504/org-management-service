from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(settings.MONGO_URI)
    
    @classmethod
    async def close_db(cls):
        cls.client.close()
    
    @classmethod
    def get_master_db(cls):
        return cls.client[settings.MASTER_DB_NAME]
    
    @classmethod
    def get_org_collection(cls, collection_name: str):
        """Dynamically access organization collection"""
        return cls.client[settings.MASTER_DB_NAME][collection_name]
    
    @classmethod
    async def create_org_collection(cls, org_name: str):
        """Create new collection for organization"""
        collection_name = f"org_{org_name.lower().replace(' ', '_')}"
        db = cls.get_master_db()
        
        # Check if collection exists
        collections = await db.list_collection_names()
        if collection_name not in collections:
            await db.create_collection(collection_name)
        
        return collection_name

db = Database()
