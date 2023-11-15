from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from config import CODE_TOTAL_DIGITS, PASSWD_MAX_LENGTH, PASSWD_MIN_LENGTH


class requestCredSchema(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    code: str = Field(
        ..., min_length=CODE_TOTAL_DIGITS, max_length=CODE_TOTAL_DIGITS)
    password: Optional[str] = Field(
        None, min_length=PASSWD_MIN_LENGTH, max_length=PASSWD_MAX_LENGTH)
