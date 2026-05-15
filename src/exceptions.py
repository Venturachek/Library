

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

