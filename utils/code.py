import random
from datetime import datetime
from typing import Union

from config import CODE_ATTEMPT, CODE_COOLDOWN_SECONDS, CODE_TOTAL_DIGITS, CODE_UNIQUE_DIGITS
from utils.exceptions import RequestHTTPError

# Code checking. Returns True if the password is correct and an exception if not


async def check_code(user, code_date, code_field, user_data_code, request, db):
    # We check whether the code has expired and whether it is necessary to wait before the next attempt to enter the code
    code_cooldown = seconds_until_next_code(getattr(user, code_date))
    if code_cooldown is False:
        raise RequestHTTPError(status_code=401, detail="Code has expired")
    elif code_cooldown and user.code_attempt >= CODE_ATTEMPT:
        raise RequestHTTPError(
            status_code=429, detail=f"Too many code attempts, cooldown: {code_cooldown}")
    # If the password is incorrect, write down the user's attempt and IP address
    if getattr(user, code_field) != user_data_code:
        user.code_attempt += 1
        user.last_ip = request.client.host
        await db.commit()
        raise RequestHTTPError(status_code=401, detail="Invalid code")
    return True


# Calculating the time until the next code, returns either seconds or false

def seconds_until_next_code(issue_date: datetime) -> Union[str, bool]:
    seconds_remaining = CODE_COOLDOWN_SECONDS - \
        int((datetime.utcnow() - issue_date).total_seconds())
    if seconds_remaining > 0:
        return str(seconds_remaining)
    return False


# Beautiful code generation

def generate_code():
    # Check that the number of unique characters and the total number of characters meet the requirements
    if CODE_UNIQUE_DIGITS > CODE_TOTAL_DIGITS or CODE_UNIQUE_DIGITS > 10:
        raise RequestHTTPError(
            status_code=500, detail="Total or unique digits param error", hide_details_in_prod=True)
    # Select unique numbers
    unique_digits = random.sample(
        range(10), CODE_UNIQUE_DIGITS)
    final_digits = unique_digits.copy()
    # Add random digits from unique ones to the list until its length reaches TOTAL_DIGITS
    while len(final_digits) < CODE_TOTAL_DIGITS:
        final_digits.append(random.choice(unique_digits))
    # Mix the numbers
    random.shuffle(final_digits)
    # Convert the list of numbers to a string and return
    return ''.join(map(str, final_digits))
