from datetime import datetime, timedelta, timezone, UTC

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TelegramLink(Base):
    __tablename__ = "telegram_link"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC) + timedelta(minutes=10)
    )
    used: Mapped[bool] = mapped_column(default=False, nullable=False)
    
