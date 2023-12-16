import uuid
from typing import Dict

from database.db import database
from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.users_schema import (
    UserLoginRequestSchema,
    UserRegisterRequestSchema,
    UserRegisterResponseSchema,
)
from utils.constants import (
    EMAIL_ALREADY_EXIST,
    USER_REGISTERED_SUCCESSFULLY,
    SUCCESS,
    INCORRECT_EMAIL_PASSWORD,
    NOT_FOUND
)
from views.users import (
    create_access_token,
    authenticate_user,
    hash_password
)

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": NOT_FOUND}},
)


@user_router.post("/register", response_model=UserRegisterResponseSchema)
async def register_user(user: UserRegisterRequestSchema) -> Dict[str, str]:
    """
    Register new User.

    Args:
        user: UserRegisterRequestSchema - The user data to be registered.

    Returns:
        Dict[str, str]: A dictionary with a message indicating the registration status.
    """
    user_collection: AsyncIOMotorCollection = await database.get_collection("users")
    existing_user: Dict = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_ALREADY_EXIST
        )

    user_data: Dict = user.model_dump()

    user_data["uuid"] = str(uuid.uuid4())
    user_data["password"] = hash_password(user.password.get_secret_value())
    await user_collection.insert_one(user_data)

    return {"message": USER_REGISTERED_SUCCESSFULLY}


@user_router.post("/login")
async def login_user(user: UserLoginRequestSchema) -> Dict[str, str]:
    """
    Authenticate user login.

    Args:
        user: UserLoginRequestSchema - The user login credentials.

    Returns:
        Dict[str, str]: A dictionary with a message and access token upon successful login.
    """
    user_collection: AsyncIOMotorCollection = await database.get_collection("users")
    user_data: Dict = await user_collection.find_one({"email": user.email})

    authenticate: bool = await authenticate_user(
        email=user.email,
        password=user.password.get_secret_value(),
        user_collection=user_collection
    )

    if not user_data or not authenticate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=INCORRECT_EMAIL_PASSWORD
        )
    access_token: str = await create_access_token(
        data={
            "id": str(user_data["uuid"]),
            "email": user_data["email"],
        }
    )

    return {"message": SUCCESS, "access_token": access_token}
