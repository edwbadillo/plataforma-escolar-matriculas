import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade
from app.school.grade.repo import exists_by_id, get_grades


async def test_list_grades(db: AsyncSession, grades: list[Grade]):
    """Lista todos los grados del colegio"""

    grades_list = await get_grades(db)
    assert len(grades_list) == len(grades)

    first_grade = grades_list[0]
    assert first_grade.id == grades[0].id
    assert first_grade.name == grades[0].name
    assert first_grade.level == grades[0].level


@pytest.mark.parametrize(
    "id, exists",
    [
        (0, True),
        (345, False),
    ],
)
async def test_exists_by_id(
    db: AsyncSession, grades: list[Grade], id: int, exists: bool
):
    """Verifica que existe el grado con el id dado"""

    assert await exists_by_id(db, id) == exists
