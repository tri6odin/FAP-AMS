from database.crud import get_row
from database.setup import AsyncSessionLocal
from database.models.user import UserModel
from typing import Optional, Union

from utils.exceptions import RequestHTTPError


# Throws an exception if the user is not found

def raise_if_user_not_found(user):
    if not user:
        raise RequestHTTPError(status_code=404, detail="User not found")


# Throws an exception if both fields (email and phone) are provided or both fields are empty

def raise_if_both_email_and_phone_provided_or_none(user_data):
    if not (bool(user_data.email) ^ bool(user_data.phone)):
        raise RequestHTTPError(
            status_code=400, detail="Either email or phone must be provided")

    cred_type = "email" if user_data.email else "phone"
    code_date = f"code_{cred_type}_issue_date"
    code_field = f"code_{cred_type}"

    return cred_type, code_date, code_field


# Status check

def check_user_status(status: str):
    if status == "suspended":
        raise RequestHTTPError(
            status_code=403, detail="Account is suspended. Please contact support")
    elif status == "deleted":
        raise RequestHTTPError(status_code=403, detail="Account is deleted")
    elif status == "banned":
        raise RequestHTTPError(status_code=403, detail="Account is banned")


# Receiving a user by mail or phone

async def get_user_by_credential(db: AsyncSessionLocal, email: Optional[str], phone: Optional[str]) -> Union[UserModel, None]:
    # Define the filter based on whether an email or phone is provided
    filter_ = UserModel.email == email if email else UserModel.phone == phone
    result = await get_row(db, UserModel, filter_)
    user = result.scalar_one_or_none()
    if user:
        check_user_status(user.status)
    return user


# Getting user by id

async def get_user_by_id(db: AsyncSessionLocal, user_id: str) -> UserModel:
    filter_ = UserModel.id == user_id
    result = await get_row(db, UserModel, filter_)
    user = result.scalar_one_or_none()
    raise_if_user_not_found(user)
    check_user_status(user.status)
    return user


# Nickname uniqueness check

async def check_nickname_uniqueness(db: AsyncSessionLocal, nickname, current_user_id):
    filter_ = UserModel.nickname == nickname
    result = await get_row(db, UserModel, filter_)
    user_with_nickname = result.scalar_one_or_none()
    if user_with_nickname and user_with_nickname.id != current_user_id:
        raise RequestHTTPError(
            status_code=409, detail="Nickname already exists")
