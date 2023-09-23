import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from app.school.academicyear.repository import AcademicYearRepository

from .faker import fake_academic_year


@pytest.fixture
def repository(db: AsyncSession):
    return AcademicYearRepository(db, AcademicYear)


async def test_list_all_academic_years(
    db: AsyncSession, repository: AcademicYearRepository
):
    await fake_academic_year(db, year=2020)
    await fake_academic_year(db, year=2021)
    await fake_academic_year(db, year=2022)

    academic_years_list = await repository.get_all()
    assert len(academic_years_list) == 3

    # Check order by year desc
    assert academic_years_list[0].year == 2022


async def test_exists_by_id(db: AsyncSession, repository: AcademicYearRepository):
    await fake_academic_year(db, id=1)

    assert await repository.exists_by_id(1)
    assert not await repository.exists_by_id(2)


async def test_count(db: AsyncSession, repository: AcademicYearRepository):
    await fake_academic_year(db, num_rows=3)

    assert await repository.count() == 3


async def test_exists_by_year(db: AsyncSession, repository: AcademicYearRepository):
    await fake_academic_year(db, year=2020)

    assert await repository.exists_by_year(2020)
    assert not await repository.exists_by_year(2021)
