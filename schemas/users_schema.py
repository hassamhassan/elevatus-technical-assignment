from pydantic import BaseModel, EmailStr, SecretStr


class UserRegisterRequestSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr


class UserRegisterResponseSchema(BaseModel):
    message: str


class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: SecretStr
