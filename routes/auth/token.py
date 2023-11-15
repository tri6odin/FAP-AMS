from datetime import datetime

from fastapi import Depends, Request, APIRouter

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.schemas.token import requestTokenSchema, responseTokenSchema

from routes.auth.responses.token import EXC_400, EXC_401, EXC_403, EXC_404, EXC_422, EXC_429

from utils.exceptions import RequestHTTPError
from utils.token import generate_tokens_with_cooldown_check
from utils.code import check_code
from utils.passwd import check_password
from utils.user import get_user_by_credential, raise_if_both_email_and_phone_provided_or_none, raise_if_user_not_found


router = APIRouter()


@router.post("/token",
             response_model=responseTokenSchema,
             summary="Get JWT and RT token",
             description="""
### Purpose:

Receiving **JWT** and **RT** tokens
             
### How to use:

* To receive **JWT** and **RT** you must send a pair of **email** and **code** sent to it

* To receive **JWT** and **RT** you must send a pair of **phone** and **code** sent to it

     *If the user has **password** set, it must also be specified in the request*
    
### ⚠️ Caution:

* The user has a limited time and number of attempts to enter **code**, after which the **code** will become invalid and a new one will need to be generated. The frequency of the ability to generate **code**, its lifetime and the number of attempts are set in **.env** or **config.py** file

* If the user exceeds the number of times they have incorrectly entered **password**, their **status** changes to **suspended**. The number of attempts is set in **.env** or **config.py** file

* The frequency of being able to generate **JWT** and **RT** is set to **.env** or **config.py** file
""",
             responses={**EXC_400, **EXC_401, **EXC_403, **EXC_404, **EXC_422, **EXC_429
                        })
async def get_token(
        user_data: requestTokenSchema,
        request: Request,
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check that the request contains either email or phone

    cred_type, code_date, code_field = raise_if_both_email_and_phone_provided_or_none(
        user_data)

    # 2. Receive the current user by mail or phone

    user = await get_user_by_credential(db, user_data.email, user_data.phone)

    # 3. If the user is not found, return a 404 error

    raise_if_user_not_found(user)

    # 4. Check two-factor authentication

    if user.password:
        if user_data.password:
            await check_password(user, user_data.password, request, db)
        else:
            raise RequestHTTPError(
                status_code=400, detail="Password is required")

    # 5. Checking the code

    await check_code(user, code_date, code_field, user_data.code, request, db)

    # 6. Check the cooldown of the token before generating, if ok – generate

    jwt_token, refresh_token = generate_tokens_with_cooldown_check(user)

    # 7. Activate the user if he is temp

    if user.status == "temp":
        user.status = "active"

    # 8. Update the last IP of the user, reset the number of attempts to enter the code and password, update the date of issue of the token

    user.code_attempt = 0
    user.password_attempt = 0
    user.last_ip = request.client.host
    user.token_issue_date = datetime.utcnow()

    # 9. Set changes to the database

    await db.commit()
    return {"JWT": jwt_token, "RT": refresh_token}
