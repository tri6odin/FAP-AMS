from datetime import datetime, timedelta

from sqlalchemy import select
from config import CODE_COOLDOWN_SECONDS, BATCH_SIZE
from database.models.user import UserModel
from database.setup import AsyncSessionLocal
from utils.logger import logger


async def delete_temp_users():
    async with AsyncSessionLocal() as db:
        deletion_date = datetime.utcnow() - timedelta(seconds=CODE_COOLDOWN_SECONDS)
        while True:
            # A selection of users with the 'temp' status and registration date older than CODE_COOLDOWN_SECONDS, limited by batch size
            users_to_delete = await db.execute(
                select(UserModel)
                .where(UserModel.status == 'temp')
                .where(UserModel.registration_date < deletion_date)
                .limit(BATCH_SIZE)
            )
            users_to_delete = users_to_delete.scalars().all()
            if not users_to_delete:
                break  # Exit loop if there are no more users to delete
            logger.warning("Sheduler - Deleted %s profile",
                           len(users_to_delete))
            for user in users_to_delete:
                await db.delete(user)
                await db.commit()
