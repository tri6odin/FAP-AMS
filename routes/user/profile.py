from fastapi import Depends, Request, APIRouter, Header

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.schemas.profile import requestProfileSchema, responseProfileSchema

from routes.user.responses.profile import EXC_401, EXC_403, EXC_404, EXC_409, EXC_422

from utils.token import verify_token
from utils.user import get_user_by_id, check_nickname_uniqueness

router = APIRouter()


@router.put("/profile", response_model=responseProfileSchema,
            summary="Get and change profile data",
            description="""
### Purpose:

Changing, adding or deleting user data

### How to use:

* To receive profile data, you must send a request without the **{}** parameter with a valid **JWT**

* To change profile data, you must send a parameter/s that match with the rules set in **.env** or **config.py** file

* To delete profile data, you must send a parameter/s equal to **null**

     *The **nickname** field is checked for uniqueness before changing*
""",
            responses={**EXC_422, **EXC_403, **EXC_404, **EXC_409, **EXC_401
                       })
async def profile(
        request: Request,
        user_data: requestProfileSchema,
        JWT: str = Header(...),
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check the JWT token

    user_id = verify_token(JWT, "access")

    # 2. Get the current user by id from the token

    user = await get_user_by_id(db, user_id)

    # 3. Check the uniqueness of the nickname if it is sent and differs from the current one

    if user_data.nickname and user_data.nickname != user.nickname:
        await check_nickname_uniqueness(db, user_data.nickname, user_id)

    # 4. Update user fields only if they were sent and differ from the current ones. If the value is null, we delete it by writing Null to the db

    fields_updated = False
    for field, value in user_data.model_dump(exclude_unset=True).items():
        if getattr(user, field) != value:
            setattr(user, field, value)
            fields_updated = True

    # 5. Set IP and changed fields to the database

    if fields_updated:
        user.last_ip = request.client.host
        await db.commit()

    return responseProfileSchema(**user.__dict__)
