from pydantic import BaseModel


class responseKeySchema(BaseModel):
    version: int
    public_key: str
