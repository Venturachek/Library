from fastapi import HTTPException

from src.api.Dependencies import UserIDDep
from src.exceptions import ObjectNotFoundException, BookNotFound, BookNotAvailableException, LoanNotFound
from src.models.utils import two_weeks_from_now
from src.schemas.books import AvailabilityBook
from src.schemas.loan import Loan, AddLoan
from src.services.base import BaseService


class LoansService(BaseService):

    async def create_loan(self, user: UserIDDep, book_id: int):
        try:
            book = await self.db.books.get_filter_by(id=book_id)
        except ObjectNotFoundException:
            raise BookNotFound
        if not book.availability:
            raise BookNotAvailableException
        data_loan = AddLoan(book_id=book.id, user_id=user)
        loan_data = await self.db.loan.add(data_loan)
        patch_book = AvailabilityBook(availability=False, available_from=two_weeks_from_now())
        await self.db.books.patch(data=patch_book, id=book.id)
        await self.db.commit()
        return loan_data

    async def return_book(self, loan_id: int):
        try:
            book_id = await self.db.loan.get_book_id_by_loan(loan_id)
        except ObjectNotFoundException:
            raise LoanNotFound
        await self.db.books.patch(id=book_id, data=AvailabilityBook(availability=True, available_from=None))
        await self.db.loan.return_loan(loan_id=loan_id)
        await self.db.commit()

    async def get_loan(self, user: UserIDDep):
        try:
            loan_data = await self.db.loan.get_filter_by(user_id=user)
        except ObjectNotFoundException:
            raise LoanNotFound
        return loan_data