from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query, HTTPException
from fastapi.params import Depends

from src.api.Dependencies import DBDep, PaginationDep, get_role
from src.exceptions import BookNotFound, ObjectAlreadyExistsException
from src.models.book import Genre
from src.models.user import Role
from src.schemas.books import AddBook, PATCHBook

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", dependencies=[Depends(get_role(Role.ADMIN))])
async def add_book(db: DBDep, data: AddBook = Body()):
    try:
        res = await db.books.add(data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Book already exists")
    return {"status": "OK", "data": res}

@router.post("/bulk", dependencies=[Depends(get_role(Role.ADMIN))])
async def insert_bulk_book(db: DBDep, data: list[AddBook] = Body()):
    await db.books.add_bulk(data)
    await db.commit()
    return {"status": "OK"}



@router.get("")
@cache(expire=20)
async def get_books(
        db: DBDep,
        pag: PaginationDep,
        title: str | None = Query(None),
        author: str | None = Query(None),
        genre: Genre | None = Query(None),

        ):
    per_page = pag.per_page or 5
    try:
        return await db.books.all_books(
            title=title,
            author=author,
            genre=genre,
            limit=per_page,
            offset=per_page * (pag.page - 1)
        )
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.put("/{book_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def update_book(
        db: DBDep,
        data: AddBook,
        book_id: int
):
    res = await db.books.update(data, id=book_id)
    await db.commit()
    return {"status": "OK", "data": res}

@router.patch("/{book_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def patch_book(
        db: DBDep,
        data: PATCHBook,
        book_id: int
):
    res = await db.books.patch(data, id=book_id)
    await db.commit()
    return {"status": "OK", "data": res}

@router.delete("/{book_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def delete_book(db: DBDep, book_id: int):
    try:
        await db.books.delete(id=book_id)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    await db.commit()
    return {"status": "OK"}