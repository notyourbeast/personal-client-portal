"""
Quick script to test MongoDB connection.
Run this to verify your MongoDB setup before starting the server.
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.settings import get_settings


async def test_connection():
    settings = get_settings()
    print(f"Testing connection to: {settings.mongo_uri.replace(settings.mongo_uri.split('@')[0].split('://')[1].split(':')[0], '***') if '@' in settings.mongo_uri else settings.mongo_uri}")
    print(f"Database: {settings.mongo_db}")
    
    try:
        client = AsyncIOMotorClient(settings.mongo_uri)
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        db = client[settings.mongo_db]
        collections = await db.list_collection_names()
        print(f"📁 Collections in database: {collections if collections else 'None (database is empty)'}")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your MONGO_URI in .env file")
        print("2. For MongoDB Atlas: Make sure your IP is whitelisted")
        print("3. For local MongoDB: Make sure MongoDB is running")
        print("4. Verify your username and password are correct")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)

