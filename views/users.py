from datetime import datetime, timedelta
from typing import Optional, Union, Dict

from configurations.config import settings
from database.db import database
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext


HASH_STRING = CryptContext(schemes=["bcrypt"])


def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password: str - The plain text password.
        hashed_password: str - The hashed password to be verified against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return HASH_STRING.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Hash the provided password.

    Args:
        password: str - The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return HASH_STRING.hash(password)


async def authenticate_user(email: str, password: str, user_collection: AsyncIOMotorCollection) -> bool:
    """
    Authenticate a user by verifying the provided email and password.

    Args:
        email: str - The user's email.
        password: str - The user's password.
        user_collection: Collection - The collection to search for the user.

    Returns:
        bool: True if authentication succeeds, False otherwise.
    """
    user: Dict = await user_collection.find_one({"email": email})
    if not user or not verify_password_hash(password, user.get("password")):
        return False
    return True


async def create_access_token(data: dict) -> str:
    """
    Create an access token based on the provided data.

    Args:
        data: dict - The data to encode into the token.

    Returns:
        str: The generated access token.
    """
    data["type"] = "access_token"
    data["exp"] = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE))
    data["iat"] = datetime.utcnow()
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def verify_user(
        authentication: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Optional[Dict[str, Union[str, int]]]:
    """
    Verify the user based on the provided authentication credentials.

    Args:
        authentication: HTTPAuthorizationCredentials - The user authentication credentials.

    Returns:
        Optional[Dict[str, Union[str, int]]]: Dictionary containing user details if verified, None otherwise.
    """
    authentication_error: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
    )
    try:
        payload: Dict = jwt.decode(
            authentication.credentials,
            settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM,
        )
    except jwt.JWTError as e:
        raise authentication_error

    user_collection: AsyncIOMotorCollection = await database.get_collection("users")
    user: Dict = await user_collection.find_one({"email": payload.get("email")})
    if not user:
        raise authentication_error
    return user
