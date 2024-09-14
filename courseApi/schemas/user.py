from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    email: EmailStr
    full_name: str | None = None

    @field_validator("full_name")
    def validate_full_name(cls, value):
        if len(value) < 30:
            return value
        raise HTTPException("too long fullName")


class UserInDB(User):
    password: str


class UserMe(BaseModel):
    id:int
    email: EmailStr
    full_name: str | None = None
    is_admin:bool



class UserChangePassword(BaseModel):
    password: str
    new_password: str
    new_password_retype: str