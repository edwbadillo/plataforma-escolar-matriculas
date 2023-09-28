from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.exceptions import AcademicYearNotFound
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


async def test_exists_by_year(db: AsyncSession, repository: AcademicYearRepository):
    academic_year = await faker_db_func(db, fake_academic_year, year=2020)

    assert await repository.exists_by_year(2020)
    assert not await repository.exists_by_year(2021)
    assert not await repository.exists_by_year(2020, exclude_id=academic_year.id)


async def test_get_by_id(db: AsyncSession, repository: AcademicYearRepository):
    await faker_db_func(db, fake_academic_year, id=1)

    academic_year = await repository.get_by_id(1)
    assert academic_year.id == 1

    with pytest.raises(AcademicYearNotFound):
        await repository.get_by_id(2)


async def test_create_academic_year(
    db: AsyncSession, repository: AcademicYearRepository
):
    academic_year = await fake_academic_year(db)
    row = await repository.save(academic_year)

    assert row.id
    assert academic_year.created_at
    assert not academic_year.updated_at


async def test_update_academic_year(
    db: AsyncSession, repository: AcademicYearRepository
):
    academic_year = await fake_academic_year(
        db, year=2023, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31)
    )
    await repository.save(academic_year)

    academic_year.year = 2024
    academic_year.start_date = date(2024, 1, 1)
    academic_year.end_date = date(2024, 12, 31)
    await repository.save(academic_year)

    await db.refresh(academic_year)
    assert academic_year.year == 2024
    assert academic_year.updated_at
