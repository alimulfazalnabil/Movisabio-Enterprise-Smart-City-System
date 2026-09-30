"""
Database infrastructure using SQLAlchemy for PostgreSQL.
"""
from typing import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# Fallback to an in-memory SQLite database if the PostgreSQL URI is missing.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing a database session to FastAPI routes."""
    async with async_session_maker() as session:
        yield session
