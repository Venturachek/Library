from src.utils.decorators import db_dec
from src.api.Dependencies import PaginationParams
from src.models.book import Genre
from src.services.books import BooksService


class BookTools:

    @db_dec
    async def search_books(
        self,
        db,
        title: str | None = None,
        author: str | None = None,
        genre: Genre | None = None,
        page: int = 1,
        per_page: int = 10
    ):

        service = BooksService(db)

        pag = PaginationParams(page=page, per_page=per_page)

        books = await service.get_books(
            title=title,
            author=author,
            genre=genre,
            pag=pag
        )

        return [
            {
                "title": b.title,
                "author": b.author,
                "genre": b.genre,
                "price": b.price,
            }
                for b in books
            ]
