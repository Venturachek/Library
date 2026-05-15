from pydantic import BaseModel

from src.models.book import BooksOrm
from src.models.loan import LoanOrm
from src.repositories.Base import BaseRepository
from src.repositories.Mapper.mappers import LoanDataMapper
from sqlalchemy import insert, select, delete, update

from src.schemas.books import PATCHBook, AvailabilityBook
from src.schemas.loan import ReturnLoan


class LoanRepository(BaseRepository):
    model = LoanOrm
    mapper = LoanDataMapper

    async def returning_book(self, loan_id: int):
        query = select(LoanOrm.book_id).where(LoanOrm.id == loan_id)
        res = await self.session.execute(query)
        book = res.scalar_one()
        book_data = AvailabilityBook(availability=True, available_from=None)
        patch_stmt = update(BooksOrm).filter_by(id=book).values(**book_data.model_dump(exclude_unset=True))
        await self.session.execute(patch_stmt)
        loan_data = ReturnLoan(returned=True)
        patch_loan_stmt = update(LoanOrm).filter_by(id=loan_id).values(**loan_data.model_dump(exclude_unset=True))
        await self.session.execute(patch_loan_stmt)

