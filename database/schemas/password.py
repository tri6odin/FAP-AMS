from pydantic import BaseModel, Field
from typing import Optional
from config import PASSWD_MAX_LENGTH, PASSWD_MIN_LENGTH


class requestPasswordSchema(BaseModel):
    old_password: Optional[str] = Field(
        None, min_length=PASSWD_MIN_LENGTH, max_length=PASSWD_MAX_LENGTH)
    password: Optional[str] = Field(
        None, min_length=PASSWD_MIN_LENGTH, max_length=PASSWD_MAX_LENGTH)


class responsePasswordSchema(BaseModel):
    detail: str
