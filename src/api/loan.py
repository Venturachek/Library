from fastapi import APIRouter, HTTPException, Depends
from src.api.Dependencies import UserIDDep, DBDep, get_role
from src.exceptions import BookNotFound, BookNotAvailableException
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
    await LoansService(db).return_loan(loan_id=loan_id)
    return {"status": "OK"}
