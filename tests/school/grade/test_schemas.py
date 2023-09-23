from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade
from app.school.grade.schemas import GradeSchema
from tests.faker import faker_db_func

from .faker import fake_grade


async def test_grades_schema_list(db: AsyncSession):
    """Verifique que no haya problema al convertir a un modelo Pydantic desde una lista
    de objetos de SQLAlchemy"""

    grades: list[Grade] = await faker_db_func(db, fake_grade, num_rows=2)

    grade = grades[0]
    grade_schema = GradeSchema.model_validate(grade)
    assert grade_schema.id == grade.id
    assert grade_schema.name == grade.name
    assert grade_schema.level == grade.level

    userlist = TypeAdapter(list[GradeSchema])
    schemas = userlist.validate_python(grades)
    assert len(schemas) == len(grades)
    assert schemas[0].id == grades[0].id
    assert schemas[0].name == grades[0].name
    assert schemas[0].level == grades[0].level
