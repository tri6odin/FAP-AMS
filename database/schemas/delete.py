from typing import Optional
from pydantic import BaseModel, Field

from config import PASSWD_MAX_LENGTH, PASSWD_MIN_LENGTH


class requestDeleteSchema(BaseModel):
    password: Optional[str] = Field(
        None, min_length=PASSWD_MIN_LENGTH, max_length=PASSWD_MAX_LENGTH)


class responseDeleteSchema(BaseModel):
    detail: str
