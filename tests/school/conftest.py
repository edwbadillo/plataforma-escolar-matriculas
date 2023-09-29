from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from app.school.educationlevel.models import EducationLevel, Grade
from tests.faker import faker_db_func

from .academicyear.faker import fake_academic_year
from .educationlevel.faker import fake_education_level, fake_grade


@pytest.fixture
async def academic_year(db: AsyncSession) -> AcademicYear:
    current_year = date.today().year
    return await faker_db_func(
        db,
        fake_academic_year,
        year=current_year,
        start_date=date(current_year, 1, 1),
        end_date=date(current_year, 12, 31),
    )


@pytest.fixture
async def education_level(db: AsyncSession) -> EducationLevel:
    return await faker_db_func(db, fake_education_level)


@pytest.fixture
async def grade(db: AsyncSession, education_level: EducationLevel) -> Grade:
    return await faker_db_func(db, fake_grade, education_level=education_level)
