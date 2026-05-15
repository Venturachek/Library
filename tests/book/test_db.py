from src.schemas.books import AddBook


async def test_books_db(db):
    query = await db.books.all_books()
    assert query is not None

