from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

from config import NICKNAME_MAX_LENGTH, NICKNAME_MIN_LENGTH, STR_MAX_LENGTH
from typing_extensions import Annotated


class requestProfileSchema(BaseModel):
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=STR_MAX_LENGTH)
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=STR_MAX_LENGTH)
    nickname: Optional[str] = Field(
        None, min_length=NICKNAME_MIN_LENGTH, max_length=NICKNAME_MAX_LENGTH)
    age: Optional[Annotated[int, Field(ge=18)]] = None


class responseProfileSchema(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=STR_MAX_LENGTH)
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=STR_MAX_LENGTH)
    nickname: Optional[str] = Field(
        None, min_length=NICKNAME_MIN_LENGTH, max_length=NICKNAME_MAX_LENGTH)
    age: Optional[Annotated[int, Field(ge=18)]] = None
    password: Optional[str] = None

    @field_validator('password')
    def hash_password(cls, v):
        if v is None:
            return False
        return bool(v)
