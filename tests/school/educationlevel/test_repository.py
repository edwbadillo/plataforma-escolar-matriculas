import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.educationlevel.models import EducationLevel, Grade
from app.school.educationlevel.repository import (
    EducationalLevelRepository,
    GradeRepository,
    Sort,
)
from tests.faker import faker_db_func

from .faker import fake_education_level, fake_grade


@pytest.fixture
async def education_level_repository(db: AsyncSession):
    return EducationalLevelRepository(db)


@pytest.fixture
def grade_repository(db: AsyncSession):
    return GradeRepository(db)


async def test_list_education_levels(
    db: AsyncSession, education_level_repository: EducationalLevelRepository
):
    await faker_db_func(db, fake_education_level, order=200)
    await faker_db_func(db, fake_education_level, order=100)
    await faker_db_func(db, fake_education_level, order=500)

    education_levels: list[EducationLevel] = await education_level_repository.get_all()
    assert len(education_levels) == 3

    # El primer registro debe corresponder al más bajo nivel
    assert education_levels[0].order == 100

    # Cambio de modo de ordenamiento
    education_levels = await education_level_repository.get_all(Sort.DESC)
    assert education_levels[0].order == 500


async def test_list_grades(
    db: AsyncSession, grade_repository: GradeRepository, education_level: EducationLevel
):
    await faker_db_func(db, fake_grade, order=200, education_level=education_level)
    await faker_db_func(db, fake_grade, order=100, education_level=education_level)
    await faker_db_func(db, fake_grade, order=500, education_level=education_level)

    grades: list[Grade] = await grade_repository.get_all()
    assert len(grades) == 3

    # El primer registro debe corresponder al más bajo nivel
    assert grades[0].order == 100

    # Cambio de modo de ordenamiento
    grades = await grade_repository.get_all(order=Sort.DESC)
    assert grades[0].order == 500


async def test_list_grades_by_education_level(
    db: AsyncSession, grade_repository: GradeRepository, education_level: EducationLevel
):
    await faker_db_func(db, fake_grade, education_level=education_level)

    other_education_level = await faker_db_func(db, fake_education_level)
    await faker_db_func(db, fake_grade, education_level=other_education_level)

    all_grades = await grade_repository.get_all()
    assert len(all_grades) == 2

    grades = await grade_repository.get_all(by_education_level=education_level)
    assert len(grades) == 1 and grades[0].id

    other_grades = await grade_repository.get_all(
        by_education_level=other_education_level.id
    )
    assert len(other_grades) == 1


async def test_education_level_exists_by_id(
    education_level_repository: EducationalLevelRepository,
    education_level: EducationLevel,
):
    assert await education_level_repository.exists_by_id(education_level.id)
    assert not await education_level_repository.exists_by_id(education_level.id + 1)


async def test_grade_exists_by_id(grade_repository: GradeRepository, grade: Grade):
    assert await grade_repository.exists_by_id(grade.id)
    assert not await grade_repository.exists_by_id(grade.id + 1)
