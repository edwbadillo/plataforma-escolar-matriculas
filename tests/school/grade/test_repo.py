from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade
from app.school.grade.repo import get_grades


async def test_list_grades(db: AsyncSession, grades: list[Grade]):
    """Lista todos los grados del colegio"""

    grades_list = list(await get_grades(db))
    assert len(grades_list) == len(grades)

    first_grade = grades_list[0]
    assert first_grade.id == grades[0].id
    assert first_grade.name == grades[0].name
    assert first_grade.level == grades[0].level
