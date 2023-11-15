from fastapi import Depends, Request, APIRouter, Header

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.schemas.credentails import requestCredSchema
from database.schemas.profile import responseProfileSchema

from routes.user.responses.credentials import EXC_400, EXC_401, EXC_403, EXC_404, EXC_422, EXC_429

from utils.exceptions import RequestHTTPError
from utils.passwd import check_password
from utils.token import verify_token
from utils.code import check_code
from utils.user import get_user_by_id, get_user_by_credential, raise_if_both_email_and_phone_provided_or_none, raise_if_user_not_found


router = APIRouter()


@router.patch("/credentials", response_model=responseProfileSchema,
              summary="Set and change profile credentails",
              description="""
### Purpose:

Changing or adding login information

### How to use:

* To change or add **phone** you must send a pair of **phone** and **code** sent to it

* To change or add **email** you must send a pair of **email** and **code** sent to it

     *If the user has **password** set, it must also be specified in the request*
    
### ⚠️ Caution:

* The user has a limited time and number of attempts to enter **code**, after which the **code** will become invalid and a new one will need to be generated. The frequency of the ability to generate **code**, its lifetime and the number of attempts are set in **.env** or **config.py** file

* If the user exceeds the number of times they have incorrectly entered **password**, their **status** changes to **suspended**. The number of attempts is set in **.env** or **config.py** file

* If another user had **phone** or **email** specified in the request installed and **code** matched (this means that this user has access to **phone** or **email**), then the other users **phone** or **email** value becomes **None**

* If another user's **phone** and **email** become **None**, their **status** changes to **delete**(he cant login)

* If one-time code never been sent to the specified **phone** or **email** - you will receive a **404 error**
""",
              responses={**EXC_400, **EXC_401, **EXC_403, **EXC_404, **EXC_429, **EXC_422
                         })
async def edit_credentials(
        user_data: requestCredSchema,
        request: Request,
        JWT: str = Header(...),
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check that the request contains either email or phone

    cred_type, code_date, code_field = raise_if_both_email_and_phone_provided_or_none(
        user_data)

    # 2. Check the JWT token

    user_id = verify_token(JWT, "access")

    # 3. Get the current user by id from the token

    user = await get_user_by_id(db, user_id)

    # 4. Check two-factor authentication

    if user.password:
        if user_data.password:
            await check_password(user, user_data.password, request, db)
        else:
            raise RequestHTTPError(
                status_code=400, detail="Password is required")

    # 5. Get the user associated with the specified email or phone

    user_temp = await get_user_by_credential(db, user_data.email, user_data.phone)

    # 6. If the user is not found, return an error

    raise_if_user_not_found(user_temp)

    # 7. If the request contains the same data that is contained in the current user’s profile, return it unchanged

    if getattr(user_data, cred_type) == getattr(user, cred_type):
        return responseProfileSchema(**user.__dict__)

    # 8. Compare the code sent by the current user with the code contained in the user profile associated with the specified email or phone

    await check_code(user_temp, code_date, code_field, user_data.code, request, db)

    # 9. Delete the email or phone number of the user associated with the specified email or phone number and write to the database

    cred_type_temp = getattr(user_temp, cred_type)
    setattr(user_temp, cred_type, None)
    await db.commit()

    # 10. If the mail or phone belongs to a user with the temp status, delete it

    if user_temp.status == "temp":
        await db.delete(user_temp)

    # 11. If the user associated with the specified email or phone has no email or phone left, set the status to delete

    if (not user_temp.email) and (not user_temp.phone):
        user_temp.status = "deleted"

    # 12. Add email or phone number to the current user

    setattr(user, cred_type, cred_type_temp)
    setattr(user, code_field, getattr(user_temp, code_field))
    setattr(user, code_date, getattr(user_temp, code_date))
    user.last_ip = request.client.host
    user.password_attempt = 0

    # 13. Set changes to the database

    await db.commit()
    return responseProfileSchema(**user.__dict__)
