from pydantic import TypeAdapter

from app.school.grade.models import Grade
from app.school.grade.schemas import GradeSchema


async def test_grades_schema_list(grades: list[Grade]):
    """Verifique que no haya problema al convertir a un modelo Pydantic desde una lista
    de objetos de SQLAlchemy"""

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