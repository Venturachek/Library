from pydantic import BaseModel
from datetime import datetime, timedelta, UTC
from pydantic import Field

class AddTelegramLink(BaseModel):
    user_id: int
    code: str



class TelegramLink(AddTelegramLink):
    id: int
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC) + timedelta(hours=24)
    )
    used: bool = False

class UsedTelegramLink(BaseModel):
    used: bool