from src.models.telegram_link import TelegramLink
from src.repositories.Base import BaseRepository
from src.repositories.Mapper.mappers import TelegramLinkDataMapper


class TelegramRepository(BaseRepository):
    mapper = TelegramLinkDataMapper
    model = TelegramLink

