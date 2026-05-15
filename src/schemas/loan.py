from datetime import date

from pydantic import BaseModel, ConfigDict


class AddLoan(BaseModel):
    book_id: int
    user_id: int

class Loan(AddLoan):
    id: int
    loan_from: date
    loan_to: date
    returned: bool

    model_config = ConfigDict(from_attributes=True)

class ReturnLoan(BaseModel):
    returned: bool