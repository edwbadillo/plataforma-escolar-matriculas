import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.repository import AcademicYearRepository
from tests.faker import faker_db_func

from .faker import fake_academic_year


async def test_list_all_academic_years(
    db: AsyncSession, repository: AcademicYearRepository
):
    await faker_db_func(db, fake_academic_year, year=2020)
    await faker_db_func(db, fake_academic_year, year=2021)
    await faker_db_func(db, fake_academic_year, year=2022)

    academic_years_list = await repository.get_all()
    assert len(academic_years_list) == 3

    # Check order by year desc
    assert academic_years_list[0].year == 2022


async def test_exists_by_id(db: AsyncSession, repository: AcademicYearRepository):
    await faker_db_func(db, fake_academic_year, id=1)

    assert await repository.exists_by_id(1)
    assert not await repository.exists_by_id(2)


async def test_count(db: AsyncSession, repository: AcademicYearRepository):
    await faker_db_func(db, fake_academic_year, num_rows=3)

    assert await repository.count() == 3


async def test_exists_by_year(db: AsyncSession, repository: AcademicYearRepository):
    await faker_db_func(db, fake_academic_year, year=2020)

    assert await repository.exists_by_year(2020)
    assert not await repository.exists_by_year(2021)


async def test_get_by_id(db: AsyncSession, repository: AcademicYearRepository):
    await faker_db_func(db, fake_academic_year, id=1)

    academic_year = await repository.get_by_id(1)
    assert academic_year.id == 1

    with pytest.raises(sqlalchemy.exc.NoResultFound):
        await repository.get_by_id(2)

    academic_year = await repository.get_by_id(2, optional=True)
    assert academic_year is None


async def test_create_academic_year(
    db: AsyncSession, repository: AcademicYearRepository
):
    academic_year = await fake_academic_year(db)
    row = await repository.save(academic_year)
    assert row.id
