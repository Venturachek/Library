from src.api.Dependencies import UserIDDep
from src.exceptions import ObjectNotFoundException, BookNotAvailableException, LoanNotFound
from src.schemas.books import AvailabilityBook
from src.schemas.loan import AddLoan
from src.services.base import BaseService


class LoansService(BaseService):

    async def create_loan(self, user: int, book_id: int):
        try:
            await self.db.books.try_reserve_book(book_id=book_id)
        except BookNotAvailableException:
            raise BookNotAvailableException
        data_loan = AddLoan(book_id=book_id, user_id=user)
        loan_data = await self.db.loan.add(data_loan)
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

    async def get_loan(self, user: int):
        try:
            loan_data = await self.db.loan.get_filter_by(user_id=user)
        except ObjectNotFoundException:
            raise LoanNotFound
        return loan_data

    async def get_user_loans_by_telegram_id(
            self,
            telegram_id: int,
        ):
        user = await self.db.user.get_one(
            telegram_id=telegram_id
        )

        return await self.db.loan.get_filter_by(
            user_id=user.id
        )
