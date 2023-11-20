from fastapi import Depends, APIRouter, Query

from config import PUBLIC_KEY

from database.models.key import PublicKeyModel
from database.schemas.key import responseKeySchema
from database.setup import AsyncSessionLocal
from database.crud import get_db, get_row

from routes.utils.responses.key import EXC_404, EXC_422

from utils.exceptions import RequestHTTPError

router = APIRouter()


@router.get("/public_key", response_model=responseKeySchema,
            summary="Get public key",
            description="""
### Purpose:

Receiving **public key** by other microservices for validation **JWT**

### How to use:

* When requested with the **version** parameter, returns the requested version **public key**

* When requested without the parameter, returns the **actual** version of **public key**

### ⚠️ Caution:

* After changing the **public key** and **private key** pair, you must restart the microservice. They will be added with a new **version** number to the database on the first request without parameter and will become **actual**
""",
            responses={**EXC_404, **EXC_422})
async def public_key(
    version: int = Query(None, alias="version"),
    db: AsyncSessionLocal = Depends(get_db)
):
    # Check if the key version was transferred
    if version != None:
        # Looking for the version key
        filter_ = PublicKeyModel.version == version
        result = await get_row(db, PublicKeyModel, filter_)
        key = result.scalar_one_or_none()
        # If the key is not found, return an error
        if key is None:
            raise RequestHTTPError(
                status_code=404, detail="Version of public key does not exist")
    else:
        # Looking for the default key (PUBLIC_KEY)
        filter_ = PublicKeyModel.public_key == PUBLIC_KEY
        result = await get_row(db, PublicKeyModel, filter_)
        key = result.scalar_one_or_none()
        # If the key is not found, create it
        if key is None:
            key = PublicKeyModel(public_key=PUBLIC_KEY)
            db.add(key)
            await db.commit()
            await db.refresh(key)
    # Return the key
    return responseKeySchema(**key.__dict__)
