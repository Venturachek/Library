from fastapi import APIRouter, HTTPException, Depends
from src.api.Dependencies import UserIDDep, DBDep, get_role
from src.exceptions import BookNotFound, BookNotAvailableException, ObjectNotFoundException
from src.models.user import Role
from src.services.loans import LoansService

router = APIRouter(prefix="/loan", tags=["loan"])

@router.post("/{book_id}")
async def loan_book(user: UserIDDep, db: DBDep, book_id: int):
    try:
        loan_data = await LoansService(db).create_loan(user=user, book_id=book_id)
    except BookNotAvailableException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "ok", "data": loan_data}

@router.patch("/{loan_id}", dependencies=[Depends(get_role(Role.ADMIN))])
async def loan_returned(loan_id: int, db: DBDep):
    try:
        await LoansService(db).return_book(loan_id=loan_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"status": "OK"}

@router.get("")
async def get_loan(db: DBDep, user: UserIDDep):
    try:
        loan_data = await LoansService(db).get_loan(user=user)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"status": "ok", "data": loan_data}

