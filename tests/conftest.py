import pytest
import asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from main import app
import os
from dotenv import load_dotenv

load_dotenv()

# Test database settings
TEST_MONGODB_URI = os.getenv("TEST_MONGODB_URI", "mongodb://localhost:27017")
TEST_DB_NAME = "test_organization_service"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_client():
    """Create test client"""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")  # Changed from session to function
async def test_db():
    """Setup test database for each test function"""
    client = AsyncIOMotorClient(TEST_MONGODB_URI)
    db = client[TEST_DB_NAME]
    
    # Clean up before each test
    await db.client.drop_database(TEST_DB_NAME)
    
    # Also clean master database
    master_db = client["organization_master"]
    await master_db.client.drop_database("organization_master")
    
    yield db
    
    # Clean up after test
    try:
        await db.client.drop_database(TEST_DB_NAME)
        await master_db.client.drop_database("organization_master")
        client.close()
    except Exception as e:
        print(f"Warning during cleanup: {e}")

@pytest.fixture
def sample_organization_data():
    """Sample organization data for testing"""
    return {
        "organization_name": "TestOrg",
        "email": "admin@testorg.com",
        "password": "TestPass123"
    }

@pytest.fixture
def sample_login_data():
    """Sample login data for testing"""
    return {
        "email": "admin@testorg.com",
        "password": "TestPass123"
    }

@pytest.fixture(autouse=True)
async def cleanup_test_data(test_db):
    """Auto-cleanup after each test"""
    yield
    # Cleanup happens in test_db fixture now