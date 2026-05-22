from fastapi import Query, HTTPException, Body

from src.exceptions import BookNotFound, ObjectNotFoundException
from src.models.book import Genre
from src.schemas.books import AddBook, PATCHBook
from src.services.base import BaseService


class BooksService(BaseService):
    async def get_books(
            self,
            pag,
            title: str | None = Query(None),
            author: str | None = Query(None),
            genre: Genre | None = Query(None),
    ):
        per_page = pag.per_page or 5
        try:
            return await self.db.books.all_books(
                title=title,
                author=author,
                genre=genre,
                limit=per_page,
                offset=per_page * (pag.page - 1)
            )
        except BookNotFound as e:
            raise HTTPException(status_code=404, detail=e.detail)


    async def create_book(self, data: AddBook = Body()):
        data = await self.db.books.add(data)
        await self.db.commit()
        return data

    async def insert_bulk_books(self, data: list[AddBook] = Body()):
        await self.db.books.add_bulk(data)
        await self.db.commit()

    async def update_book(self, data: AddBook, book_id: int):
        await self.db.books.update(data, id=book_id)
        await self.db.commit()

    async def patch_book(self, data: PATCHBook, book_id: int):
        await self.db.books.patch(data, id=book_id)
        await self.db.commit()

    async def delete_book(self, book_id: int):
        await self.db.books.delete(id=book_id)
        await self.db.commit()
