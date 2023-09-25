import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from tests.faker import faker_db_func

from .academicyear.faker import fake_academic_year


@pytest.fixture
async def academic_year(db: AsyncSession) -> AcademicYear:
    return await faker_db_func(db, fake_academic_year)
