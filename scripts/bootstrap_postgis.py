"""Enable PostGIS before SQLAlchemy creates geometry-backed tables."""

import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from backend.app.config import settings


async def main() -> None:
    engine = create_async_engine(settings.async_database_url)
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
