from src.database import async_session_maker
from src.models.book import Genre
from src.utils.dbmanager import DBManager


async def search_books(
        title: str | None = None,
        author: str | None = None,
        genre: Genre | None = None,
    ):
    async with DBManager(session_factory=async_session_maker) as db:

        books = await db.books.all_books(
            title=title,
            author=author,
            genre=genre,
            limit=10,
            offset=0
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
