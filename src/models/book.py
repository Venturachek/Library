from datetime import datetime
import enum
from sqlalchemy import String, Boolean, true, DateTime, Integer, Enum
from sqlalchemy.orm import mapped_column, Mapped
from src.database import Base

class Genre(str, enum.Enum):
    FICTION = 'fiction'
    NON_FICTION = 'non-fiction'
    SCIENCE = 'science'
    DETECTIVE = 'detective'
    HORROR = 'horror'




class BooksOrm(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    genre: Mapped[str] = mapped_column(Enum(Genre))
    price: Mapped[int] = mapped_column(Integer)
    availability: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=true()
    )
    available_from: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )


