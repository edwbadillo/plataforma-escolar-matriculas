import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from app.common.database.models import Base
from app.config import settings


async def migrate():
    from app.school.academicyear.models import AcademicYear  # noqa
    from app.school.grade.models import Grade  # noqa

    print("Creating tables...")

    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Tables created!")


if __name__ == "__main__":
    asyncio.run(migrate())
