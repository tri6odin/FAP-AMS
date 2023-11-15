from datetime import datetime

from fastapi import Depends, Request, APIRouter, Header

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.schemas.delete import requestDeleteSchema, responseDeleteSchema

from routes.user.responses.delete import EXC_401, EXC_403, EXC_404, EXC_422

from utils.exceptions import RequestHTTPError
from utils.passwd import check_password
from utils.token import verify_token
from utils.user import get_user_by_id


router = APIRouter()


@router.delete("/profile",
               response_model=responseDeleteSchema,
               summary="Delete profile",
               description="""
### Purpose:

Deleting a user

### How to use:

* To delete a user, you must send a request without the **{}** parameter with a valid **JWT**

     *If the user has **password**, it must be specified in the request*

     *After a valid request, the profile is not deleted: its **status** changes to **delete** and the user loses the ability to perform any operations with the profile*
    
### ⚠️ Caution:

* If the user exceeds the number of times they have incorrectly entered **password**, their **status** changes to **suspended**. The number of attempts is set in **.env** or **config.py** file

* The user will permanently lose access to other microservices only after the expiration of **JWT**
""",
               responses={**EXC_422, **EXC_403, **EXC_404, **EXC_401
                          })
async def delete_profile(
        user_data: requestDeleteSchema,
        request: Request,
        JWT: str = Header(...),
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check the JWT token

    user_id = verify_token(JWT, "access")

    # 2. Get the user by id from the token

    user = await get_user_by_id(db, user_id)

    # 3. Check two-factor authentication

    if user.password:
        if user_data.password:
            await check_password(user, user_data.password, request, db)
        else:
            raise RequestHTTPError(
                status_code=400, detail="Password is required")

    # 4. Update user data

    user.last_ip = request.client.host
    user.deletion_date = datetime.utcnow()
    user.status = "deleted"

    # 5. Set changes to the database

    await db.commit()
    return {"detail": "Profile deleted successfully"}
