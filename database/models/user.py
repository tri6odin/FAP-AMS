
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy import Column, DateTime, Integer, String, Enum
from config import CODE_TOTAL_DIGITS, NICKNAME_MAX_LENGTH, STR_MAX_LENGTH
from database.base import Base


class UserModel(Base):
    # Table configuration
    __tablename__ = "users"

    # User attributes
    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()), index=True)
    nickname = Column(String(NICKNAME_MAX_LENGTH),
                      unique=True, nullable=True, index=True)
    email = Column(String(254), unique=True, nullable=True, index=True)
    phone = Column(String(STR_MAX_LENGTH), unique=True,
                   nullable=True, index=True)
    password = Column(String(60), nullable=True)
    first_name = Column(String(STR_MAX_LENGTH), nullable=True)
    last_name = Column(String(STR_MAX_LENGTH), nullable=True)
    age = Column(Integer, nullable=True)
    # Status and types
    status = Column(Enum('temp', 'banned', 'active', 'deleted',
                    "suspended", name='user_statuses'), default='temp', index=True)

    # Attempts and codes
    code_attempt = Column(Integer, nullable=False, default=0)
    password_attempt = Column(Integer, nullable=False, default=0)
    code_email = Column(String(CODE_TOTAL_DIGITS), nullable=True)
    code_phone = Column(String(CODE_TOTAL_DIGITS), nullable=True)

    # Timestamps
    password_issue_date = Column(DateTime, nullable=True)
    code_email_issue_date = Column(DateTime, nullable=True)
    code_phone_issue_date = Column(DateTime, nullable=True)
    token_issue_date = Column(DateTime, nullable=True)
    deletion_date = Column(DateTime, nullable=True)
    registration_date = Column(
        DateTime, default=datetime.utcnow, nullable=False)

    last_ip = Column(INET, nullable=False)
