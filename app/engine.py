from __future__ import annotations

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("LOD_DATABASE_URL_ASYNC")
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    future=True,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
