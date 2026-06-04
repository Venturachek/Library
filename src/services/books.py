from src.api.Dependencies import PaginationParams
from src.models.book import Genre
from src.schemas.books import AddBook, PATCHBook
from src.services.base import BaseService


class BooksService(BaseService):
    async def get_books(
            self,
            pag: PaginationParams,
            title: str | None = None,
            author: str | None = None,
            genre: Genre | None = None,
    ):
        per_page = pag.per_page or 5
        return await self.db.books.all_books(
                title=title,
                author=author,
                genre=genre,
                limit=per_page,
                offset=per_page * (pag.page - 1)
            )


    async def create_book(self, data: AddBook):
        data = await self.db.books.add(data)
        await self.db.commit()
        return data

    async def insert_bulk_books(self, data: list[AddBook]):
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
