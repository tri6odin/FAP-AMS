from datetime import datetime

from fastapi import Depends, Request, APIRouter, Header

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.schemas.password import requestPasswordSchema, responsePasswordSchema

from routes.user.responses.password import EXC_400, EXC_401, EXC_403, EXC_404, EXC_422

from utils.exceptions import RequestHTTPError
from utils.token import verify_token
from utils.passwd import check_password, hash_password
from utils.user import get_user_by_id

router = APIRouter()


@router.post("/password", response_model=responsePasswordSchema,
             summary="Set, change and delete profile password",
             description="""
### Purpose:

Changing, adding or deleting **password**

### How to use:

* To add **password** you must send **password**

* To change **password** you must send **old_password** and **password**

* To delete **password** you must send **old_password** and **password** equal to **null**
    
### ⚠️ Caution:

* If the user exceeds the number of times they have incorrectly entered **password**, their **status** changes to **suspended**. The number of attempts is set in **.env** or **config.py** file

* After adding **password**, it will need to be specified in requests to the **user/credentails**, **user/delete** and **auth/token** endpoints
""",
             responses={**EXC_400, **EXC_422, **EXC_403, **EXC_404, **EXC_401
                        })
async def edit_password(
        user_data: requestPasswordSchema,
        request: Request,
        JWT: str = Header(...),
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check the JWT token

    user_id = verify_token(JWT, "access")

    # 2. Get the current user by id from the token

    user = await get_user_by_id(db, user_id)

    # 3. If the user already has a password

    if user.password:
        # Check for the presence of old_password in the request
        if not user_data.old_password:
            raise RequestHTTPError(
                status_code=400, detail="Old password is required")
        # Check that old_password matches the password in the db
        await check_password(user, user_data.old_password, request, db)

    # 4. Update the user's last IP, password and password change date, password attempts

    user.last_ip = request.client.host
    user.password = hash_password(user_data.password)
    user.password_attempt = 0
    user.password_issue_date = datetime.utcnow()

    # 5. Set changes to the database

    await db.commit()
    return {"detail": "Password was set successfully"}
