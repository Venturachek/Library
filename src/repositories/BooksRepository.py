from sqlalchemy import func, select, update
from sqlalchemy.exc import NoResultFound
from src.exceptions import BookNotFound, BookNotAvailableException
from src.models.book import BooksOrm, Genre
from src.models.utils import two_weeks_from_now
from src.repositories.Base import BaseRepository
from src.repositories.Mapper.mappers import BooksDataMapper


class BooksRepository(BaseRepository):
    model = BooksOrm
    mapper = BooksDataMapper

    async def all_books(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: Genre | None = None,
            offset: int | None = None,
            limit: int | None = None
    ):
        query = select(self.model)
        if author:
            query = query.where(func.trim(BooksOrm.author).ilike(f"%{author}%"))
        if title:
            query = query.where(func.trim(BooksOrm.title).ilike(f"%{title}%"))
        if genre:
            query = query.where(BooksOrm.genre == genre)
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain(book) for book in result.scalars().all()]

    async def try_reserve_book(self, book_id):
        query = (update(self.model)
                 .filter_by(id=book_id)
                 .where(BooksOrm.availability==True)
                 .values(availability=False, available_from=two_weeks_from_now())
                 .returning(BooksOrm)
                 )
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            raise BookNotAvailableException
        return self.mapper.map_to_domain(res)