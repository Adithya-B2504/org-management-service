import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from pymongo.uri_parser import parse_uri

# Force reload settings to be sure
# (Actually Config is loaded at import time, so we rely on what's in settings)

print(f"DEBUG: MONGO_URI from settings is: '{settings.MONGO_URI}'")

try:
    print("Attempting to parse URI with pymongo...")
    parsed = parse_uri(settings.MONGO_URI)
    print("Parsed successfully:", parsed)
except Exception as e:
    print(f"Pymongo parsing failed: {e}")

async def test_connect():
    print("Attempting to connect with Motor...")
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        # Force a connection check
        await client.admin.command('ping')
        print("SUCCESS: Connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connect())
