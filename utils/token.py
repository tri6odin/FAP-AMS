import jwt
from jwt.exceptions import ExpiredSignatureError

from typing import Union
from datetime import datetime, timedelta
from config import JWT_EXPIRATION_MINUTES, PRIVATE_KEY, PUBLIC_KEY, RT_EXPIRATION_HOURS, TOKEN_COOLDOWN_SECONDS

from utils.exceptions import RequestHTTPError


# Check the ability to generate tokens

def generate_tokens_with_cooldown_check(user):
    # Check cooldown before generation
    token_cooldown = seconds_until_next_token(
        user.token_issue_date) if user.token_issue_date else False
    if token_cooldown:
        raise RequestHTTPError(
            status_code=429, detail=f"Too many token attempts, cooldown: {token_cooldown}")
    # Generate tokens
    jwt_token = encode_token(user.id, "access")
    refresh_token = encode_token(user.id, "refresh")

    return jwt_token, refresh_token


# Calculating the time until the next token, returns either seconds or false

def seconds_until_next_token(issue_date: datetime) -> Union[str, bool]:
    seconds_remaining = TOKEN_COOLDOWN_SECONDS - \
        int((datetime.utcnow() - issue_date).total_seconds())
    if seconds_remaining > 0:
        return str(seconds_remaining)
    return False


# Check token type, returns ID or exception

def verify_token(jwt_token: str, token_type: str) -> str:
    decoded_token = decode_token(jwt_token)
    if decoded_token["type"] != token_type:
        raise RequestHTTPError(
            status_code=401, detail=f"Expected an {token_type} token")
    return decoded_token["id"]


# Token encoding

def encode_token(data: int, token_type: str) -> str:
    if token_type == 'access':
        EXPIRATION_MINUTES = JWT_EXPIRATION_MINUTES
    else:
        EXPIRATION_MINUTES = RT_EXPIRATION_HOURS * 60
    payload = {
        "id": data,
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }
    return jwt.encode(payload, PRIVATE_KEY, "RS256")


# Token decoding

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, PUBLIC_KEY, "RS256")
    except jwt.InvalidSignatureError:
        raise RequestHTTPError(
            status_code=422, detail="Token has an invalid signature")
    except ExpiredSignatureError:
        raise RequestHTTPError(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise RequestHTTPError(
            status_code=422, detail="Invalid token format")
