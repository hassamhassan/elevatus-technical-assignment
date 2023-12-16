import uuid

import pytest
from app import app
from database.db import database
from httpx import AsyncClient
from views.users import create_access_token, hash_password


@pytest.fixture(scope="session")
def anyio_backend():
    """
    Fixture to define the preferred AnyIO backend for the tests.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    """
    Fixture to provide an asynchronous test client for FastAPI.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
async def drop_database():
    """
    Fixture to drop the test database before each test function.
    """
    database.drop_database()


@pytest.fixture()
async def jwt_token():
    """
    Generate JWT token for user to access candidate endpoints.
    """
    user_collection = await database.get_collection("users")
    user_uuid = str(uuid.uuid4())
    payload = {
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "uuid": user_uuid,
        "password": hash_password("12345678")
    }
    await user_collection.insert_one(payload)

    user_credentials = {
        "email": payload.get("email"),
        "id": user_uuid
    }

    token = await create_access_token(user_credentials)
    return token
