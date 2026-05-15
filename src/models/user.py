import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Role(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class UserOrm(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    role: Mapped[Role] = mapped_column(Enum(Role, values_callable=lambda x: [e.value for e in x]), default=Role.USER)
