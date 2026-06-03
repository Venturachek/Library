from src.services.loans import LoansService
from src.utils.decorators import db_dec


class LoanTools:

    @db_dec
    async def get_my_loan(self, db, tg_id):

        service = LoansService(db)

        await service.get_user_loans_by_telegram_id(telegram_id=tg_id)

