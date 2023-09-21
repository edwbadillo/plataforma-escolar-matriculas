from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Devuelve una nueva sesión de base de datos.
    """
    engine = create_async_engine(settings.DATABASE_URL)
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
