from src.ai.tools.book import BookTools


async def test_books_db(db):
    query = await db.books.all_books()
    assert query is not None

    tool = BookTools()
    result = await tool.search_books(title="It")
    assert result is not None
    assert len(result) > 0
    assert result[0]["title"] == "It"