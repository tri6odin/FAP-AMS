from datetime import datetime

from fastapi import Depends, Request, APIRouter, Header

from database.setup import AsyncSessionLocal
from database.crud import get_db
from database.schemas.token import responseTokenSchema

from routes.auth.responses.refresh import EXC_401, EXC_403, EXC_404, EXC_422, EXC_429

from utils.token import generate_tokens_with_cooldown_check, verify_token
from utils.user import get_user_by_id


router = APIRouter()


@router.post("/refresh", response_model=responseTokenSchema,
             summary="Refresh JWT and RT token",
             description="""
### Purpose:

Update **JWT** and **RT** token

### How to use:

* To receive updated **JWT** and **RT** you must send a valid and not expired **RT**

### ⚠️ Caution:

* The frequency of being able to generate **JWT** and **RT** is set to **.env** or **config.py** file
""",
             responses={**EXC_422, **EXC_403, **EXC_404, **EXC_429, **EXC_401
                        })
async def refresh_token(
        request: Request,
        RT: str = Header(...),
        db: AsyncSessionLocal = Depends(get_db)):

    # 1. Check the refresh token

    user_id = verify_token(RT, "refresh")

    # 2. Get the current user by id from the token

    user = await get_user_by_id(db, user_id)

    # 3. Check the cooldown of the token before generating, if ok – generate

    jwt_token, refresh_token = generate_tokens_with_cooldown_check(user)

    # 4. Update the user’s last IP and the token issuance date

    user.last_ip = request.client.host
    user.token_issue_date = datetime.utcnow()

    # 5. Set changes to the database

    await db.commit()
    return {"JWT": jwt_token, "RT": refresh_token}
