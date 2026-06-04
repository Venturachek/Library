import pytest


@pytest.mark.parametrize("book_id",[
        (1),
        (2),
        (3)
    ]
)
async def test_crud(login_client, book_id):
    r = await login_client.post(f"/loan/{book_id}", json={"book_id": book_id})
    assert r.status_code == 200
    r = await login_client.post(f"/loan/{book_id}", json={"book_id": 2})
    assert r.status_code == 409
    returning = await login_client.patch(f"/loan/{book_id}", json={"book_id": book_id})
    assert returning.status_code == 200
    assert returning.json() == {"status": "OK"}
