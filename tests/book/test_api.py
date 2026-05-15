from src.models.book import Genre
async def test_books_crud(login_client):
    _post = await login_client.post("/books", json={"title": "IT", "author": "Stephen King", "genre": Genre.HORROR, "price": 4})
    assert _post.status_code == 200
    _get = await login_client.get("/books", params={"title": "IT", "author": "Stephen King"})
    assert _get.status_code == 200
    res = _get.json()
    assert isinstance(res, list)
    assert len(res) > 0

