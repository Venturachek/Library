from src.ai.tools.book import BookTools
from src.ai.tools.loan import LoanTools

TOOLS_MAP = {
    "search_books": BookTools().search_books,
    "get_loans": LoanTools().get_my_loan,
}
