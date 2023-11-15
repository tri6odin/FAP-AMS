from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from config import PASSWD_MAX_LENGTH, PASSWD_MIN_LENGTH, CODE_TOTAL_DIGITS


class requestTokenSchema(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    code: str = Field(
        ..., min_length=CODE_TOTAL_DIGITS, max_length=CODE_TOTAL_DIGITS)
    password: Optional[str] = Field(
        None, min_length=PASSWD_MIN_LENGTH, max_length=PASSWD_MAX_LENGTH)


class responseTokenSchema(BaseModel):
    JWT: str
    RT: str
