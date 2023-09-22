import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.repo import exists_by_id, get_grades

from .faker import fake_grade


async def test_list_grades(db: AsyncSession):
    """Lista todos los grados del colegio"""

    grades_in_db = await fake_grade(db, num_rows=5)

    grades_list = await get_grades(db)
    assert len(grades_list) == len(grades_in_db)

    first_grade = grades_list[0]
    assert first_grade.id == grades_in_db[0].id
    assert first_grade.name == grades_in_db[0].name
    assert first_grade.level == grades_in_db[0].level


@pytest.mark.parametrize(
    "id, exists",
    [
        (2, True),
        (345, False),
    ],
)
async def test_exists_by_id(db: AsyncSession, id: int, exists: bool):
    """Verifica que existe el grado con el id dado"""
    await fake_grade(db, id=2)
    assert await exists_by_id(db, id) == exists
