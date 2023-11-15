import bcrypt
from config import PASSWORD_ATTEMPT
from utils.exceptions import RequestHTTPError

from utils.user import check_user_status


# Password hashing

def hash_password(password: str) -> str:
    # If the value is null, set it to None in the database
    if password is None:
        return None
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


# Compare password with hash

async def check_password(user, password, request, db):
    check_user_status(user.status)
    if user.password_attempt >= PASSWORD_ATTEMPT:
        user.status = "suspended"
        user.last_ip = request.client.host
        await db.commit()
        raise RequestHTTPError(
            status_code=403, detail="Account is suspended. Please contact support")
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # If the password is incorrect, write down the user's attempt and IP address
        user.password_attempt += 1
        user.last_ip = request.client.host
        await db.commit()
        raise RequestHTTPError(status_code=403, detail="Invalid password")
    return True
