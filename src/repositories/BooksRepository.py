from sqlalchemy import func, select
from src.models.book import BooksOrm, Genre
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