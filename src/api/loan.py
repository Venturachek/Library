from fastapi import APIRouter, HTTPException, Depends
from src.api.Dependencies import UserIDDep, DBDep, get_role
from src.exceptions import BookNotFound
from src.models.user import Role
from src.models.utils import two_weeks_from_now
from src.schemas.books import AvailabilityBook
from src.schemas.loan import AddLoan

router = APIRouter(prefix="/loan", tags=["loan"])

@router.post("/{book_id}")
async def loan_book(user: UserIDDep, db: DBDep, book_id: int):
    try:
        book = await db.books.get_filter_by(id=book_id)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    if not book.availability:
        raise HTTPException(status_code=409, detail="Book not available")
    data_loan = AddLoan(book_id=book.id, user_id=user)
    loan_data = await db.loan.add(data_loan)
    patch_book = AvailabilityBook(availability=False, available_from=two_weeks_from_now())
    await db.books.patch(data=patch_book, id=book.id)
    await db.commit()
    return {"status": "ok", "data": loan_data}

@router.patch("/{loan_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def loan_returned(loan_id: int, db: DBDep):
    await db.loan.returning_book(loan_id)
    await db.commit()
    return {"status": "OK"}
