from src.models.user import UserOrm
from src.repositories.Base import BaseRepository
from src.repositories.Mapper.mappers import UserDataMapper
from sqlalchemy import select

from src.schemas.user import UserHashedPassword


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_by_email(self, email: str):
        query = select(self.model).filter_by(email=email)

        model = await self.session.execute(query)
        res = model.scalars().one()
        return UserHashedPassword.model_validate(res, from_attributes=True)