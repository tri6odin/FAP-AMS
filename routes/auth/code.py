from datetime import datetime

from fastapi import BackgroundTasks, Depends, Request, APIRouter

from config import CODE_COOLDOWN_SECONDS

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.models.user import UserModel
from database.schemas.code import requestCodeSchema, responseCodeSchema

from routes.auth.responses.code import EXC_400, EXC_403, EXC_422, EXC_429, EXC_500

from utils.code import generate_code, seconds_until_next_code
from utils.exceptions import RequestHTTPError
from utils.sender import send_code
from utils.user import get_user_by_credential, raise_if_both_email_and_phone_provided_or_none


router = APIRouter()


@router.post("/code",
             response_model=responseCodeSchema,
             summary="Get one-time code",
             description="""
### Purpose:

Generating and sending a one-time code required to receive **JWT** and **RT** tokens

### How to use:

* When requesting with the **phone** parameter, the user will be sent a code to their phone

* When requesting with the **email** parameter, the user will be sent a code by email

### ⚠️ Caution:

* The frequency of being able to generate **code** is set to **.env** or **config.py** file
""",
             responses={**EXC_400, **EXC_403, **EXC_422, **EXC_429, **EXC_500
                        })
async def get_code(
        user_data: requestCodeSchema,
        background_tasks: BackgroundTasks,
        request: Request,
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check that the request contains either email or phone

    cred_type, code_date, code_field = raise_if_both_email_and_phone_provided_or_none(
        user_data)

    # 2. Receive the current user by mail or phone

    user = await get_user_by_credential(db, user_data.email, user_data.phone)

    # 3. If the user is not found

    if not user:
        # Create a new temp user
        user = UserModel(
            **user_data.model_dump())
        db.add(user)
    else:
        # Check code generation cooldown
        cooldown = seconds_until_next_code(getattr(user, code_date))
        if cooldown:
            raise RequestHTTPError(
                status_code=429, detail=f"Too many code attempts, cooldown: {cooldown}")

    # 4. Update the user code, attempt counter and last IP

    setattr(user, code_field, generate_code())
    setattr(user, code_date, datetime.utcnow())
    user.code_attempt = 0
    user.last_ip = request.client.host

    # 5. Send the code to the user’s email or phone on Background tasks

    background_tasks.add_task(send_code, user, cred_type)

    # 6. Set changes to the database

    await db.commit()
    return {"cooldown": CODE_COOLDOWN_SECONDS}
