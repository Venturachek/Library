from pydantic import BaseModel

from src.services.loans import LoansService
from src.utils.decorators import db_dec


class LoanTools:

    @db_dec
    async def get_my_loan(self, db, tg_id):

        service = LoansService(db)
        res =  await service.get_user_loans_by_telegram_id(telegram_id=tg_id)
        return  [
            {
            "book_id": r.book_id,
            "loan_id": r.id,
            "loan_from": r.loan_from.isoformat(),
            "loan_to": r.loan_to.isoformat(),
            "returned": r.returned
            }
                 for r in res
        ]
