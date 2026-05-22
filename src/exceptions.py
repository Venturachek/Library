

class LoanException(Exception):
    detail = "Something went wrong"
    def __init__(self, *args):
        super().__init__(*args)


class ObjectNotFoundException(LoanException):
    detail = "Object Not Found"

class ObjectAlreadyExistsException(LoanException):
    detail = "Object Already Exists"

class BookNotFound(LoanException):
    detail = "Book not found"

class UserAlreadyExistsException(LoanException):
    detail = "User Already Exists"

class BookNotAvailableException(LoanException):
    detail = "Book not available"

class UserNotFoundException(LoanException):
    detail = "User Not Found"

class IncorrectUserDataException(LoanException):
    detail = "Incorrect User Data"

class BookIsLoanedException(LoanException):
    detail = "Book is Loaned"

class LoanNotFound(LoanException):
    detail = "Loan Not Found"