import pytest
from fastapi import status


class TestUsers:

    @pytest.mark.anyio
    async def test_users(self, client):
        """
        Test case to check if the /ping endpoint returns HTTP 200 OK.
        """
        response = await client.get("/ping")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.anyio
    async def test_register_user(self, client):
        """
        Test case to register a new user and verify the success response.
        """
        payload = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "password": "12345678"
        }
        response = await client.post("/user/register", json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User Registered Successfully"

    @pytest.mark.anyio
    async def test_register_user_with_same_email(self, client):
        """
        Test case to register a user with an existing email and verify the error response.
        """
        payload = {
            "first_name": "string",
            "last_name": "string",
            "email": "user+1@example.com",
            "password": "12345678"
        }
        response = await client.post("/user/register", json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User Registered Successfully"

        response = await client.post("/user/register", json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Email already exists"

    @pytest.mark.anyio
    async def test_login_user(self, client):
        """
        Test case to login and verify the response.
        """
        payload = {
            "first_name": "string",
            "last_name": "string",
            "email": "test_user@example.com",
            "password": "12345678"
        }
        response = await client.post("/user/register", json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User Registered Successfully"

        payload = {
            "email": "test_user@example.com",
            "password": "12345678"
        }
        response = await client.post("/user/login", json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    @pytest.mark.anyio
    async def test_login_user_invalid_credentials(self, client):
        """
        Test case to login with invalid credentials and verify the error response.
        """
        payload = {
            "first_name": "string",
            "last_name": "string",
            "email": "valid_email@example.com",
            "password": "12345678"
        }
        response = await client.post("/user/register", json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "User Registered Successfully"

        payload = {
            "email": "invalid_email@example.com",
            "password": "12345678"
        }
        response = await client.post("/user/login", json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Incorrect email or password"
