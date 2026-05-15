from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path
import logging
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.DEBUG)

from src.init import redis_conn
from src.api.book import router as book_router
from src.api.auth import router as auth_router
from src.api.loan import router as loan_router
from src.api.tasks import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_conn.connect()
    FastAPICache.init(RedisBackend(redis_conn.redis), prefix="lifespan")
    yield
    await redis_conn.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(loan_router)
app.include_router(task_router)

if __name__ == '__main__':
    uvicorn.run("main:app")
