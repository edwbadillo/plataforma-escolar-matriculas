from datetime import date

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from tests.utils import check_constraint_violation, check_unique_constraint_violation


async def test_academic_year_saved(db: AsyncSession):
    """Test para la creación de un año escolar"""
    academic_year = AcademicYear(
        year=2023, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31)
    )
    db.add(academic_year)
    await db.commit()
    await db.refresh(academic_year)
    assert academic_year.id is not None


async def test_end_date_before_start_date_error(db: AsyncSession):
    """Test para la creación de un año escolar con fechas incorrectas"""
    academic_year = AcademicYear(
        year=2022, start_date=date(2022, 1, 1), end_date=date(2021, 12, 31)
    )
    db.add(academic_year)

    try:
        await db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        check_constraint_violation(e, AcademicYear, "classes_dates")


async def test_year_not_in_start_date_error(db: AsyncSession):
    """
    Test para la creación de un año escolar cuya fecha de inicio no corresponde al año
    """
    academic_year = AcademicYear(
        year=2023, start_date=date(2022, 1, 1), end_date=date(2023, 12, 31)
    )
    db.add(academic_year)

    try:
        await db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        check_constraint_violation(e, AcademicYear, "year_in_start_date")


async def test_year_not_in_end_date_error(db: AsyncSession):
    """
    Test para la creación de un año escolar cuya fecha final no corresponde al año
    """
    academic_year = AcademicYear(
        year=2023, start_date=date(2022, 1, 1), end_date=date(2024, 12, 31)
    )
    db.add(academic_year)

    try:
        await db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        check_constraint_violation(e, AcademicYear, "year_in_end_date")


async def test_year_unique_error(db: AsyncSession):
    """Test para la creación de un año escolar duplicado"""
    db.add_all(
        [
            AcademicYear(
                year=2023, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31)
            ),
            AcademicYear(
                year=2023, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31)
            ),
        ]
    )

    try:
        await db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        check_unique_constraint_violation(e, "year", 2023)
