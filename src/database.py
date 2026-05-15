from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_async_engine(settings.db_url)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
engine_null_pull = create_async_engine(settings.db_url, poolclass=NullPool)
async_session_maker_null_pull = async_sessionmaker(
    engine_null_pull, expire_on_commit=False
)

sync_engine = create_engine(settings.sync_db_url)
sync_session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
