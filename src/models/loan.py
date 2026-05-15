from datetime import date

from sqlalchemy import ForeignKey, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.models.utils import two_weeks_from_now


class LoanOrm(Base):
    __tablename__ = "loan"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    loan_from: Mapped[date] = mapped_column(Date, default=date.today)
    loan_to: Mapped[date] = mapped_column(Date, default=two_weeks_from_now)
    returned: Mapped[bool] = mapped_column(Boolean, default=False)
