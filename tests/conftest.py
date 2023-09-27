from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.common.database.session import get_db
from app.config import settings
from app.main import app
from scripts.migrate import migrate_db


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Crea la sesión con la base de datos de pruebas, se debe tener una base de datos
    cuyo nombre sea igual al de desarrollo pero con el sufijo _test
    """
    db_name = settings.DATABASE_URL.split("/")[-1]
    db_url = settings.DATABASE_URL.replace(f"/{db_name}", f"/{db_name}_test")

    engine = create_async_engine(db_url, echo=True)

    async with engine.begin() as conn:
        await migrate_db(conn, reset_db=True)

    session = async_sessionmaker(engine, expire_on_commit=False)()
    yield session
    await session.close()


@pytest.fixture()
def test_app(db: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db] = lambda: db
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(
        app=test_app, base_url="http://127.0.0.1:8000/api"
    ) as client:
        yield client
