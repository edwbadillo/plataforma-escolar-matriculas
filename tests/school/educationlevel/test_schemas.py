from sqlalchemy.ext.asyncio import AsyncSession

from app.school.educationlevel.models import EducationLevel, Grade
from app.school.educationlevel.schemas import (
    EducationLevelSchema,
    EducationLevelsInformation,
    GradeSchema,
)
from tests.faker import faker_db_func

from .faker import fake_grade


async def test_grade_schema(grade: Grade):
    grade_schema = GradeSchema.model_validate(grade)
    assert grade_schema.id == grade.id
    assert grade_schema.name == grade.name


async def test_education_level_schema(
    db: AsyncSession, education_level: EducationLevel
):
    grade_db = await faker_db_func(db, fake_grade, education_level=education_level)
    await db.refresh(education_level, ["grades"])

    education_level_schema = EducationLevelSchema.model_validate(education_level)
    assert education_level_schema.id == education_level.id
    assert education_level_schema.name == education_level.name
    assert len(education_level_schema.grades)

    grade = education_level_schema.grades[0]
    assert grade.id == grade_db.id
    assert grade.name == grade_db.name


async def test_education_levels_information_schema(
    db: AsyncSession, education_level: EducationLevel
):
    await faker_db_func(db, fake_grade, education_level=education_level)
    await db.refresh(education_level, ["grades"])

    schema = EducationLevelsInformation(education_levels=[education_level])
    assert len(schema.education_levels) == 1
