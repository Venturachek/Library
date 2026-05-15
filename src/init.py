from src.config import settings
from src.connectors.redis_manager import RedisManager

redis_conn = RedisManager(host=settings.REDIS_HOST,port=settings.REDIS_PORT)