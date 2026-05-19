from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query, HTTPException
from fastapi.params import Depends
from src.api.Dependencies import DBDep, PaginationDep, get_role
from src.exceptions import BookIsLoanedException, ObjectNotFoundException
from src.models.book import Genre
from src.models.user import Role
from src.schemas.books import AddBook, PATCHBook
from src.services.books import BooksService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", dependencies=[Depends(get_role(Role.ADMIN))])
async def add_book(db: DBDep, data: AddBook = Body()):
    res = await BooksService(db).create_book(data)
    return {"status": "OK", "data": res}

@router.post("/bulk", dependencies=[Depends(get_role(Role.ADMIN))])
async def insert_bulk_books(db: DBDep, data: list[AddBook] = Body()):
    await BooksService(db).insert_bulk_books(data)
    return {"status": "OK"}



@router.get("")
@cache(expire=20, namespace="books")
async def get_books(
        db: DBDep,
        pag: PaginationDep,
        title: str | None = Query(None),
        author: str | None = Query(None),
        genre: Genre | None = Query(None),
        ):
    return await BooksService(db).get_books(
        title=title,
        author=author,
        genre=genre,
        pag=pag
    )

@router.put("/{book_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def update_book(
        db: DBDep,
        data: AddBook,
        book_id: int
):
    res = await BooksService(db).update_book(data=data, book_id=book_id)
    return {"status": "OK", "data": res}

@router.patch("/{book_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def patch_book(
        db: DBDep,
        data: PATCHBook,
        book_id: int
):
    res = BooksService(db).patch_book(data=data, book_id=book_id)
    return {"status": "OK", "data": res}

@router.delete("/{book_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def delete_book(db: DBDep, book_id: int):
    try:
        await BooksService(db).delete_book(book_id)
    except BookIsLoanedException:
        raise HTTPException(status_code=409, detail="Book is loaned")
    except ObjectNotFoundException:
        raise HTTPException(status_code=409, detail="The book does not exist")
    return {"status": "OK"}