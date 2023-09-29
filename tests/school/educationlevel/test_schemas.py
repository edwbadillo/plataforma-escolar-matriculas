from app.school.educationlevel.models import EducationLevel, Grade
from app.school.educationlevel.schemas import EducationLevelSchema, GradeSchema


async def test_grade_schema(grade: Grade):
    grade_schema = GradeSchema.model_validate(grade)
    assert grade_schema.id == grade.id
    assert grade_schema.name == grade.name


async def test_education_level_schema(education_level: EducationLevel):
    education_level_schema = EducationLevelSchema.model_validate(education_level)
    assert education_level_schema.id == education_level.id
    assert education_level_schema.name == education_level.name
