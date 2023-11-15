from pydantic import BaseModel, EmailStr
from typing import Optional


class requestCodeSchema(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class responseCodeSchema(BaseModel):
    cooldown: int
