from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("LOD_DATABASE_URL_ASYNC", None)
ENGINE_ECHO_SQL = os.getenv("LOD_ENGINE_ECHO_SQL", "0")
API_PATH = os.getenv("API_PATH", "api")
API_VERSION = os.getenv("API_VERSION", "v2")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("LOD_DATABASE_URL_ASYNC is not set")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=bool(int(ENGINE_ECHO_SQL)))

async_session_maker = async_sessionmaker(
    bind=engine,
    future=True,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
