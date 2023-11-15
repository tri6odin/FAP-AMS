from sqlalchemy import Column, Integer, String
from database.base import Base


class PublicKeyModel(Base):
    __tablename__ = 'public_key'

    version = Column(Integer, primary_key=True, autoincrement=True, index=True)
    public_key = Column(String, nullable=False, index=True)
