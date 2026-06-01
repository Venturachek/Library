from datetime import datetime, timezone

from src.exceptions import CodeExpiredException, ObjectNotFoundException, NoSuchCodeException, CodeAlreadyUsedException
from src.schemas.telegram_link import UsedTelegramLink
from src.schemas.user import UserTelegramLink
from src.services.base import BaseService


class TelegramService(BaseService):

    async def add_tg_user(self, code, tg_id):
        try:
            tg_code = await self.db.tg.get_one(code=code)
        except ObjectNotFoundException:
            raise NoSuchCodeException
        print(tg_code)
        if tg_code.expires_at < datetime.now(timezone.utc):
            raise CodeExpiredException
        if tg_code.used:
            raise CodeAlreadyUsedException

        tg_data = UsedTelegramLink(used=True)
        await self.db.tg.patch(tg_data, id=tg_code.id)

        user_data = UserTelegramLink(telegram_id=tg_id)
        await self.db.user.patch(user_data, id=tg_code.user_id)
        await self.db.commit()
