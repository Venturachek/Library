from pydantic import BaseModel

from src.models.book import BooksOrm
from src.models.loan import LoanOrm
from src.repositories.Base import BaseRepository
from src.repositories.Mapper.mappers import LoanDataMapper
from sqlalchemy import select, update


class LoanRepository(BaseRepository):
    model = LoanOrm
    mapper = LoanDataMapper

    async def return_loan(self, loan_id: int):
        stmt = update(LoanOrm).filter_by(id=loan_id).values(returned=True)
        await self.session.execute(stmt)

    async def get_book_id_by_loan(self, loan_id: int) -> int:
        res = await self.session.execute(
            select(LoanOrm.book_id).where(LoanOrm.id == loan_id)
        )
        return res.scalar_one()