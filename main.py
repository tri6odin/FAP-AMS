from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from contextlib import asynccontextmanager

from utils.exceptions import RequestHTTPError, custom_http_handler, custom_pydantic_handler
from utils.scheduler import delete_temp_users
from utils.logger import logger

from database.models.key import PublicKeyModel
from database.models.user import UserModel
from database.crud import create_table

from config import REDOC, SWAGGER, SCHEDULER_FREQUENCY_SECONDS

from routes.user import credentials, delete, profile, password
from routes.auth import code, refresh, token
from routes.utils import key


# Create and start scheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(delete_temp_users, 'interval',
                  seconds=SCHEDULER_FREQUENCY_SECONDS)
scheduler.start()


# Create db before startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_table(UserModel)
        await create_table(PublicKeyModel)
        logger.info("Database - Connected")
        yield
        logger.info("App - Stopped")
    except Exception as e:
        logger.critical("Database - %s", str(e))

app = FastAPI(
    lifespan=lifespan,
    title="FAP-AMS",
    version="1.0.0",
    docs_url="/docs" if SWAGGER else None,
    redoc_url="/redoc" if REDOC else None,
    license_info={
        "name": "MIT License",
        "url": "https://github.com/tri6odin/FAP-AMS/blob/main/LICENSE.MD",
    },
    description="""
### ⚠️ Caution:

* Don't forget to add the parameter `hide_details_in_prod = True` for all **RequestHTTPErrors** that you want to hide detailed exceptions, and set `DEV_MODE = False` in the config before deploying to prod

### To change the configuration:

* If using **Docker** - modify `.env` and restart **container**:

    ```bash
    docker stop auth_microservice && docker rm auth_microservice
    docker run -d --env-file .env -p 8000:8000 auth_microservice
    ```

* If using **local version** - modify `config.py` and restart **uvicorn**:

    Press `Control`+`C` to stop server and `uvicorn main:app --reload` to start again
---
""")
logger.info("App - Started")

# Catching and decorating errors
app.exception_handler(RequestHTTPError)(
    custom_http_handler)
app.exception_handler(RequestValidationError)(
    custom_pydantic_handler)

# Including routes
app.include_router(key.router, prefix="/utils", tags=["Utils"])

app.include_router(code.router, prefix="/auth", tags=["Authentication"])
app.include_router(token.router, prefix="/auth", tags=["Authentication"])
app.include_router(refresh.router, prefix="/auth", tags=["Authentication"])

app.include_router(profile.router, prefix="/user", tags=["User"])
app.include_router(credentials.router, prefix="/user", tags=["User"])
app.include_router(password.router, prefix="/user", tags=["User"])
app.include_router(delete.router, prefix="/user", tags=["User"])
